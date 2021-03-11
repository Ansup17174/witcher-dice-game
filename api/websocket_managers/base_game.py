from fastapi.websockets import WebSocket
from websockets.exceptions import ConnectionClosed
from fastapi import HTTPException
from .general import RoomListManager
from ..services import user_service
from ..database import SessionLocal
from ..models import UserModel
from .timer import Timer
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
import asyncio


class BaseRoomManager(ABC):

    game_name = None
    max_players = None

    @abstractmethod
    def __init__(self, room_id: str):
        """self.game_state, max_players and game_name has to be assigned"""
        self.room_id: str = room_id
        self.spectator_list: list[WebSocket] = []
        self.connection_list: list[list[WebSocket, UserModel]] = []
        self.game_state = None
        self.timer: Timer = Timer(60, self)

    async def authorize(self, ws: WebSocket, access_token: str):
        try:
            user = user_service.authenticate_user(token=access_token, db=SessionLocal())
            if user.username in self.game_state.players:
                self.connection_list.append([ws, user])
            elif len(self.game_state.players) < self.max_players:
                self.game_state.players.append(user.username)
                self.connection_list.append([ws, user])
                if len(self.connection_list) == 2:
                    asyncio.get_running_loop().create_task(self.timer.start())
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

    async def disconnect_all(self):
        for connection in self.connection_list:
            await connection[0].close()
        for spectator in self.spectator_list:
            await spectator.close()

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

    async def get_user(self, ws: WebSocket):
        user = None
        for connection in self.connection_list:
            if connection[0] is ws and connection[1]:
                user = connection[1]
                break
        return user

    async def claim_readiness(self, player_index: int):
        if self.game_state.ready != [True] * self.max_players and len(self.game_state.players):
            self.game_state.ready[player_index] = True
            await self.timer.reset()
            if self.game_state.ready == [True] * self.max_players:
                self.game_state.round_result = None
                await self.initialize_game()
            await self.send_game_state()

    @abstractmethod
    async def dispatch(self, data: dict, ws: WebSocket):
        pass

    @abstractmethod
    async def initialize_game(self):
        pass

    @abstractmethod
    async def next_round(self):
        pass

    @abstractmethod
    async def finish_game(self, db: Session = SessionLocal()):
        pass

    @abstractmethod
    async def timed_out(self):
        pass
