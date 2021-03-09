import asyncio


class Timer:

    def __init__(self, timeout: int, room):
        if timeout <= 0:
            raise ValueError("Timeout has to be longer than 0 seconds")
        self.timeout = timeout
        self.room = room

    async def run(self):
        while True:
            self.room.game_state.timeout = self.timeout
            await self.room.send_game_state()
            await asyncio.sleep(1)
            self.timeout -= 1
            if self.timeout <= 0:
                print("Time up!")
                break
        del self

    async def reset(self, timeout: int):
        self.timeout = timeout
