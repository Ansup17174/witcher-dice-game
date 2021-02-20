from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi import HTTPException
from . import services
from .database import SessionLocal


class ConnectionManager:
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
            await self.send_users_list()
        except HTTPException:
            raise WebSocketDisconnect

    async def disconnect(self, ws: WebSocket):
        for connection in self.connection_list:
            if connection[0] is ws:
                self.connection_list.remove(connection)
        await ws.close()

    async def send_users_list(self):
        users = [connection[1] for connection in self.connection_list if connection[1]]
        for connection in self.connection_list:
            await connection[0].send_json(users)
