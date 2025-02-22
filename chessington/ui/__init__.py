"""
A GUI chess board that can be interacted with, and pieces moved around on.
"""

import os

import PySimpleGUI as psg
import time
from chessington.engine.board import Board, BOARD_SIZE
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Pawn, Knight, Bishop, Rook, Queen, King
from chessington.engine.chess_bot import ChessBotRandom, ChessBotDefense, ChessBotStronk, NuChessBotStronk

IMAGES_BASE_DIRECTORY = 'images'

BLACK_SQUARE_COLOUR = '#B58863'
WHITE_SQUARE_COLOUR = '#F0D9B5'
FROM_SQUARE_COLOUR = '#33A1FF'
TO_SQUARE_COLOUR = '#B633FF'

def get_image_name_from_piece(piece):
    if piece is None:
        return os.path.join(IMAGES_BASE_DIRECTORY, 'blank.png')
    class_to_piece_name = { Pawn: 'pawn', Knight: 'knight', Bishop: 'bishop', Rook: 'rook', Queen: 'queen', King: 'king' }
    player_to_colour_suffix = { Player.WHITE: 'w', Player.BLACK: 'b' }
    image_name = class_to_piece_name[piece.__class__] + player_to_colour_suffix[piece.player] + '.png'
    return os.path.join(IMAGES_BASE_DIRECTORY, image_name)

def get_key_from_square(square):
    return (square.row, square.col)

def get_square_colour(square):
    return BLACK_SQUARE_COLOUR if square.row % 2 == square.col % 2 else WHITE_SQUARE_COLOUR

def render_square(board, square):
    piece = board.get_piece(square)
    image_file = get_image_name_from_piece(piece)
    square_colour = get_square_colour(square)
    key = get_key_from_square(square)
    return psg.Button('', image_filename=image_file, size=(1, 1), button_color=('white', square_colour), pad=(0, 0), key=key)

def render_board(board):
    return [[render_square(board, Square.at(row, col)) for col in range(BOARD_SIZE)] for row in range(BOARD_SIZE - 1, -1, -1)] + [[psg.Button("Continue")]]

def update_pieces(window, board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            image_file = get_image_name_from_piece(board.get_piece(Square.at(row, col)))
            element = window.FindElement(key=(row, col))
            element.Update(image_filename=image_file)

def set_square_colour(window, square, colour):
    element = window.FindElement(key=(square.row, square.col))
    element.Update(button_color=('white', colour))

def reset_square_colours(window):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            colour = get_square_colour(Square.at(row, col))
            element = window.FindElement(key=(row, col))
            element.Update(button_color=('white', colour))

def highlight_squares(window, from_square, to_squares):
    reset_square_colours(window)
    if from_square is not None:
        set_square_colour(window, from_square, FROM_SQUARE_COLOUR)
    for square in to_squares:
        set_square_colour(window, square, TO_SQUARE_COLOUR)



def play_game():
    psg.ChangeLookAndFeel('GreenTan')

    board = Board.at_starting_position()
    board_layout = render_board(board)
    window = psg.Window('Chessington', default_button_element_size=(12, 1), auto_size_buttons=False).Layout(board_layout)

    from_square = None
    to_squares = []

    def handle_click(row, col):

        nonlocal window, board, from_square, to_squares
        clicked_piece = board.get_piece(Square.at(row, col))

        # If making an allowed move, then make it
        if from_square is not None and any(s.row == row and s.col == col for s in to_squares):
            board.get_piece(from_square).move_to(board, Square.at(row, col))
            from_square, to_squares = None, []

        # If clicking on a piece whose turn it is, get its allowed moves
        elif clicked_piece is not None and clicked_piece.player == board.current_player:
            from_square = Square.at(row, col)
            to_squares = clicked_piece.get_available_moves(board)

        # Otherwise reset everthing to default
        else:
            from_square, to_squares = None, []

    # def activate_bot(window, board, , ):
    #     move = ChessBotStronk().do_smart_move(board)
    #     handle_click(*move[0])
    #     highlight_squares(window, from_square, to_squares)
    #     update_pieces(window, board)
    #
    #     button, _ = window.Read()
    #     if button is not None:
    #         handle_click(*move[1])
    #         highlight_squares(window, from_square, to_squares)
    #         update_pieces(window, board)
    button, _ = window.Read()
    while True:
        counter = 0
        if board.current_player == Player.WHITE:
            '''
            Bot code
            '''
            player = Player.WHITE
            opponent = Player.BLACK
            move = ChessBotStronk(player, opponent).get_move(board)
            if move is not None:
                handle_click(*move[0])
                highlight_squares(window, from_square, to_squares)
                button, _ = window.Read(timeout=40)
                # if button is not None:
                handle_click(*move[1])
                highlight_squares(window, from_square, to_squares)
                update_pieces(window, board)
            else:
                button, _ = window.Read()

            '''
            Player code
            '''
            # button, _ = window.Read()
            # if button is not None:
            #     handle_click(*button)
            # highlight_squares(window, from_square, to_squares)
            # update_pieces(window, board)

        if board.current_player == Player.BLACK:
            """
            Bot code
            """
            player = Player.BLACK
            opponent = Player.WHITE
            move = NuChessBotStronk(player, opponent).get_move(board)
            if move is not None:
                handle_click(*move[0])
                highlight_squares(window, from_square, to_squares)
                button, _ = window.Read(timeout=40)
                # if button is not None:
                handle_click(*move[1])
                highlight_squares(window, from_square, to_squares)
                update_pieces(window, board)
            else:
                button, _ = window.Read()

        # Update the UI
        highlight_squares(window, from_square, to_squares)
        update_pieces(window, board)

