import numpy as np
import functools


class Game:
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
        self.__current_turn = Game.WHO_GO_FIRST
        self.__winner = Game.GAME_IN_PROGRESS
        self.__board = np.zeros((Game.ROWS, Game.COLUMNS), dtype=np.int8)
        # Boolean list which start at true
        # In Python 1 is True and 0 is False
        self.__possible_moves = np.ones(Game.COLUMNS, dtype=np.bool)

    def is_game_over(self):
        if self.__winner != Game.GAME_IN_PROGRESS:
            return False
        else:
            return True

    def __str__(self):
        return str(self.__board)

    @staticmethod
    def __update_possible_moves(board, possible_moves):
        "This function update the list self.__possible_moves "
        for i, value in enumerate(board[0]):
            if value != Game.EMPTY:
                possible_moves[i] = False

    @staticmethod
    def __find_first_non_empty(arr):
        for i, ele in enumerate(arr):
            if ele != Game.EMPTY:
                return i
        return Game.NOT_FOUND  # if not found

    @staticmethod
    def __update_board(board, column, current_turn):
        """
        This function adds disk to the board
        :param board: np.array
        :param column: the column the player chose (int)
        :param current_turn: CONST
        :return: None if can't add ,else the board itself
        """
        Game.check_location(column=column)
        # Full column
        if board[0, column] != 0:
            return Game.FAILED, Game.NOT_FOUND, Game.NOT_FOUND
        # Scan the column
        column_data = board[:, column]
        # This function return Game.NOT_FOUND if not found
        item_index = Game.__find_first_non_empty(column_data)
        if item_index == Game.NOT_FOUND:
            current_turn = np.int8(current_turn)
            board[Game.ROWS - 1, column] = current_turn
            return Game.SUCCESS, Game.ROWS - 1, column
        else:
            current_turn = np.int8(current_turn)
            board[item_index - 1, column] = current_turn
            return Game.SUCCESS, item_index - 1, column

    def flip_color(self):
        """
        Change the color
        :return:
        """
        if self.__current_turn == Game.WHITE:
            self.__current_turn = Game.BLACK
            return
        if self.__current_turn == Game.BLACK:
            self.__current_turn = Game.WHITE
            return

    def check_if_draw(self):
        return not functools.reduce(lambda x, y: x or y, self.__possible_moves)

    def make_move(self, column):
        Game.check_location(column=column)
        if self.__winner != Game.GAME_IN_PROGRESS:
            raise Exception("Illegal location")
        if not self.__possible_moves[column]:
            raise Exception("Illegal location")
        is_success, x, y = self.__update_board(self.__board, column, self.__current_turn)
        if is_success == Game.FAILED:
            raise Exception("Illegal location")
        self.__update_possible_moves(self.__board, self.__possible_moves)

        self.__winner = Game.check_win_in_point(self.__board, x, y, self.__current_turn)

        if self.check_if_draw():
            self.__winner = Game.TIE

        self.flip_color()

    def get_winner(self):
        return self.__winner

    def get_player_at(self, row, col):
        """
        This function checks position in the board
        :return: None if position empty , 1 if white , 2 if black
        """
        Game.check_location(row=row, column=col)
        if self.__board[row, col] == Game.WHITE:
            return Game.WHITE
        if self.__board[row, col] == Game.BLACK:
            return Game.BLACK
        if self.__board[row, col] == Game.EMPTY:
            return None

    def get_current_player(self):
        return self.__current_turn

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

    @property
    def winner(self):
        return self.__winner

    @property
    def current_player(self):
        return self.__current_turn

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, new_board):
        self.__board = new_board

    @property
    def possible_moves(self):
        return self.__possible_moves



