import numpy as np
from ex12.board import Board
import random
import copy


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
        self.__temp_board = copy.deepcopy(self.__board_instance)
        # get all valid move into eval_dict
        self.__temp_board.update_possible_moves()
        self.dict_move = {}
        for move in self.__board_instance.possible_moves:
            self.dict_move[move] = 0

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

    def instant_algorithm(self):
        return random.choice(self.list_of_moves())

    def fast_algorithm(self):
        for column in self.__board_instance.possible_moves:
            flag, x, y = self.__temp_board.update_board(column, self.__player)
            if self.__temp_board.check_win_in_point(x, y, self.__player):
                self.dict_move[column] += 100
        return AI.key_with_max_val(self.dict_move)

    @staticmethod
    def key_with_max_val(dic):
        """ a) create a list of the dict's keys and values;
            b) return the key with the max value"""
        values = list(dic.values())
        keys = list(dic.keys())
        return keys[values.index(max(values))]

    def backtrack_helper(self):
        pass

    def medium_algorithm(self):
        pass

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
        return self.instant_algorithm()

    def get_last_found_move(self):
        pass
