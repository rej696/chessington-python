import random
from chessington.engine.data import Player, Square


class ChessBotRandom:
    def __init__(self):
        pass

    def do_move(self, board):
        while True:
            try:
                selected_square = self.get_random_square()
                while not self.valid_piece(board, selected_square):
                    selected_square = self.get_random_square()
                selected_move = self.random_move(board, selected_square)
                board.get_piece(selected_square).move_to(board, selected_move)
                return
            except:
                continue

    def get_random_square(self):
        random_col = random.choice(range(8))
        random_row = random.choice(range(8))
        return Square.at(random_row, random_col)

    def valid_piece(self, board, selected_square):
        if board.is_square_empty(selected_square):
            return False
        return board.get_piece(selected_square).player == Player.BLACK

    def random_move(self, board, selected_square):
        current_piece = board.get_piece(selected_square)
        to_squares = current_piece.get_available_moves(board)
        return random.choice(to_squares)
