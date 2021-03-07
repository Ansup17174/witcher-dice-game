from fastapi.websockets import WebSocket
from websockets.exceptions import ConnectionClosed
from fastapi import HTTPException
from .general import RoomListManager
from ..services import user_service
from ..database import SessionLocal
from ..models import UserModel
from ..schemas.game import WitcherGameSchema
from ..utils import look_for_patterns, compare_dices
from sqlalchemy.orm import Session
import random


class WitcherRoomManager:
    def __init__(self, room_id: str):
        self.room_id: str = room_id
        self.spectator_list: list[WebSocket] = []
        self.connection_list: list[list[WebSocket, UserModel]] = []
        self.game_state: WitcherGameSchema = WitcherGameSchema(**{
            "players": [],
            "score": [0, 0],
            "dices": [
                [6, 6, 6, 6, 6],
                [6, 6, 6, 6, 6]
            ],
            "dices_value": [0, 0],
            "current_player": 0,
            "turn": 1,
            "deal": 1,
            "is_finished": False,
            "ready": [False, False],
            "max_players": 2
        })

    async def authorize(self, ws: WebSocket, access_token: str, db: Session = SessionLocal()):
        try:
            user = user_service.authenticate_user(token=access_token, db=db)
            if user.username in self.game_state.players:
                self.connection_list.append([ws, user])
            elif len(self.game_state.players) < self.game_state.max_players:
                self.game_state.players.append(user.username)
                self.connection_list.append([ws, user])
                await RoomListManager.send_to_all()
            else:
                self.spectator_list.append(ws)
        except HTTPException:
            await ws.send_text("Invalid token")
            self.spectator_list.append(ws)
        finally:
            await self.send_game_state()
            db.close()

    async def disconnect(self, ws: WebSocket):
        for connection in self.connection_list:
            if connection[0] is ws:
                self.connection_list.remove(connection)

    async def send_game_state(self):
        for connection in self.connection_list:
            try:
                await connection[0].send_json(self.game_state.dict())
            except ConnectionClosed:
                pass
        for spectator in self.spectator_list:
            try:
                await spectator.send_json(self.game_state.dict())
            except ConnectionClosed:
                pass

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
        await self.reset_dices()
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
            game="Witcher dice",
            limit=1,
            offset=0
        )[0]
        loser_stats = user_service.get_user_stats(
            db=db,
            user_id=loser_id,
            game="Witcher dice",
            limit=1,
            offset=0
        )[0]
        winner_stats.matches_won += 1
        winner_stats.matches_played += 1
        loser_stats.matches_lost += 1
        loser_stats.matches_played += 1
        db.commit()
        for connection in self.connection_list:
            await connection[0].close()
        for spectator in self.spectator_list:
            await spectator.close()
        RoomListManager.room_list.remove(self)

    async def get_user(self, ws: WebSocket):
        user = None
        for connection in self.connection_list:
            if connection[0] is ws and connection[1]:
                user = connection[1]
                break
        return user

    async def claim_readiness(self, player_index: int):
        if self.game_state.ready != [True, True]:
            self.game_state.ready[player_index] = True
            if self.game_state.ready == [True, True]:
                await self.initialize_game()
            await self.send_game_state()

    async def next_round(self):
        self.game_state.turn = 1
        self.game_state.deal += 1
        self.game_state.ready = [False, False]
        if self.game_state.dices_value[0] > self.game_state.dices_value[1]:
            self.game_state.score[0] += 1
            self.game_state.deal_result = 0
        elif self.game_state.dices_value[0] < self.game_state.dices_value[1]:
            self.game_state.score[1] += 1
            self.game_state.deal_result = 1
        else:
            winning_index = compare_dices(
                self.game_state.dices[0],
                self.game_state.dices[1],
                self.game_state.dices_value[0]
            )
            if winning_index >= 0:
                self.game_state.score[winning_index] += 1
                self.game_state.deal_result = winning_index
            else:
                self.game_state.deal_result = -1

    async def dispatch(self, data: dict, ws: WebSocket):
        actions = ['roll', 'pass', 'surrender', 'tie', 'ready', 'authorize']
        action = data.get('action')
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
        if action not in actions:
            await self.send_game_state()
            return
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
            await self.roll_dices(player_index=player_index, chosen_dices=chosen_dices)
        elif action == 'pass':
            await self.send_game_state()
        self.game_state.turn += 1
        if self.game_state.turn == 5:
            await self.next_round()
        if self.game_state.score[0] == 2 or self.game_state.score[1] == 2:
            await self.finish_game()
        self.game_state.current_player = 0 if self.game_state.current_player == 1 else 1
        await self.send_game_state()
