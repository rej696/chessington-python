"""
Definitions of each of the different chess pieces.
"""

from abc import ABC, abstractmethod

from chessington.engine.data import Player, Square

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

    def edge_check(self, current_square):
        if current_square.row == 7 or current_square.row == 0:
            return []
        return None


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_available_moves(self, board):
        current_square = self.position(board)
        directions = self.edge_check(current_square)
        if directions is None:
            directions = self.on_start_row(current_square)
        valid_moves = []
        for direction in directions:
            next_square = Square.at(current_square.row + direction, current_square.col)
            if board.is_square_empty(next_square):
                valid_moves.append(next_square)
            else:
                return []
        return valid_moves

    def on_start_row(self, current_square):
        if current_square.row == 1 or current_square.row == 6:
            direction = [1, 2] if self.player == Player.WHITE else [-1, -2]
        else:
            direction = [1] if self.player == Player.WHITE else [-1]
        return direction


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        return []


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        return []


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        return []


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        return []


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        return []