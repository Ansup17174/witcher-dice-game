from fastapi.websockets import WebSocket
from websockets.exceptions import ConnectionClosed
from fastapi import HTTPException
from .general import RoomListManager
from ..services import user_service
from ..database import SessionLocal
from ..models import UserModel

from ..utils import look_for_patterns, compare_dices
from sqlalchemy.orm import Session
import random


class BaseRoomManager:
    def __init__(self, room_id: str):
        """self.game_state has to be assigned"""
        self.room_id: str = room_id
        self.spectator_list: list[WebSocket] = []
        self.connection_list: list[list[WebSocket, UserModel]] = []
        self.game_state = None
        self.game_name = None

    async def authorize(self, ws: WebSocket, access_token: str):
        try:
            user = user_service.authenticate_user(token=access_token, db=SessionLocal())
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

    async def initialize_game(self):
        """Must be implemented"""
        raise NotImplementedError()

    async def finish_game(self, db: Session = SessionLocal()):
        raise NotImplementedError("function finish_game has to be implemented")

    async def get_user(self, ws: WebSocket):
        user = None
        for connection in self.connection_list:
            if connection[0] is ws and connection[1]:
                user = connection[1]
                break
        return user

    async def claim_readiness(self, player_index: int):
        if self.game_state.ready != [True] * self.game_state.max_players:
            self.game_state.ready[player_index] = True
            if self.game_state.ready == [True] * self.game_state.max_players:
                await self.initialize_game()
            await self.send_game_state()

    async def dispatch(self, data: dict, ws: WebSocket):
        raise NotImplementedError("function dispatch has to be implemented")
