from fastapi.websockets import WebSocket
from websockets.exceptions import ConnectionClosed
from fastapi import HTTPException
from ..services import user_service
from ..models import UserModel
from ..schemas.game import GameStateSchema
from ..database import SessionLocal
from ..utils import look_for_patterns, compare_dices
from sqlalchemy.orm import Session
from uuid import uuid4
import random


async def authorize(connection_list: list[list[WebSocket, str]], ws: WebSocket, access_token: str):
    user = user_service.authenticate_user(token=access_token, db=SessionLocal())
    usernames = [connection[1] for connection in connection_list]
    if user.username not in usernames:
        for connection in connection_list:
            if connection[0] is ws:
                connection[1] = user.username
                break


class OnlineUsersManager:
    def __init__(self):
        self.connection_list: list[list[WebSocket, str]] = []

    async def authorize(self, ws: WebSocket, access_token: str):
        try:
            await authorize(self.connection_list, ws, access_token)
            await self.send_to_all()
        except HTTPException:
            await ws.send_text("Invalid token")

    async def disconnect(self, ws: WebSocket):
        for connection in self.connection_list:
            if connection[0] is ws:
                self.connection_list.remove(connection)

    async def send_to_one(self, ws: WebSocket):
        users = [connection[1] for connection in self.connection_list if connection[1]]
        await ws.send_json(users)

    async def send_to_all(self):
        users = [connection[1] for connection in self.connection_list if connection[1]]
        for connection in self.connection_list:
            try:
                await connection[0].send_json(users)
            except ConnectionClosed:
                pass


class PublicChatManager:
    def __init__(self):
        self.connection_list: list[list[WebSocket, str]] = []
        self.chat_state: list[str] = []

    async def authorize(self, ws: WebSocket, access_token: str):
        try:
            await authorize(self.connection_list, ws, access_token)
        except HTTPException:
            await ws.send_text("Invalid token")

    async def send_chat_to_all(self):
        for connection in self.connection_list:
            try:
                await connection[0].send_text("\n".join(self.chat_state))
            except ConnectionClosed:
                pass

    async def receive_message(self, message: str):
        self.chat_state.append(message)
        await self.send_chat_to_all()

    async def send_chat_to_one(self, ws: WebSocket):
        await ws.send_text("\n".join(self.chat_state))

    async def disconnect(self, ws: WebSocket):
        for connection in self.connection_list:
            if connection[0] is ws:
                self.connection_list.remove(connection)
                break


class RoomManager:
    def __init__(self, room_id: str):
        self.room_id: str = room_id
        self.connection_list: list[list[WebSocket, UserModel]] = []
        self.game_state: GameStateSchema = GameStateSchema(**{
            "players": [],
            "score": [0, 0],
            "dices": [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ],
            "dices_value": [0, 0],
            "current_player": 0,
            "turn": 1,
            "deal": 1,
            "is_finished": False,
            "ready": [False, False]
        })

    async def authorize(self, ws: WebSocket, access_token: str):
        try:
            user = user_service.authenticate_user(token=access_token, db=SessionLocal())
            if len(self.game_state.players) < 2:
                self.game_state.players.append(user.username)
                self.connection_list.append([ws, user])
            elif user.username in self.game_state.players:
                self.connection_list.append([ws, user])
            else:
                await ws.close()
        except HTTPException:
            await ws.send_text("Invalid token")

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
        for connection in self.connection_list:
            if connection[1].username == winner_username:
                winner_id = connection[1].id
            elif connection[1].username == loser_username:
                loser_id = connection[1].id
        winner_profile = user_service.get_user_profile(db=db, user_id=winner_id)
        loser_profile = user_service.get_user_profile(db=db, user_id=loser_id)
        winner_profile.matches_won += 1
        winner_profile.matches_played += 1
        loser_profile.matches_lost += 1
        loser_profile.matches_played += 1
        db.commit()
        for connection in self.connection_list:
            await connection[0].close()

    async def get_user(self, ws: WebSocket):
        user = None
        for connection in self.connection_list:
            if connection[0] is ws and connection[1]:
                user = connection[1]
                break
        return user

    async def dispatch(self, data: dict, ws: WebSocket):
        if self.game_state.is_finished:
            return
        user = await self.get_user(ws)
        if not user:
            await self.send_game_state()
            return
        player_index = self.game_state.players.index(user.username)
        actions = ['roll', 'pass', 'surrender', 'tie', 'ready']
        action = data.get('action')
        if action not in actions:
            await self.send_game_state()
            return
        if action == 'ready' and self.game_state.ready != [True, True]:
            self.game_state.ready[player_index] = True
            if self.game_state.ready == [True, True]:
                await self.initialize_game()
            await self.send_game_state()
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
            self.game_state.turn = 1
            self.game_state.deal += 1
            self.game_state.ready = [False, False]
            if self.game_state.dices_value[0] > self.game_state.dices_value[1]:
                self.game_state.score[0] += 1
            elif self.game_state.dices_value[0] < self.game_state.dices_value[1]:
                self.game_state.score[1] += 1
            else:
                winning_index = compare_dices(
                    self.game_state.dices[0],
                    self.game_state.dices[1],
                    self.game_state.dices_value[0]
                )
                if winning_index >= 0:
                    self.game_state.score[winning_index] += 1
        if self.game_state.score[0] == 2 or self.game_state.score[1] == 2:
            await self.finish_game()
        self.game_state.current_player = 0 if self.game_state.current_player == 1 else 1
        await self.send_game_state()


class RoomListManager:
    def __init__(self):
        self.connection_list: list[WebSocket] = []
        self.room_list: list[RoomManager] = []

    async def send_to_all(self):
        room_ids = [room.room_id for room in self.room_list]
        for connection in self.connection_list:
            try:
                await connection.send_json(room_ids)
            except ConnectionClosed:
                self.connection_list.remove(connection)

    async def send_to_one(self, ws: WebSocket):
        room_ids = [room.room_id for room in self.room_list]
        await ws.send_json(room_ids)

    async def create_room(self):
        room_manager = RoomManager(str(uuid4()))
        self.room_list.append(room_manager)
        await self.send_to_all()

    async def remove_room(self, room_id: str):
        for room_manager in self.room_list:
            if room_manager.room_id == room_id:
                self.room_list.remove(room_manager)
                break
        await self.send_to_all()

    async def disconnect(self, ws: WebSocket):
        self.connection_list.remove(ws)
