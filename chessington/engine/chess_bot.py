import random
import copy
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Queen, King, Knight, Rook, Bishop, Pawn


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
        enemy_pieces_squares = self.get_enemy_locations(board)
        death_squares = self.get_death_squares(board, enemy_pieces_squares)
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
        enemy_pieces_squares = []
        for square_row in range(8):
            for square_col in range(8):
                selected_square = Square.at(square_row, square_col)
                if self.check_enemy_piece(board, selected_square):
                    enemy_pieces_squares.append(selected_square)
        return enemy_pieces_squares

    def get_death_squares(self, board, enemy_pieces_squares):
        """
        Get all squares enemy pieces can move into
        """
        death_squares = []
        for square in enemy_pieces_squares:
            death_squares += board.get_piece(square).get_available_moves(board)
        return death_squares

    def check_death_square(self, death_squares, selected_move):
        return selected_move in death_squares


class ChessBotStronk:
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent

    def do_smart_move(self, board):
        desired_board_state = self.get_desired_board_state(board)
        from_square = desired_board_state.next_move[0]
        to_square = desired_board_state.next_move[1]
        # board.get_piece(from_square).move_to(board, to_square)
        return from_square, to_square

    def get_desired_board_state(self, board):
        future_board_states = self.get_future_board_states(board)
        # for future_board_state in future_board_states:
        #     future_board_states_lvl2 = self.get_future_board_states(future_board_state)
        #     future_board_state.value += max(future_board_states_lvl2, key=lambda f: f.value).value
        return max(future_board_states, key=lambda f: f.value)

    def get_future_board_states(self, board):
        future_board_state_list = []
        # for every available move
        bot_pieces_squares = self.get_bot_locations(board)
        for from_square in bot_pieces_squares:
            bot_piece_available_move_squares = self.get_bot_square_moves(board, from_square)
            for to_square in bot_piece_available_move_squares:
                future_board_state_list.append(self.get_new_board_state(board, from_square, to_square))
        return future_board_state_list

    def get_new_board_state(self, board, from_square, to_square):
        new_board_state = copy.deepcopy(board)
        new_board_state.next_move = [from_square, to_square]
        new_board_state.get_piece(from_square).move_to(new_board_state, to_square)
        new_board_state.value = self.value_assign(new_board_state) + random.random() / 2  # TODO
        return new_board_state

    def value_assign(self, new_board_state):
        """
        assign the value of the new board state by counting if
        a piece is taken by the bot or if pieces can be taken by the player
        """
        enemy_squares = self.get_enemy_locations(new_board_state)
        bot_squares = self.get_bot_locations(new_board_state)
        bad_death_squares = self.get_death_squares(new_board_state, enemy_squares)
        good_death_squares = self.get_death_squares(new_board_state, bot_squares)
        death_square_value = - 4 * self.piece_ranking(new_board_state, bad_death_squares, 30)
        death_square_value += 2 * self.piece_ranking(new_board_state, good_death_squares, random.randint(8, 12))
        living_pieces_value = - 2 * self.piece_ranking(new_board_state, enemy_squares, random.randint(12, 15))
        living_pieces_value += 4 * self.piece_ranking(new_board_state, bot_squares, 30)
        value = living_pieces_value + death_square_value
        return value

    def piece_ranking(self, board, squares, check_rank):
        value = 0
        for square in squares:
            piece = board.get_piece(square)
            if isinstance(piece, King):
                value += check_rank
            if isinstance(piece, Queen):
                value += random.randint(6, 12)
            if isinstance(piece, Bishop):
                value += random.randint(4, 10)
            if isinstance(piece, Knight):
                value += random.randint(4, 10)
            if isinstance(piece, Rook):
                value += random.randint(4, 10)
            if isinstance(piece, Pawn):
                value += random.randint(2, 6)
        return value

    def check_valid_piece(self, board, selected_square):
        if board.is_square_empty(selected_square):
            return False
        return board.get_piece(selected_square).player == self.player

    def check_enemy_piece(self, board, selected_square):
        if board.is_square_empty(selected_square):
            return False
        return board.get_piece(selected_square).player == self.opponent

    def get_bot_locations(self, board):
        bot_pieces_squares = []
        for square_row in range(8):
            for square_col in range(8):
                selected_square = Square.at(square_row, square_col)
                if self.check_valid_piece(board, selected_square):
                    bot_pieces_squares.append(selected_square)
        return bot_pieces_squares

    def get_bot_square_moves(self, board, square):
        return board.get_piece(square).get_available_moves(board)

    def get_enemy_locations(self, board):
        """
        Get all squares containing enemy pieces
        """
        enemy_pieces_squares = []
        for square_row in range(8):
            for square_col in range(8):
                selected_square = Square.at(square_row, square_col)
                if self.check_enemy_piece(board, selected_square):
                    enemy_pieces_squares.append(selected_square)
        return enemy_pieces_squares

    def get_death_squares(self, board, enemy_pieces_squares):
        """
        Get all squares enemy pieces can move into
        """
        death_squares = []
        for square in enemy_pieces_squares:
            death_squares += board.get_piece(square).get_available_moves(board)
        return death_squares

    def check_death_square(self, death_squares, selected_move):
        return selected_move in death_squares
