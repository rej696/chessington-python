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
        self.has_moved = False

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
        self.has_moved = True

    def _get_available_diagonal_moves(self, board):
        return (
            list(self._available_moves_in_direction(board, lambda s: Square.at(s.row + 1, s.col + 1))) +
            list(self._available_moves_in_direction(board, lambda s: Square.at(s.row + 1, s.col - 1))) +
            list(self._available_moves_in_direction(board, lambda s: Square.at(s.row - 1, s.col + 1))) +
            list(self._available_moves_in_direction(board, lambda s: Square.at(s.row - 1, s.col - 1)))
        )

    def _available_moves_in_direction(self, board, direction_function):
        next_square = direction_function(board.find_piece(self))
        while self._is_free_or_capturable(board, next_square):
            yield next_square
            if board.square_is_occupied(next_square):
                break
            next_square = direction_function(next_square)

    def _is_free_or_capturable(self, board, square):
        return board.square_in_bounds(square) and (board.square_is_empty(square) or self._is_piece_capturable(board.get_piece(square)))

    def _is_square_capturable(self, board, square):
        return (
            board.square_in_bounds(square) and 
            board.square_is_occupied(square) and 
            self._is_piece_capturable(board.get_piece(square))
        )

    def _is_piece_capturable(self, piece):
        return piece.player != self.player


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_available_moves(self, board):
        location = board.find_piece(self)
        delta = 1 if self.player == Player.WHITE else -1
        
        single_move_square = Square.at(location.row + delta, location.col)
        double_move_square = Square.at(location.row + 2 * delta, location.col)
        
        normal_moves = []
        if not board.square_in_bounds(single_move_square) or board.square_is_occupied(single_move_square):
            normal_moves = []
        elif self.has_moved or not board.square_in_bounds(double_move_square) or board.square_is_occupied(double_move_square):
            normal_moves = [single_move_square]
        else:
            normal_moves = [single_move_square, double_move_square]

        capture_moves = [Square.at(location.row + delta, location.col + 1), Square.at(location.row + delta, location.col - 1)]
        capture_moves = list(filter(lambda square: self._is_square_capturable(board, square), capture_moves))

        return normal_moves + capture_moves


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        location = board.find_piece(self)
        row, col = location.row, location.col

        candidate_moves = [
            Square.at(row + 2, col + 1), Square.at(row + 2, col - 1), 
            Square.at(row + 1, col + 2), Square.at(row + 1, col - 2),
            Square.at(row - 2, col + 1), Square.at(row - 2, col - 1), 
            Square.at(row - 1, col + 2), Square.at(row - 1, col - 2),
        ]

        return list(filter(lambda square: self._is_free_or_capturable(board, square), candidate_moves))


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        return self._get_available_diagonal_moves(board)


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
        location = board.find_piece(self)
        row, col = location.row, location.col

        candidate_moves = [
            Square.at(row + 1, col + 1), Square.at(row + 1, col), Square.at(row + 1, col - 1),
            Square.at(row, col + 1), Square.at(row, col - 1),
            Square.at(row - 1, col + 1), Square.at(row - 1, col), Square.at(row - 1, col - 1)
        ]

        return list(filter(lambda square: self._is_free_or_capturable(board, square), candidate_moves))