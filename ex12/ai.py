import numpy as np
from ex12.board import Board
import random


class NoPossibleMovesAI(Exception):
    def __init__(self):
        super().__init__('No possible AI moves.')


class AI:
    def __init__(self, game, player):
        """
        initiation
        :param game: object Game
        :param player:  AI.WHITE , AI.BLACK
        """
        self.__game = game
        self.__player = player
        # In Boolean Form [1 1 1 1 1] means all possible ->
        self.__board_instance = Board()
        self.update_board_in_numpy_array()

    def is_game_over(self):
        "This function return False if the AI is not over"
        for i in range(Board.ROWS):
            for j in range(Board.COLUMNS):
                if self.__board_instance.check_win_in_point(i, j, Board.WHITE) != Board.GAME_IN_PROGRESS:
                    return True
                if self.__board_instance.check_win_in_point(i, j, Board.BLACK) != Board.GAME_IN_PROGRESS:
                    return True
        return False

    def update_board_in_numpy_array(self):
        """
        This function update the board into numpy array
        this is good for memory effiency (explain in README)
        :return:
        """
        for i in range(Board.ROWS):
            for j in range(Board.COLUMNS):
                if self.__game.get_player_at(i, j) is None:
                    self.__board_instance.board[i, j] = Board.EMPTY
                else:
                    self.__board_instance.board[i, j] = np.int8(self.__game.get_player_at(i, j))

    def list_of_moves(self):
        """
        This function get all possible moves
        :return: lst of all possible moves
        """
        lst = []
        for i, ele in enumerate(self.__board_instance.possible_moves):
            if ele:
                lst.append(i)
        return lst

    def find_legal_move(self, timeout=None):
        """
        This function the program recommend the user
        what should he play
        :param timeout:
        :return: integer from 0 to AI.COLUMNS
        """
        # Checks if the AI has finished
        if self.is_game_over():
            raise NoPossibleMovesAI
        self.__board_instance.update_possible_moves()
        if self.__board_instance.check_if_draw():
            raise NoPossibleMovesAI
        #
        # return a random of possible choices
        return random.choice(self.list_of_moves())

    def get_last_found_move(self):
        pass
