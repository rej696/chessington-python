from chessington.engine.board import Board
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Pawn
from chessington.engine.pieces import Rook
from chessington.engine.pieces import King
from chessington.engine.pieces import Bishop
from chessington.engine.pieces import Queen
from chessington.engine.pieces import Knight


class TestPawns:

    @staticmethod
    def test_white_pawns_can_move_up_one_square():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        square = Square.at(1, 4)
        board.set_piece(square, pawn)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(2, 4) in moves

    @staticmethod
    def test_black_pawns_can_move_down_one_square():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        square = Square.at(6, 4)
        board.set_piece(square, pawn)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(5, 4) in moves

    @staticmethod
    def test_white_pawn_can_move_up_two_squares_if_not_moved():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        square = Square.at(1, 4)
        board.set_piece(square, pawn)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(3, 4) in moves

    @staticmethod
    def test_black_pawn_can_move_down_two_squares_if_not_moved():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        square = Square.at(6, 4)
        board.set_piece(square, pawn)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(4, 4) in moves

    @staticmethod
    def test_white_pawn_cannot_move_up_two_squares_if_already_moved():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        starting_square = Square.at(1, 4)
        board.set_piece(starting_square, pawn)

        intermediate_square = Square.at(2, 4)
        pawn.move_to(board, intermediate_square)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(4, 4) not in moves

    @staticmethod
    def test_black_pawn_cannot_move_down_two_squares_if_already_moved():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        starting_square = Square.at(6, 4)
        board.set_piece(starting_square, pawn)

        intermediate_square = Square.at(5, 4)
        pawn.move_to(board, intermediate_square)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(3, 4) not in moves

    @staticmethod
    def test_white_pawn_cannot_move_if_piece_in_front():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        pawn_square = Square.at(4, 4)
        board.set_piece(pawn_square, pawn)

        obstructing_square = Square.at(5, 4)
        obstruction = Pawn(Player.BLACK)
        board.set_piece(obstructing_square, obstruction)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert len(moves) == 0

    @staticmethod
    def test_black_pawn_cannot_move_if_piece_in_front():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        pawn_square = Square.at(4, 4)
        board.set_piece(pawn_square, pawn)

        obstructing_square = Square.at(3, 4)
        obstruction = Pawn(Player.WHITE)
        board.set_piece(obstructing_square, obstruction)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert len(moves) == 0

    @staticmethod
    def test_white_pawn_cannot_move_two_squares_if_piece_two_in_front():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        pawn_square = Square.at(4, 4)
        board.set_piece(pawn_square, pawn)

        obstructing_square = Square.at(6, 4)
        obstruction = Pawn(Player.BLACK)
        board.set_piece(obstructing_square, obstruction)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert obstructing_square not in moves

    @staticmethod
    def test_black_pawn_cannot_move_two_squares_if_piece_two_in_front():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        pawn_square = Square.at(4, 4)
        board.set_piece(pawn_square, pawn)

        obstructing_square = Square.at(2, 4)
        obstruction = Pawn(Player.WHITE)
        board.set_piece(obstructing_square, obstruction)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert obstructing_square not in moves

    @staticmethod
    def test_white_pawn_cannot_move_two_squares_if_piece_one_in_front():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        pawn_square = Square.at(1, 4)
        board.set_piece(pawn_square, pawn)

        obstructing_square = Square.at(2, 4)
        obstruction = Pawn(Player.BLACK)
        board.set_piece(obstructing_square, obstruction)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(3, 4) not in moves

    @staticmethod
    def test_black_pawn_cannot_move_two_squares_if_piece_one_in_front():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        pawn_square = Square.at(6, 4)
        board.set_piece(pawn_square, pawn)

        obstructing_square = Square.at(5, 4)
        obstruction = Pawn(Player.WHITE)
        board.set_piece(obstructing_square, obstruction)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(4, 4) not in moves

    @staticmethod
    def test_white_pawn_cannot_move_at_top_of_board():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        square = Square.at(7, 4)
        board.set_piece(square, pawn)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert len(moves) == 0

    @staticmethod
    def test_black_pawn_cannot_move_at_bottom_of_board():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        square = Square.at(0, 4)
        board.set_piece(square, pawn)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert len(moves) == 0

    @staticmethod
    def test_white_pawns_can_capture_diagonally():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        pawn_square = Square.at(3, 4)
        board.set_piece(pawn_square, pawn)

        enemy1 = Pawn(Player.BLACK)
        enemy1_square = Square.at(4, 5)
        board.set_piece(enemy1_square, enemy1)

        enemy2 = Pawn(Player.BLACK)
        enemy2_square = Square.at(4, 3)
        board.set_piece(enemy2_square, enemy2)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert enemy1_square in moves
        assert enemy2_square in moves

    @staticmethod
    def test_black_pawns_can_capture_diagonally():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        pawn_square = Square.at(3, 4)
        board.set_piece(pawn_square, pawn)

        enemy1 = Pawn(Player.WHITE)
        enemy1_square = Square.at(2, 5)
        board.set_piece(enemy1_square, enemy1)

        enemy2 = Pawn(Player.WHITE)
        enemy2_square = Square.at(2, 3)
        board.set_piece(enemy2_square, enemy2)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert enemy1_square in moves
        assert enemy2_square in moves

    @staticmethod
    def test_white_pawns_cannot_move_diagonally_except_to_capture():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        pawn_square = Square.at(3, 4)
        board.set_piece(pawn_square, pawn)

        friendly = Pawn(Player.WHITE)
        friendly_square = Square.at(4, 5)
        board.set_piece(friendly_square, friendly)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(4, 3) not in moves
        assert Square.at(4, 5) not in moves

    @staticmethod
    def test_black_pawns_cannot_move_diagonally_except_to_capture():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        pawn_square = Square.at(3, 4)
        board.set_piece(pawn_square, pawn)

        friendly = Pawn(Player.BLACK)
        friendly_square = Square.at(2, 5)
        board.set_piece(friendly_square, friendly)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(2, 3) not in moves
        assert Square.at(2, 5) not in moves

    @staticmethod
    def test_white_pawn_changes_to_queen_when_moved_to_top_of_board():
        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        from_square = Square.at(6, 4)
        to_square = Square.at(7, 4)
        board.set_piece(from_square, pawn)
        board.move_piece(from_square, to_square)
        new_queen = board.get_piece(to_square)
        # Assert
        assert isinstance(new_queen, Queen)

    @staticmethod
    def test_black_pawn_changes_to_queen_when_moved_to_top_of_board():
        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        square = Square.at(1, 4)
        board.set_piece(square, pawn)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert len(moves) == 1

