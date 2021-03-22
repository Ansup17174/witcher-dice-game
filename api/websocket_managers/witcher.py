from fastapi.websockets import WebSocket
from .general import RoomListManager
from ..services import user_service
from ..database import SessionLocal
from ..schemas.game import WitcherGameSchema
from ..utils import look_for_patterns, compare_dices
from .base_game import BaseRoomManager
from sqlalchemy.orm import Session
import random


class WitcherRoomManager(BaseRoomManager):

    game_name = "Witcher-dice"
    max_players = 2
    use_timer = False

    def __init__(self, room_id: str):
        super().__init__(room_id=room_id)
        self.game_state: WitcherGameSchema = WitcherGameSchema(**{
            "players": [],
            "score": [0, 0],
            "dices": [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ],
            "dices_value": [0, 0],
            "current_player": None,
            "turn": 0,
            "deal": 1,
            "is_finished": False,
            "ready": [False, False],
        })

    async def roll_dices(self, player_index: int = None, chosen_dices: list[int] = None):
        if chosen_dices is None:
            chosen_dices = [0, 1, 2, 3, 4]
        else:
            chosen_dices = list(set([el for el in chosen_dices if el in [0, 1, 2, 3, 4]]))
        if player_index is None:
            player_index = self.game_state.current_player
        for number in chosen_dices:
            self.game_state.dices[player_index][number] = random.randint(1, 6)
        self.game_state.dices_value[player_index] = look_for_patterns(self.game_state.dices[player_index])

    async def reset_dices(self):
        await self.roll_dices(player_index=0)
        await self.roll_dices(player_index=1)

    async def initialize_game(self):
        self.game_state.turn = 0
        self.game_state.dices = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        self.game_state.current_player = 0

    async def finish_game(self, db: Session = SessionLocal()):
        self.game_state.is_finished = True
        await self.send_game_state()
        winner_index = 0 if self.game_state.score[0] > self.game_state.score[1] else 1
        loser_index = 0 if winner_index == 1 else 1
        winner_username = self.game_state.players[winner_index]
        loser_username = self.game_state.players[loser_index]
        self.game_state.winner = winner_username
        await self.send_game_state()
        for connection in self.connection_list:
            if connection[1].username == winner_username:
                winner_id = connection[1].id
            elif connection[1].username == loser_username:
                loser_id = connection[1].id
        winner_stats = user_service.get_user_stats(
            db=db,
            user_id=winner_id,
            game="Witcher-dice",
            limit=1,
            offset=0
        )[0]
        loser_stats = user_service.get_user_stats(
            db=db,
            user_id=loser_id,
            game="Witcher-dice",
            limit=1,
            offset=0
        )[0]
        winner_stats.matches_won += 1
        winner_stats.matches_played += 1
        loser_stats.matches_lost += 1
        loser_stats.matches_played += 1
        db.commit()
        db.close()
        for connection in self.connection_list:
            await connection[0].close()
        for spectator in self.spectator_list:
            await spectator.close()
        RoomListManager.room_list.remove(self)
        await RoomListManager.send_to_all()

    async def next_round(self):
        self.game_state.deal += 1
        self.game_state.ready = [False, False]
        if self.game_state.dices_value[0] > self.game_state.dices_value[1]:
            self.game_state.score[0] += 1
            self.game_state.round_result = 0
        elif self.game_state.dices_value[0] < self.game_state.dices_value[1]:
            self.game_state.score[1] += 1
            self.game_state.round_result = 1
        else:
            winning_index = compare_dices(
                self.game_state.dices[0],
                self.game_state.dices[1],
                self.game_state.dices_value[0]
            )
            if winning_index >= 0:
                self.game_state.score[winning_index] += 1
                self.game_state.round_result = winning_index
            else:
                self.game_state.round_result = -1

    async def timed_out(self):
        if not self.use_timer:
            return
        self.game_state.is_finished = True
        if self.game_state.current_player is None:
            score1, score2 = self.game_state.score
            if score1 == score2 == 0:
                self.game_state.round_result = -1
                RoomListManager.room_list.remove(self)
                await RoomListManager.send_to_all()
                await self.send_game_state()
                await self.disconnect_all()
            elif score1 == score2:
                ready1, ready2 = self.game_state.ready
                if ready1 == ready2:
                    self.game_state.round_result = -1
                    RoomListManager.room_list.remove(self)
                    await RoomListManager.send_to_all()
                    await self.send_game_state()
                    await self.disconnect_all()
                else:
                    self.game_state.score = [2, 0] if ready1 else [0, 2]
                    await self.finish_game()
            else:
                await self.finish_game()
        else:
            self.game_state.score = [2, 0] if self.game_state.current_player else [0, 2]
            await self.finish_game()

    async def dispatch(self, data: dict, ws: WebSocket):
        actions = ['roll', 'pass', 'ready', 'authorize']
        action = data.get('action')
        if action not in actions:
            await self.send_game_state()
            return
        if self.game_state.is_finished:
            return
        if action == 'authorize' and data.get('access_token'):
            await self.authorize(ws=ws, access_token=data['access_token'])
            return
        user = await self.get_user(ws)
        if not user:
            await self.send_game_state()
            return
        player_index = self.game_state.players.index(user.username)
        if action == 'ready':
            await self.claim_readiness(player_index)
            return
        if player_index != self.game_state.current_player:
            await self.send_game_state()
            return
        if not self.game_state.ready[0] and not self.game_state.ready[1]:
            await self.send_game_state()
            return
        if action == 'roll':
            chosen_dices = data.get('dices')
            if self.game_state.turn > 1:
                await self.roll_dices(player_index=player_index, chosen_dices=chosen_dices)
            else:
                await self.roll_dices(player_index=player_index)
        elif action == 'pass':
            if self.game_state.turn < 2:
                return
            await self.send_game_state()
        self.game_state.turn += 1
        if self.game_state.turn == 4:
            await self.next_round()
        if self.game_state.score[0] == 2 or self.game_state.score[1] == 2:
            await self.finish_game()
        self.game_state.current_player = 0 if self.game_state.current_player == 1 else 1
        await self.send_game_state()
