import asyncio
from .general import RoomListManager


class Timer:

    def __init__(self, initial_timeout: int, room):
        if initial_timeout <= 0:
            raise ValueError("Timeout has to be longer than 0 seconds")
        self.initial_timeout = initial_timeout
        self.timeout = initial_timeout
        self.room = room

    async def start(self):
        while True:
            self.room.game_state.timeout = self.timeout
            await self.room.send_game_state()
            await asyncio.sleep(1)
            self.timeout -= 1
            if self.timeout <= 0:
                self.room.game_state.timeout = None
                await self.room.send_game_state()
                await self.room.timed_out()
                break
        del self

    async def reset(self):
        self.timeout = self.initial_timeout
