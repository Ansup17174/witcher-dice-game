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
    round_result: Optional[int] = None
    timeout: Optional[int] = None


class TicTacToeGameSchema(BaseModel):
    players: list[str]
    score: list[int]
    board: list[Optional[int]]
    current_player: Optional[int] = None
    round: int
    is_finished: bool
    winner: Optional[int] = None
    ready: list[bool]
    round_result: Optional[int] = None
    timeout: Optional[int] = None


class BlackQueenGameSchema(BaseModel):
    players: list[str]
    score: list[int]
    ready: list[bool]
    decks: list[dict[str, list[str]]]
    table: list[list[str, int]]
    current_player: Optional[int] = None
    is_finished: bool
    turn: int
    deal: int
    scoring_cards: dict[str, int]
    timeout: Optional[int] = None
