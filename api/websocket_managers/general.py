from fastapi.websockets import WebSocket
from websockets.exceptions import ConnectionClosed
from fastapi import HTTPException
from ..services import user_service
from ..database import SessionLocal
from uuid import uuid4


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
            pass

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
                await connection[0].send_json(self.chat_state)
            except ConnectionClosed:
                pass

    async def receive_message(self, message: str, ws: WebSocket):
        for connection in self.connection_list:
            if connection[0] is ws and connection[1]:
                self.chat_state.append(f"{connection[1]}: {message}")
                await self.send_chat_to_all()
                break

    async def send_chat_to_one(self, ws: WebSocket):
        await ws.send_json(self.chat_state)

    async def disconnect(self, ws: WebSocket):
        for connection in self.connection_list:
            if connection[0] is ws:
                self.connection_list.remove(connection)
                break

    async def dispatch(self, data: dict, ws: WebSocket):
        actions = ['message', 'authorize']
        action = data.get('action')
        if action not in actions:
            return
        if action == "authorize":
            await self.authorize(ws=ws, access_token=data['access_token'])
        elif action == "message" and data.get("text"):
            await self.receive_message(message=data['text'], ws=ws)


class RoomListManager:

    room_list = []
    connection_list: list[WebSocket] = []

    @classmethod
    async def send_to_all(cls):
        rooms = [{
            "id": room.room_id,
            "players": len(room.game_state.players),
            "game": room.game_name
        } for room in cls.room_list]
        for connection in cls.connection_list:
            try:
                await connection.send_json(rooms)
            except ConnectionClosed:
                cls.connection_list.remove(connection)

    @classmethod
    async def send_to_one(cls, ws: WebSocket):
        rooms = [{
            "id": room.room_id,
            "players": len(room.game_state.players),
            "game": room.game_name
        } for room in cls.room_list]
        await ws.send_json(rooms)

    @classmethod
    async def create_room(cls, room):
        room_manager = room(str(uuid4()))
        cls.room_list.append(room_manager)
        await cls.send_to_all()

    @classmethod
    async def remove_room(cls, room_id: str):
        for room_manager in cls.room_list:
            if room_manager.room_id == room_id:
                cls.room_list.remove(room_manager)
                del room_manager
                break
        await cls.send_to_all()

    @classmethod
    async def disconnect(cls, ws: WebSocket):
        cls.connection_list.remove(ws)
