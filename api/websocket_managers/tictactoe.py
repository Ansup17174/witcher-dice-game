from sqlalchemy.orm import Session
from starlette.websockets import WebSocket
from ..schemas.game import TicTacToeGameSchema
from ..database import SessionLocal
from ..services import user_service
from .general import RoomListManager
from .base_game import BaseRoomManager


class TicTacToeManager(BaseRoomManager):

    game_name = "Tic-tac-toe"
    max_players = 2

    def __init__(self, room_id: str):
        super().__init__(room_id=room_id)
        self.game_state = TicTacToeGameSchema(
            players=[],
            score=[0, 0],
            board=[None]*9,
            current_player=0,
            round=1,
            is_finished=False,
            ready=[False]*self.max_players
        )

    async def check_board(self):
        board = self.game_state.board[:]
        for row in range(0, 7, 3):
            if board[row] == board[row+1] == board[row+2]:
                round_winner = board[row]
                self.game_state.score[round_winner] += 1
                await self.next_round()
                return
        for column in range(3):
            if board[column] == board[column+3] == board[column+6]:
                round_winner = board[column]
                self.game_state.score[round_winner] += 1
                await self.next_round()
                return
        if board[0] == board[4] == board[8] or board[2] == board[4] == board[6]:
            round_winner = board[4]
            self.game_state.score[round_winner] += 1
            await self.next_round()
            return

    async def dispatch(self, data: dict, ws: WebSocket):
        actions = ("ready", "authorize", "move")
        action = data.get('action')
        if action not in actions:
            await self.send_game_state()
            return
        if self.game_state.is_finished:
            return
        if action == "authorize" and (token := data.get('access_token')):
            await self.authorize(ws=ws, access_token=token)
            return
        user = await self.get_user(ws)
        if not user:
            await self.send_game_state()
            return
        player_index = self.game_state.players.index(user.username)
        if action == 'ready':
            await self.claim_readiness(player_index)
            return
        if player_index != self.game_state.current_player:
            await self.send_game_state()
            return
        if not self.game_state.ready[0] and not self.game_state.ready[1]:
            await self.send_game_state()
            return
        if action == "move" and (index := data.get('index')):
            if self.game_state.board[index] is not None:
                self.game_state.board[index] = player_index
                await self.check_board()

    async def initialize_game(self):
        self.game_state.board = [None] * 9
        self.game_state.current_player = 0
        await self.send_game_state()

    async def next_round(self):
        if self.game_state.score[0] == 2 or self.game_state.score[1] == 2:
            await self.finish_game()
        else:
            await self.initialize_game()
            self.game_state.round += 1

    async def finish_game(self, db: Session = SessionLocal()):
        self.game_state.is_finished = True
        await self.send_game_state()
        winner_index = 0 if self.game_state.score[0] > self.game_state.score[1] else 1
        loser_index = 0 if winner_index == 1 else 1
        winner_username = self.game_state.players[winner_index]
        loser_username = self.game_state.players[loser_index]
        self.game_state.winner = winner_username
        await self.send_game_state()
        for connection in self.connection_list:
            if connection[1].username == winner_username:
                winner_id = connection[1].id
            elif connection[1].username == loser_username:
                loser_id = connection[1].id
        winner_stats = user_service.get_user_stats(
            db=db,
            user_id=winner_id,
            game="Tic-tac-toe",
            limit=1,
            offset=0
        )[0]
        loser_stats = user_service.get_user_stats(
            db=db,
            user_id=loser_id,
            game="Tic-tac-toe",
            limit=1,
            offset=0
        )[0]
        winner_stats.matches_won += 1
        winner_stats.matches_played += 1
        loser_stats.matches_lost += 1
        loser_stats.matches_played += 1
        db.commit()
        for connection in self.connection_list:
            await connection[0].close()
        for spectator in self.spectator_list:
            await spectator.close()
        RoomListManager.room_list.remove(self)
        await RoomListManager.send_to_all()