class TestRooks:

    @staticmethod
    def test_white_rooks_can_move_horizontally_right():

        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        square = Square.at(0, 0)
        board.set_piece(square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(0, 1) in moves
        assert Square.at(0, 5) in moves

    @staticmethod
    def test_white_rooks_can_move_vertically_up():

        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        square = Square.at(0, 0)
        board.set_piece(square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(1, 0) in moves
        assert Square.at(5, 0) in moves

    @staticmethod
    def test_black_rooks_can_move_horizontally_right():

        # Arrange
        board = Board.empty()
        rook = Rook(Player.BLACK)
        square = Square.at(0, 0)
        board.set_piece(square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(0, 1) in moves
        assert Square.at(0, 5) in moves

    @staticmethod
    def test_black_rooks_can_move_vertically_up():

        # Arrange
        board = Board.empty()
        rook = Rook(Player.BLACK)
        square = Square.at(0, 0)
        board.set_piece(square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(1, 0) in moves
        assert Square.at(5, 0) in moves

    @staticmethod
    def test_white_rooks_can_move_horizontally_left():

        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        square = Square.at(7, 7)
        board.set_piece(square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(7, 1) in moves
        assert Square.at(7, 5) in moves

    @staticmethod
    def test_white_rooks_can_move_vertically_down():

        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        square = Square.at(7, 7)
        board.set_piece(square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(1, 7) in moves
        assert Square.at(5, 7) in moves

    @staticmethod
    def test_black_rooks_can_move_horizontally_left():

        # Arrange
        board = Board.empty()
        rook = Rook(Player.BLACK)
        square = Square.at(7, 7)
        board.set_piece(square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(7, 1) in moves
        assert Square.at(7, 5) in moves

    @staticmethod
    def test_black_rooks_can_move_vertically_down():

        # Arrange
        board = Board.empty()
        rook = Rook(Player.BLACK)
        square = Square.at(7, 7)
        board.set_piece(square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert Square.at(1, 7) in moves
        assert Square.at(5, 7) in moves

    @staticmethod
    def test_white_rooks_cannot_move_if_piece_in_front():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(4, 4)
        board.set_piece(rook_square, rook)

        obstructing_square1 = Square.at(3, 4)
        obstruction = Pawn(Player.WHITE)
        board.set_piece(obstructing_square1, obstruction)

        obstructing_square2 = Square.at(5, 4)
        obstruction = Pawn(Player.WHITE)
        board.set_piece(obstructing_square2, obstruction)

        obstructing_square3 = Square.at(4, 3)
        obstruction = Pawn(Player.WHITE)
        board.set_piece(obstructing_square3, obstruction)

        obstructing_square3 = Square.at(4, 5)
        obstruction = Pawn(Player.WHITE)
        board.set_piece(obstructing_square3, obstruction)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert len(moves) == 0

    @staticmethod
    def test_black_rooks_cannot_move_if_piece_in_front():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.BLACK)
        rook_square = Square.at(4, 4)
        board.set_piece(rook_square, rook)

        obstructing_square1 = Square.at(3, 4)
        obstruction = Pawn(Player.BLACK)
        board.set_piece(obstructing_square1, obstruction)

        obstructing_square2 = Square.at(5, 4)
        obstruction = Pawn(Player.BLACK)
        board.set_piece(obstructing_square2, obstruction)

        obstructing_square3 = Square.at(4, 3)
        obstruction = Pawn(Player.BLACK)
        board.set_piece(obstructing_square3, obstruction)

        obstructing_square3 = Square.at(4, 5)
        obstruction = Pawn(Player.BLACK)
        board.set_piece(obstructing_square3, obstruction)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert len(moves) == 0

    @staticmethod
    def test_white_rooks_can_take_black_pieces_but_not_white():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        rook_square = Square.at(4, 4)
        board.set_piece(rook_square, rook)

        obstructing_square1 = Square.at(3, 4)
        obstruction = Pawn(Player.BLACK)
        board.set_piece(obstructing_square1, obstruction)

        obstructing_square2 = Square.at(5, 4)
        obstruction = Pawn(Player.WHITE)
        board.set_piece(obstructing_square2, obstruction)

        obstructing_square3 = Square.at(4, 3)
        obstruction = Pawn(Player.WHITE)
        board.set_piece(obstructing_square3, obstruction)

        obstructing_square3 = Square.at(4, 5)
        obstruction = Pawn(Player.BLACK)
        board.set_piece(obstructing_square3, obstruction)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert len(moves) == 2

    @staticmethod
    def test_black_rooks_can_take_white_pieces_but_not_black():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.BLACK)
        rook_square = Square.at(4, 4)
        board.set_piece(rook_square, rook)

        obstructing_square1 = Square.at(3, 4)
        obstruction = Pawn(Player.WHITE)
        board.set_piece(obstructing_square1, obstruction)

        obstructing_square2 = Square.at(5, 4)
        obstruction = Pawn(Player.BLACK)
        board.set_piece(obstructing_square2, obstruction)

        obstructing_square3 = Square.at(4, 3)
        obstruction = Pawn(Player.BLACK)
        board.set_piece(obstructing_square3, obstruction)

        obstructing_square3 = Square.at(4, 5)
        obstruction = Pawn(Player.WHITE)
        board.set_piece(obstructing_square3, obstruction)

        # Act
        moves = rook.get_available_moves(board)

        # Assert
        assert len(moves) == 2
