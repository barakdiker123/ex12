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

    ROWS = 6
    COLUMNS = 7

    NOT_FOUND = -1
    FAILED = -1
    SUCCESS = -2

    def __init__(self):
        self.__current_turn = Game.WHO_GO_FIRST
        self.__winner = Game.GAME_IN_PROGRESS
        self.__board = np.ones((Game.ROWS, Game.COLUMNS), dtype=np.int8)
        # Boolean list which start at true
        # In Python 1 is True and 0 is False
        self.__possible_moves = np.zeros(Game.COLUMNS, dtype=np.bool)

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
            return Game.FAILED
        # Scan the column
        column_data = board[:, column]
        # This function return Game.NOT_FOUND if not found
        item_index = np.where(np.logical_or(column_data == Game.BLACK,
                                            column_data == Game.WHITE))
        if item_index[0].size == 0:
            board[Game.ROWS - 1, column] = current_turn
            return Game.SUCCESS
        board[item_index[0] - 1, column] = current_turn
        return Game.SUCCESS

    def flip_color(self):
        """
        Change the color
        :return:
        """
        if self.__current_turn == Game.WHITE:
            self.__current_turn = Game.BLACK
        if self.__current_turn == Game.BLACK:
            self.__current_turn = Game.WHITE

    def check_if_draw(self):
        return not functools.reduce(lambda x, y: x or y, self.__possible_moves)

    def make_move(self, column):
        Game.check_location(column=column)
        if not self.__possible_moves[column]:
            raise Exception("Illegal location")
        if self.__update_board(self.__board, column, self.__current_turn) == Game.FAILED:
            raise Exception("Illegal location")
        self.flip_color()
        self.__update_possible_moves(self.__board, self.__possible_moves)
        if self.check_if_draw():
            self.__winner = Game.TIE
        #Scan New Diagonal

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
    def check_location(row=0, column=0):
        if not 0 <= column < Game.COLUMNS or not 0 <= row < Game.ROWS:
            raise Exception("Illegal location")

    @property
    def winner(self):
        return self.__winner

    @property
    def current_player(self):
        return self.__current_turn

    @property
    def board(self):
        return self.__board

    @property
    def possible_moves(self):
        return self.__possible_moves


game1 = Game()
# for i in range(4):
#     game1.make_move(3)
game1.board[0, 0] = Game.EMPTY
game1.board[1, 0] = Game.EMPTY
game1.make_move(0)
print(game1.possible_moves)
print(game1)
