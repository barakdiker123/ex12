import numpy as np
from ex12.game import Game
import random


class NoPossibleMovesAI(Exception):
    def __init__(self):
        super().__init__('No possible AI moves.')


class AI:
    WHITE = np.int8(1)
    BLACK = np.int8(2)
    EMPTY = np.int8(0)

    WHO_GO_FIRST = WHITE

    GAME_IN_PROGRESS = None
    WHITE_WINS = 1
    BLACK_WINS = 2
    TIE = 0

    WINNER_DICT = {WHITE: WHITE_WINS,
                   BLACK: BLACK_WINS}

    ROWS = 6
    COLUMNS = 7

    NOT_FOUND = -1
    FAILED = -1
    SUCCESS = -2

    WHITE_WINS_SEQ = '1111'
    BLACK_WINS_SEQ = '2222'

    GET_WIN_SEQ = {WHITE: WHITE_WINS_SEQ,
                   BLACK: BLACK_WINS_SEQ}

    def __init__(self, game, player):
        """
        initiation
        :param game: object Game
        :param player:  Game.WHITE , Game.BLACK
        """
        self.__game = game
        self.__player = player
        # In Boolean Form [1 1 1 1 1] means all possible ->
        self.__possible_moves = np.ones(Game.COLUMNS, dtype=np.bool)
        self.__board = np.zeros((Game.ROWS, Game.COLUMNS), dtype=np.int8)
        self.update_board_in_numpy_array()
#Code duplicate due to requirement
#############################################################################################
#############################################################################################
#############################################################################################
    @staticmethod
    def check_win_in_point(board, x, y, player):
        """
        Searchs for victory in current turn
        :param board:
        :param x:
        :param y:
        :param player: Game.BLACK or Game.WHITE
        :return:
        """
        column = board[:, y]
        if Game.__search_for_victory(column, player):
            return Game.WINNER_DICT[player]

        row = board[x, :]
        if Game.__search_for_victory(row, player):
            return Game.WINNER_DICT[player]

        main_slant = Game.__create_main_slant(board, x, y)
        if Game.__search_for_victory(main_slant, player):
            return Game.WINNER_DICT[player]

        secondry_slant = Game.__create_secondry_slant(board, x, y)
        if Game.__search_for_victory(secondry_slant, player):
            return Game.WINNER_DICT[player]
        return Game.GAME_IN_PROGRESS

    @staticmethod
    def __create_main_slant(board, x, y):
        arr = []
        index_x = x
        index_y = y
        while Game.is_in_board(index_x, index_y):
            arr.append(board[index_x, index_y])
            index_x += 1
            index_y += 1

        index_x = x - 1
        index_y = y - 1
        while Game.is_in_board(index_x, index_y):
            arr.insert(0, board[index_x, index_y])
            index_x -= 1
            index_y -= 1
        arr = np.array(arr)
        return arr

    @staticmethod
    def __create_secondry_slant(board, x, y):
        arr = []
        index_x = x
        index_y = y
        while Game.is_in_board(index_x, index_y):
            arr.append(board[index_x, index_y])
            index_x += 1
            index_y -= 1

        index_x = x - 1
        index_y = y + 1
        while Game.is_in_board(index_x, index_y):
            arr.insert(0, board[index_x, index_y])
            index_x -= 1
            index_y += 1
        arr = np.array(arr)
        return arr

    @staticmethod
    def __search_for_victory(one_dimension_arr, player):
        one_dimension_arr = one_dimension_arr.astype(str)
        one_dimension_arr = ''.join(one_dimension_arr)
        if Game.GET_WIN_SEQ[player] in one_dimension_arr:
            return True
        return False

    @staticmethod
    def check_location(row=0, column=0):
        if not 0 <= column < Game.COLUMNS or not 0 <= row < Game.ROWS:
            raise Exception("Illegal location")

    @staticmethod
    def is_in_board(row, column):
        if 0 <= row < Game.ROWS and 0 <= column < Game.COLUMNS:
            return True
        return False
#############################################################################################
#############################################################################################
#############################################################################################
    def is_game_over(self):
        "This function return False if the game is not over"
        for i in range(Game.ROWS):
            for j in range(Game.COLUMNS):
                if Game.check_win_in_point(self.__board, i, j, Game.WHITE) != Game.GAME_IN_PROGRESS:
                    return True
                if Game.check_win_in_point(self.__board, i, j, Game.BLACK) != Game.GAME_IN_PROGRESS:
                    return True
        return False

    def update_board_in_numpy_array(self):
        """
        This function update the board into numpy array
        this is good for memory effiency (explain in README)
        :return:
        """
        for i in range(Game.ROWS):
            for j in range(Game.COLUMNS):
                if self.__game.get_player_at(i, j) is None:
                    self.__board[i, j] = Game.EMPTY
                else:
                    self.__board[i, j] = np.int8(self.__game.get_player_at(i, j))

    def list_of_moves(self):
        """
        This function get all possible moves
        :return: lst of all possible moves
        """
        lst = []
        for i, ele in enumerate(self.__possible_moves):
            if ele:
                lst.append(i)
        return lst

    def find_legal_move(self, timeout=None):
        """
        This function the program recommend the user
        what should he play
        :param timeout:
        :return: integer from 0 to Game.COLUMNS
        """
        # Checks if the game has finished
        if self.is_game_over():
            raise NoPossibleMovesAI
        Game.update_possible_moves(self.__board, self.__possible_moves)
        if Game.check_if_draw(self.__possible_moves):
            raise NoPossibleMovesAI
        #
        # return a random of possible choices
        return random.choice(self.list_of_moves())

    def get_last_found_move(self):
        pass
