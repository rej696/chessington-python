"""
A module providing a representation of a chess board. The rules of chess are not implemented - 
this is just a "dumb" board that will let you move pieces around as you like.
"""

from collections import namedtuple
from enum import Enum, auto

from chessington.engine.data import Player, Square
from chessington.engine.pieces import Pawn, Knight, Bishop, Rook, Queen, King

BOARD_SIZE = 8

class Board:
    """
    A representation of the chess board, and the pieces on it.
    """

    def __init__(self, player, board_state):
        self.current_player = player
        self.board = board_state
        self.next_move = None
        self.value = None
        self.total_value = None
        self.last_move_pawn = None

    @staticmethod
    def empty():
        return Board(Player.WHITE, Board._create_empty_board())

    @staticmethod
    def at_starting_position():
        return Board(Player.WHITE, Board._create_starting_board())

    @staticmethod
    def _create_empty_board():
        return [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    @staticmethod
    def _create_starting_board():

        # Create an empty board
        board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

        # Setup the rows of pawns
        board[1] = [Pawn(Player.WHITE) for _ in range(BOARD_SIZE)]
        board[6] = [Pawn(Player.BLACK) for _ in range(BOARD_SIZE)]

        # Setup the rows of pieces
        piece_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        board[0] = list(map(lambda piece: piece(Player.WHITE), piece_row))
        board[7] = list(map(lambda piece: piece(Player.BLACK), piece_row))

        return board

    def set_piece(self, square, piece):
        """
        Places the piece at the given position on the board.
        """
        self.board[square.row][square.col] = piece

    def get_piece(self, square):
        """
        Retrieves the piece from the given square of the board.
        """
        return self.board[square.row][square.col]

    def in_bounds(self, square):
        return 0 <= square.row <= 7 and 0 <= square.col <= 7

    def is_square_empty(self, square):
        return self.get_piece(square) is None

    def is_square_full(self, square):
        return not self.is_square_empty(square)

    def is_square_attackable(self, square, current_player):
        if self.is_square_full(square):
            return self.get_piece(square).player != current_player
        return False

    def find_piece(self, piece_to_find):
        """
        Searches for the given piece on the board and returns its square.
        """
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] is piece_to_find:
                    return Square.at(row, col)
        raise Exception('The supplied piece is not on the board')

    def move_piece(self, from_square, to_square):
        """
        Moves the piece from the given starting square to the given destination square.
        """
        moving_piece = self.get_piece(from_square)
        if moving_piece is not None and moving_piece.player == self.current_player:
            self.set_piece(to_square, moving_piece)
            self.set_piece(from_square, None)
            self.en_passant_deletion(to_square, moving_piece)
            self.pawn_promotion_check(to_square)
            self.en_passant_check(from_square, to_square, moving_piece)
            self.current_player = self.current_player.opponent()

    def pawn_promotion_check(self, to_square):
        piece_to_promote = self.get_piece(to_square)
        if isinstance(piece_to_promote, Pawn):
            if piece_to_promote.edge_check_row(to_square):
                self.set_piece(to_square, Queen(self.current_player))

    def en_passant_check(self, from_square, to_square, moving_piece):
        if not isinstance(moving_piece, Pawn):
            self.last_move_pawn = None
            return
        if abs(to_square.row - from_square.row) == 2:
            self.last_move_pawn = Square.at(to_square.row, to_square.col)
            return
        self.last_move_pawn = None

    def en_passant_deletion(self, to_square, moving_piece):
        if not isinstance(moving_piece, Pawn):
            return
        if moving_piece.en_passant_attack(self, to_square):
            self.set_piece(self.last_move_pawn, None)
