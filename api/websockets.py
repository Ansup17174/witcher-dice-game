from fastapi.websockets import WebSocket
from fastapi import HTTPException
from . import services
from .database import SessionLocal


class ConnectionManager:
    def __init__(self):
        self.connection_list: list[tuple[WebSocket, str]] = []

    async def authorize(self, websocket: WebSocket, access_token: str):
        try:
            user = services.authenticate_user(token=access_token, db=SessionLocal())
            if (websocket, user.username) not in self.connection_list:
                self.connection_list.append((websocket, user.username))
        except HTTPException:
            print("Unauthorized")

    async def disconnect(self, websocket: WebSocket):
        print("Disconnected")
        for connection in self.connection_list:
            if connection[0] == websocket:
                self.connection_list.remove(connection)
        await websocket.close()

    async def send_users_list(self):
        users = [connection[1] for connection in self.connection_list if connection[1]]
        for connection in self.connection_list:
            await connection[0].send_json(users)
