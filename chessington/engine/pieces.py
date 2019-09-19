"""
Definitions of each of the different chess pieces.
"""

from abc import ABC, abstractmethod
import logging
from chessington.engine.data import Player, Square
logging.basicConfig(filename="pieces.log", filemode="w", level=logging.DEBUG)


class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player):
        self.player = player

    @abstractmethod
    def get_available_moves(self, board):
        """
        Get all squares that the piece is allowed to move to.
        """
        pass

    def move_to(self, board, new_square):
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)

    def position(self, board):
        """
        Attach the position of the piece to self
        """
        return board.find_piece(self)

    def edge_check_row(self, current_square):
        if current_square.row == 7 or current_square.row == 0:
            return True
        return False

    def edge_check_col(self, current_square):
        if current_square.col == 7 or current_square.col == 0:
            return True
        return False

    def move_continuous(self, board, vertical_dir, horizontal_dir):
        current_square = self.position(board)
        next_square = Square.at(current_square.row, current_square.col)
        valid_moves = []
        while True:
            next_square = Square.at(next_square.row + vertical_dir, next_square.col + horizontal_dir)
            if not board.in_bounds(next_square):
                return valid_moves
            if board.is_square_empty(next_square):
                valid_moves.append(next_square)
            elif board.is_square_attackable(next_square, self.player):
                valid_moves.append(next_square)
                return valid_moves
            else:
                return valid_moves

    def move_single(self, board, vertical_dir, horizontal_dir):
        current_square = self.position(board)
        valid_moves = []
        next_square = Square.at(current_square.row + vertical_dir, current_square.col + horizontal_dir)
        if not board.in_bounds(next_square):
            return valid_moves
        if board.is_square_empty(next_square) or board.is_square_attackable(next_square, self.player):
            valid_moves.append(next_square)
            return valid_moves
        else:
            return valid_moves


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_available_moves(self, board):
        current_square = self.position(board)
        valid_moves = []
        is_on_edge = self.edge_check_row(current_square)
        ranges = []
        if not is_on_edge:
            ranges = self.on_start_row(current_square)
            valid_moves = self.kill_opponent(current_square, board)
            logging.info(f"{self.player} has {valid_moves} as valid moves for attacking")
        else:
            logging.info(f"{self.player} is on edge at {current_square}")
        for location in ranges:
            next_square = Square.at(current_square.row + location, current_square.col)
            if board.is_square_empty(next_square):
                valid_moves.append(next_square)
            else:
                logging.info(f"{self.player} has {valid_moves} as valid moves for moving into")
                return valid_moves
        logging.info(f"{self.player} has {valid_moves} as valid moves for moving into")
        return valid_moves

    def on_start_row(self, current_square):
        if current_square.row == 1 or current_square.row == 6:
            direction = [1, 2] if self.player == Player.WHITE else [-1, -2]
        else:
            direction = [1] if self.player == Player.WHITE else [-1]
        return direction

    def kill_opponent(self, current_square, board):
        direction_row = 1 if self.player == Player.WHITE else -1
        directions_col = []
        if current_square.col == 0:
            directions_col = [1]
        if current_square.col == 7:
            directions_col = [-1]
        if not self.edge_check_col(current_square):
            directions_col = [1, -1]
        attack_squares = []
        valid_attack_squares = []
        for direction_col in directions_col:
            attack_squares.append(Square.at(current_square.row + direction_row, current_square.col + direction_col))
        for attack_square in attack_squares:
            if board.is_square_attackable(attack_square, self.player):
                valid_attack_squares.append(attack_square)
        return valid_attack_squares


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        valid_moves = self.move_single(board, 2, 1)
        valid_moves += self.move_single(board, 2, -1)
        valid_moves += self.move_single(board, -2, 1)
        valid_moves += self.move_single(board, -2, -1)
        valid_moves += self.move_single(board, 1, 2)
        valid_moves += self.move_single(board, 1, -2)
        valid_moves += self.move_single(board, -1, 2)
        valid_moves += self.move_single(board, -1, -2)
        logging.info(f"{self.player} has {valid_moves} as valid moves for moving into")
        return valid_moves


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        valid_moves = self.move_continuous(board, 1, 1)
        valid_moves += self.move_continuous(board, -1, 1)
        valid_moves += self.move_continuous(board, 1, -1)
        valid_moves += self.move_continuous(board, -1, -1)
        logging.info(f"{self.player} has {valid_moves} as valid moves for moving into")
        return valid_moves


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        valid_moves = self.move_continuous(board, 1, 0)
        valid_moves += self.move_continuous(board, -1, 0)
        valid_moves += self.move_continuous(board, 0, 1)
        valid_moves += self.move_continuous(board, 0, -1)
        logging.info(f"{self.player} has {valid_moves} as valid moves for moving into")
        return valid_moves


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        valid_moves = self.move_continuous(board, 1, 0)
        valid_moves += self.move_continuous(board, -1, 0)
        valid_moves += self.move_continuous(board, 0, 1)
        valid_moves += self.move_continuous(board, 0, -1)
        valid_moves += self.move_continuous(board, 1, 1)
        valid_moves += self.move_continuous(board, -1, 1)
        valid_moves += self.move_continuous(board, 1, -1)
        valid_moves += self.move_continuous(board, -1, -1)
        logging.info(f"{self.player} has {valid_moves} as valid moves for moving into")
        return valid_moves


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        valid_moves = self.move_single(board, 1, 0)
        valid_moves += self.move_single(board, -1, 0)
        valid_moves += self.move_single(board, 0, 1)
        valid_moves += self.move_single(board, 0, -1)
        valid_moves += self.move_single(board, 1, 1)
        valid_moves += self.move_single(board, 1, -1)
        valid_moves += self.move_single(board, -1, 1)
        valid_moves += self.move_single(board, -1, -1)
        logging.info(f"{self.player} has {valid_moves} as valid moves for moving into")
        return valid_moves
