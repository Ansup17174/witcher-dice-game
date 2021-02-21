from fastapi.websockets import WebSocket
from fastapi import HTTPException
from . import services
from . import models
from . import schemas
from .database import SessionLocal
from uuid import uuid4
import random


class OnlineUsersManager:
    def __init__(self):
        self.connection_list: list[list[WebSocket, str]] = []

    async def authorize(self, ws: WebSocket, access_token: str):
        try:
            user = services.authenticate_user(token=access_token, db=SessionLocal())
            usernames = [connection[1] for connection in self.connection_list]
            if user.username not in usernames:
                for connection in self.connection_list:
                    if connection[0] is ws:
                        connection[1] = user.username
                        break
            await self.send_to_all()
        except HTTPException:
            await ws.send_text("Invalid token")

    async def disconnect(self, ws: WebSocket):
        for connection in self.connection_list:
            if connection[0] is ws:
                self.connection_list.remove(connection)
        await ws.close()

    async def send_to_one(self, ws: WebSocket):
        users = [connection[1] for connection in self.connection_list if connection[1]]
        await ws.send_json(users)

    async def send_to_all(self):
        users = [connection[1] for connection in self.connection_list if connection[1]]
        for connection in self.connection_list:
            await connection[0].send_json(users)


class PublicChatManager:
    def __init__(self):
        self.connection_list: list[list[WebSocket, str]] = []
        self.chat_state: list[str] = []

    async def authorize(self, ws: WebSocket, access_token: str):
        try:
            user = services.authenticate_user(token=access_token, db=SessionLocal())
            usernames = [connection[1] for connection in self.connection_list]
            if user.username not in usernames:
                for connection in self.connection_list:
                    if connection[0] is ws:
                        connection[1] = user.username
                        break
        except HTTPException:
            await ws.send_text("Invalid token")

    async def send_chat_to_all(self):
        for connection in self.connection_list:
            await connection[0].send_text("\n".join(self.chat_state))

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
        await ws.close()


class RoomManager:
    def __init__(self, room_id: str):
        self.room_id: str = room_id
        self.connection_list: list[list[WebSocket, models.User]] = []
        self.game_state: schemas.GameState = schemas.GameState(**{
            "players": [],
            "score": [0, 0],
            "dices": [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ],
            "current_player": 0,
            "turn": 1,
            "deal": 1
        })

    async def authorize(self, ws: WebSocket, access_token: str):
        try:
            user = services.authenticate_user(token=access_token, db=SessionLocal())
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
        await ws.close()

    async def send_game_state(self):
        for connection in self.connection_list:
            await connection[0].send_json(self.game_state)

    async def roll_dices(self, player_index: int = None, chosen_dices: list[int] = None):
        if chosen_dices is None:
            chosen_dices = [0, 1, 2, 3, 4]
        else:
            chosen_dices = list(set([el for el in chosen_dices if el in [0, 1, 2, 3, 4]]))
        if player_index is None:
            player_index = self.game_state.current_player
        for number in chosen_dices:
            self.game_state.dices[player_index][number] = random.randint(1, 6)

    async def game_step(self):
        pass

    async def initialize_game(self):
        await self.roll_dices(0)
        await self.roll_dices(1)


class RoomListManager:
    def __init__(self):
        self.connection_list: list[WebSocket] = []
        self.room_list: list[RoomManager] = []

    async def send_to_all(self):
        for connection in self.connection_list:
            await connection.send_json(self.room_list)

    async def send_to_one(self, ws: WebSocket):
        await ws.send_json(self.room_list)

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
