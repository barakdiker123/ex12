import numpy as np
import functools


class Board:
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

    def __init__(self):
        self.__board = np.zeros((Board.ROWS, Board.COLUMNS), dtype=np.int8)
        # Boolean list which start at true
        # In Python 1 is True and 0 is False
        self.__possible_moves = np.ones(Board.COLUMNS, dtype=np.bool)

    @property
    def possible_moves(self):
        return self.__possible_moves

    @property
    def board(self):
        return self.__board

    def update_possible_moves(self):
        "This function update the list self.__possible_moves "
        for i, value in enumerate(self.__board[0]):
            if value != Board.EMPTY:
                self.possible_moves[i] = False

    @staticmethod
    def __find_first_non_empty(arr):
        for i, ele in enumerate(arr):
            if ele != Board.EMPTY:
                return i
        return Board.NOT_FOUND  # if not found

    def update_board(self, column, current_turn):
        """
        This function adds disk to the board
        :param board: np.array
        :param column: the column the player chose (int)
        :param current_turn: CONST
        :return: None if can't add ,else the board itself
        """
        Board.check_location(column=column)
        # Full column
        if self.__board[0, column] != 0:
            return Board.FAILED, Board.NOT_FOUND, Board.NOT_FOUND
        # Scan the column
        column_data = self.__board[:, column]
        # This function return Game.NOT_FOUND if not found
        item_index = Board.__find_first_non_empty(column_data)
        if item_index == Board.NOT_FOUND:
            current_turn = np.int8(current_turn)
            self.__board[Board.ROWS - 1, column] = current_turn
            return Board.SUCCESS, Board.ROWS - 1, column
        else:
            current_turn = np.int8(current_turn)
            self.__board[item_index - 1, column] = current_turn
            return Board.SUCCESS, item_index - 1, column

    def check_if_draw(self):
        self.update_possible_moves()
        return not functools.reduce(lambda x, y: x or y, self.__possible_moves)

    def check_win_in_point(self, x, y, player):
        """
        Searchs for victory in current turn
        :param board:
        :param x:
        :param y:
        :param player: Game.BLACK or Game.WHITE
        :return:
        """
        column = self.__board[:, y]
        if Board.__search_for_victory(column, player):
            return Board.WINNER_DICT[player]

        row = self.__board[x, :]
        if Board.__search_for_victory(row, player):
            return Board.WINNER_DICT[player]

        main_slant = self.__create_main_slant(x, y)
        if Board.__search_for_victory(main_slant, player):
            return Board.WINNER_DICT[player]

        secondry_slant = self.__create_secondry_slant(x, y)
        if Board.__search_for_victory(secondry_slant, player):
            return Board.WINNER_DICT[player]
        return Board.GAME_IN_PROGRESS

    def __create_main_slant(self, x, y):
        arr = []
        index_x = x
        index_y = y
        while Board.is_in_board(index_x, index_y):
            arr.append(self.__board[index_x, index_y])
            index_x += 1
            index_y += 1

        index_x = x - 1
        index_y = y - 1
        while Board.is_in_board(index_x, index_y):
            arr.insert(0, self.__board[index_x, index_y])
            index_x -= 1
            index_y -= 1
        arr = np.array(arr)
        return arr

    def __create_secondry_slant(self, x, y):
        arr = []
        index_x = x
        index_y = y
        while Board.is_in_board(index_x, index_y):
            arr.append(self.__board[index_x, index_y])
            index_x += 1
            index_y -= 1

        index_x = x - 1
        index_y = y + 1
        while Board.is_in_board(index_x, index_y):
            arr.insert(0, self.__board[index_x, index_y])
            index_x -= 1
            index_y += 1
        arr = np.array(arr)
        return arr

    @staticmethod
    def __search_for_victory(one_dimension_arr, player):
        one_dimension_arr = one_dimension_arr.astype(str)
        one_dimension_arr = ''.join(one_dimension_arr)
        if Board.GET_WIN_SEQ[player] in one_dimension_arr:
            return True
        return False

    @staticmethod
    def check_location(row=0, column=0):
        if not 0 <= column < Board.COLUMNS or not 0 <= row < Board.ROWS:
            raise Exception("Illegal location")

    @staticmethod
    def is_in_board(row, column):
        if 0 <= row < Board.ROWS and 0 <= column < Board.COLUMNS:
            return True
        return False
