from fastapi.websockets import WebSocket
from fastapi import HTTPException
from . import services
from .database import SessionLocal
from uuid import uuid4


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


class RoomListManager:
    def __init__(self):
        self.connection_list: list[WebSocket] = []
        self.room_list: list[str] = []

    async def send_to_all(self):
        for connection in self.connection_list:
            await connection.send_json(self.room_list)

    async def send_to_one(self, ws: WebSocket):
        await ws.send_json(self.room_list)

    async def create_room(self):
        self.room_list.append(str(uuid4()))
        print(self.connection_list)
        await self.send_to_all()
        print(self.room_list)

    async def remove_room(self, room_id: str):
        if room_id in self.room_list:
            self.room_list.remove(room_id)
            await self.send_to_all()
