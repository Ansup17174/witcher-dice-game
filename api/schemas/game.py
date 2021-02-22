from typing import Optional
from pydantic import BaseModel


class GameStateSchema(BaseModel):
    players: list[str]
    score: list[int]
    dices: list[list[int]]
    dices_value: list[int, int]
    current_player: Optional[int] = 0
    turn: int
    deal: int
    is_finished: bool
