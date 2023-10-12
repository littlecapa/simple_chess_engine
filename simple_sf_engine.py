import chess

from engine_libs.eval import Eval as e
from engine_libs.move_logger import Move_Logger as ml
from engine_libs.log_lib import setup_logging
import logging


class ChessEngine_v7:
    def __init__(self, initial_position_fen, max_depth=3):
        self.board = chess.Board(initial_position_fen)
        self.max_depth = max_depth
        self.evaluator = e()

    def evaluate_position(self):
      if self.board.is_checkmate():
        return float("-inf") if self.board.turn == chess.WHITE else float("inf")
      elif self.board.is_game_over():
        return 0.0
      mlog.add_eval
      score = self.evaluator.get_score(self.board.fen())
      #logging.info(f"FEN: {self.board.fen()}, Score: {score}")
      self.mlog.add_eval(-score)
      return -score
      
    def find_best_move(self, mlog):
        self.mlog = mlog
        best_move = None
        maximize = self.board.turn
        best_value = float("-inf") if maximize else float("inf")
        legal_moves = list(self.board.legal_moves)
        best_move = legal_moves[0]
        for move in legal_moves:
            self.mlog.make_move(move)
            self.board.push(move)
            value = self.minimax(self.max_depth - 1, not maximize)
            self.board.pop()
            self.mlog.take_move_back()
            if maximize:
              if value > best_value:
                best_value = value
                best_move = move
            else:
              if value < best_value:
                best_value = value
                best_move = move
        return best_move, best_value

    def minimax(self, depth, maximize):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_position()

        legal_moves = list(self.board.legal_moves)
        best_value = float("-inf") if maximize else float("inf")

        for move in legal_moves:
            self.mlog.make_move(move)
            self.board.push(move)
            value = self.minimax(depth - 1, not maximize)
            best_value = max(best_value, value) if maximize else min(best_value, value)
            self.board.pop()
            self.mlog.take_move_back()
        return best_value

if __name__ == "__main__":
    # Step 1: Setup Initial Position
    start_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    initial_position = start_position
    max_depth = 3  # Adjust the maximum search depth
    
    chess_engine = ChessEngine_v7(initial_position, max_depth)
    board = chess_engine.board
    setup_logging()
    logging.info("Start")
    while not board.is_game_over():
        # Step 2: Computer finds the best move
        mlog = ml(board)
        best_move, value = chess_engine.find_best_move(mlog)
        print(f"Best: {best_move} {value}")
        logging.info(mlog.get_pgn())

        # Step 3: Move is executed on the board
        board.push(best_move)
        print(f"New FEN: {board.fen()}\n")

        # Step 4: Disply Board
        print(board)

        # Step 5: User enters a move
        user_move = input("Enter your move (e.g., 'e2e4'): ")

        # Step 6: Move is executed on the board
        try:
            board.push_san(user_move)
        except ValueError:
            print("Invalid move. Please try again.")
            continue

    # Step 7: Game is over
    print("Game over. Result: " + board.result())
