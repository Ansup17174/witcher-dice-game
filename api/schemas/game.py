from typing import Optional
from pydantic import BaseModel


class WitcherGameSchema(BaseModel):
    players: list[str]
    score: list[int]
    dices: list[list[int]]
    dices_value: list[int, int]
    current_player: Optional[int] = 0
    turn: int
    deal: int
    is_finished: bool
    winner: Optional[int] = None
    ready: list[bool]
    deal_result: Optional[int] = None


class TicTacToeGameSchema(BaseModel):
    players: list[str]
    score: list[int]
    board: list[Optional[int]]
    current_player: int
    round: int
    is_finished: bool
    winner: Optional[int] = None
    ready: list[bool]

