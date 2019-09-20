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


class ChessBotDefense:
    def __init__(self):
        pass

    def do_move(self, board):
        enemy_pieces = self.get_enemy_locations(board)
        death_squares = self.get_death_squares(board, enemy_pieces)
        while True:
            try:
                selected_square = self.get_random_square()
                while not self.check_valid_piece(board, selected_square):
                    selected_square = self.get_random_square()
                selected_move = self.random_move(board, selected_square)
                if not self.check_death_square(death_squares, selected_move):
                    board.get_piece(selected_square).move_to(board, selected_move)
                    return
            except:
                continue

    def get_random_square(self):
        random_col = random.choice(range(8))
        random_row = random.choice(range(8))
        return Square.at(random_row, random_col)

    def check_valid_piece(self, board, selected_square):
        if board.is_square_empty(selected_square):
            return False
        return board.get_piece(selected_square).player == Player.BLACK

    def check_enemy_piece(self, board, selected_square):
        if board.is_square_empty(selected_square):
            return False
        return board.get_piece(selected_square).player == Player.WHITE

    def random_move(self, board, selected_square):
        current_piece = board.get_piece(selected_square)
        to_squares = current_piece.get_available_moves(board)
        return random.choice(to_squares)

    def get_enemy_locations(self, board):
        """
        Get all squares containing enemy pieces
        """
        enemy_pieces = []
        for square_row in range(8):
            for square_col in range(8):
                selected_square = Square.at(square_row, square_col)
                if self.check_enemy_piece(board, selected_square):
                    enemy_pieces.append(selected_square)
        return enemy_pieces

    def get_death_squares(self, board, enemy_pieces):
        """
        Get all squares enemy pieces can move into
        """
        death_squares = []
        for piece in enemy_pieces:
            death_squares += piece.get_available_moves(board)
        return death_squares

    def check_death_square(self, death_squares, selected_move):
        return selected_move in death_squares
