from fastapi.websockets import WebSocket
from ..schemas.game import TicTacToeGameSchema
from ..models import UserModel


class TicTacToeManager:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.spectator_list: list[WebSocket] = []
        self.connection_list: list[list[WebSocket, UserModel]]
        self.game_state = TicTacToeGameSchema({
            "players": [],
            "score": [0, 0],
            "board": [None, None, None,
                      None, None, None,
                      None, None, None],
            "current_player": 0,
            "round": 0,
            "is_finished": False,
            "ready": [False, False],
            "max_players": 2
        })



