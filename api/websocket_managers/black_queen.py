from sqlalchemy.orm import Session
from fastapi.websockets import WebSocket
from websockets.exceptions import ConnectionClosed
from ..schemas.game import BlackQueenGameSchema
from ..database import SessionLocal
from ..services import user_service
from ..utils import get_scoring_cards
from .general import RoomListManager
import random
from .base_game import BaseRoomManager
from operator import itemgetter


class BlackQueenManager(BaseRoomManager):

    max_players = 3
    game_name = "Black-queen"
    allow_spectators = False
    use_timer = False

    def __init__(self, room_id: str):
        super().__init__(room_id=room_id)
        self.game_state = BlackQueenGameSchema(
            players=[],
            score=[0, 0, 0],
            ready=[False, False, False],
            decks=[
                {"s": [], "c": [], "d": [], "h": []},
                {"s": [], "c": [], "d": [], "h": []},
                {"s": [], "c": [], "d": [], "h": []}
            ],
            table=[],
            is_finished=False,
            turn=1,
            deal=0,
            scoring_cards=get_scoring_cards()
            )

    @staticmethod
    async def get_full_deck():
        """Card sign consist of two signs, first is suit(spade, club, diamond, heart), second is face cards"""
        deck = []
        for char in "scdh":
            for i in range(2, 15):
                deck.append(char + str(i))
        deck.remove("c2")
        return deck

    async def send_game_state(self):
        game_state = self.game_state.dict()
        del game_state['decks']
        user_data = dict(zip(self.game_state.players, self.game_state.decks))
        for connection in self.connection_list:
            try:
                game_state['deck'] = user_data[connection[1].username]
                await connection[0].send_json(game_state)
            except ConnectionClosed:
                pass
        for spectator in self.spectator_list:
            try:
                await spectator.send_json(self.game_state.dict())
            except ConnectionClosed:
                pass

    async def dispatch(self, data: dict, ws: WebSocket):
        actions = ("ready", "authorize", "put")
        action = data.get('action')
        if action not in actions:
            await self.send_game_state()
            return
        if self.game_state.is_finished:
            return
        if action == "authorize" and (token := data.get('access_token')):
            await self.authorize(ws=ws, access_token=token)
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
        if not self.game_state.ready[0] and not self.game_state.ready[1] and not self.game_state.ready[2]:
            await self.send_game_state()
            return
        if action == "put" and data.get('card'):
            card = data['card']
            deck = self.game_state.decks[player_index]
            if card not in deck[card[0]]:
                return
            if not len(self.game_state.table):
                if card[0] == "h":
                    if len(deck["s"]) or len(deck["c"]) or len(deck["d"]):
                        return
                self.game_state.table.append([card, player_index])
                deck[card[0]].remove(card)
                self.game_state.current_player = (self.game_state.current_player + 1) % 3
            else:
                if card[0] != (symbol := self.game_state.table[0][0][0]) and len(deck[symbol]):
                    return
                self.game_state.table.append([card, player_index])
                deck[card[0]].remove(card)
                self.game_state.current_player = (self.game_state.current_player + 1) % 3
            if len(self.game_state.table) == 3:
                table = self.game_state.table
                highest_card = max(table, key=lambda c: int(c[0][1:]))
                index = highest_card[1]
                points = 0
                for card in table:
                    if card[0] in self.game_state.scoring_cards:
                        points += self.game_state.scoring_cards[card[0]]
                self.game_state.score[index] += points
                self.game_state.table = []
                self.game_state.current_player = index
                self.game_state.turn += 1
                if self.game_state.turn == 18:
                    score1, score2, score3 = self.game_state.score
                    if score1 >= 100 or score2 >= 100 or score3 >= 100:
                        await self.finish_game()
                        return
                    await self.initialize_game()

    async def initialize_game(self):
        full_deck = await self.get_full_deck()
        random.shuffle(full_deck)
        part1 = full_deck[:17]
        part2 = full_deck[17:34]
        part3 = full_deck[34:]
        parts = [part1, part2, part3]
        for index, deck in enumerate(parts):
            for card in deck:
                self.game_state.decks[index][card[0]].append(card)
        self.game_state.turn = 1
        self.game_state.deal += 1
        for index, deck in enumerate(self.game_state.decks):
            if "c3" in deck["club"]:
                self.game_state.table.append(["c3", index])
                self.game_state.decks[index]["club"].remove("c3")
                self.game_state.current_player = (index + 1) % 3
                return

    async def next_round(self):
        pass

    async def finish_game(self, db: Session = SessionLocal()):
        self.game_state.is_finished = True
        score_table = sorted(zip(self.game_state.score, self.game_state.players), key=itemgetter(0))
        third_player = score_table[0][1]
        second_player = score_table[1][1]
        first_player = score_table[2][1]
        for connection in self.connection_list:
            if connection[1].username == third_player:
                third_user_id = connection[1].id
            elif connection[1].username == second_player:
                second_user_id = connection[1].id
            elif connection[1].username == first_player:
                first_user_id = connection[1].id
        third_stats = user_service.get_user_stats(
            db=db,
            limit=1,
            offset=0,
            user_id=third_user_id,
            game="Black-queen"
        )
        second_stats = user_service.get_user_stats(
            db=db,
            limit=1,
            offset=0,
            user_id=second_user_id,
            game="Black-queen"
        )
        first_stats = user_service.get_user_stats(
            db=db,
            limit=1,
            offset=0,
            user_id=first_user_id,
            game="Black-queen"
        )
        if score_table[0][0] < score_table[1][0] < score_table[2][0]:
            first_stats.matches_won += 1
            third_stats.matches_lost += 1
        elif score_table[0][0] == score_table[1][0] < score_table[2][0]:
            first_stats.matches_won += 1
        elif score_table[0][0] < score_table[1][0] == score_table[2][0]:
            third_stats.matches_lost += 1
        first_stats.matches_played += 1
        second_stats.matches_played += 1
        third_stats.matches_played += 1
        db.commit()
        db.close()
        for connection in self.connection_list:
            await connection[0].close()
        for spectator in self.spectator_list:
            await spectator.close()
        RoomListManager.room_list.remove(self)
        await RoomListManager.send_to_all()

    async def timed_out(self):
        pass
