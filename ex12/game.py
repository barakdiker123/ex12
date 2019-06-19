import numpy as np
import functools
from ex12.board import Board

class Game:
    GAME_IN_PROGRESS = None
    WHITE_WINS = 1
    BLACK_WINS = 2
    TIE = 0

    def __init__(self):
        self.__current_turn = Board.WHO_GO_FIRST
        self.__winner = Board.GAME_IN_PROGRESS
        self.__board_instance = Board()
        # Boolean list which start at true
        # In Python 1 is True and 0 is False

    def is_game_over(self):
        if self.__winner != Board.GAME_IN_PROGRESS:
            return False
        else:
            return True

    def __str__(self):
        return str(self.__board_instance.board)

    def flip_color(self):
        """
        Change the color
        :return:
        """
        if self.__current_turn == Board.WHITE:
            self.__current_turn = Board.BLACK
            return
        if self.__current_turn == Board.BLACK:
            self.__current_turn = Board.WHITE
            return

    def make_move(self, column):
        """
        Select a Column you want to insert into
        and update self.board
        :param column:
        :return:
        """
        Board.check_location(column=column)
        if self.__winner != Board.GAME_IN_PROGRESS:
            raise Exception("Illegal move.")
        if not self.__board_instance.possible_moves[column]:
            raise Exception("Illegal move.")
        is_success, x, y = self.__board_instance.update_board(column, self.__current_turn)
        if is_success == Board.FAILED:
            raise Exception("Illegal move.")
        self.__board_instance.update_possible_moves()

        self.__winner = self.__board_instance.check_win_in_point(x, y, self.__current_turn)

        if self.__board_instance.check_if_draw():
            self.__winner = Board.TIE

        self.flip_color()
        return x, y

    def get_winner(self):
        """
        if tie has won return the value Game.TIE
        if White has won return the value Game.WHITE_WINS
        if Black has won return the value Game.BLACK_WINS
        if non of the parties has won the game return Game.GAME_IN_PROGRESS
        :return: one of the up constants
        """
        return self.__winner

    def get_player_at(self, row, col):
        """
        This function checks position in the board
        :return: None if position empty , 1 if white , 2 if black
        """
        Board.check_location(row=row, column=col)
        if self.__board_instance.board[row, col] == Board.WHITE:
            return Board.WHITE
        if self.__board_instance.board[row, col] == Board.BLACK:
            return Board.BLACK
        if self.__board_instance.board[row, col] == Board.EMPTY:
            return None

    def get_current_player(self):
        """
        returns the players that now plays
        :return: Board.WHITE or Board.BLACK
        """
        return self.__current_turn

    @staticmethod
    def is_in_board(row, column):
        if 0 <= row < Board.ROWS and 0 <= column < Board.COLUMNS:
            return True
        return False

    @property
    def board(self):
        return self.__board_instance.board

