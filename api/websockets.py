from fastapi.websockets import WebSocket
from fastapi import HTTPException
from . import services
from .database import SessionLocal


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


class InvitationsManager:
    def __init__(self):
        self.connection_list: list[WebSocket] = []




class GameManager:

    def __init__(self, game_id: str):
        self.game_id: str = game_id
        self.game_state: dict = {

        }


