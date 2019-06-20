import numpy as np
from ex12.board import Board
import random
import copy


class NoPossibleMovesAI(Exception):
    def __init__(self):
        super().__init__('No possible AI moves.')


class AI:
    INSTANT_ALGORITHM_TIMEOUT = -1
    FAST_ALGORITHM_TIMEOUT = -2

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
        # get all valid move into eval_dict
        self.__board_instance.update_possible_moves()

        self.dict_move = {}
        for move in self.__board_instance.list_of_moves():
            self.dict_move[move] = 0

    def is_game_over(self):
        "This function return False if the AI is not over"
        for i in range(Board.ROWS):
            for j in range(Board.COLUMNS):
                if self.__board_instance.check_win_in_point(i, j, Board.WHITE) \
                        is not Board.GAME_IN_PROGRESS:
                    return True
                if self.__board_instance.check_win_in_point(i, j, Board.BLACK) \
                        is not Board.GAME_IN_PROGRESS:
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

    def instant_algorithm(self):
        return random.choice(self.__board_instance.list_of_moves())

    def fast_algorithm(self):
        column_winning = self.__board_instance.search_for_win_in_one_move(self.__player)
        if column_winning != Board.NOT_FOUND:
            return column_winning
        column_winning = self.__board_instance.search_for_win_in_one_move(Board.flip_color(self.__player))
        if column_winning != Board.NOT_FOUND:
            return column_winning
        self.__board_instance.evaluate(self.__player, self.dict_move)
        print(self.dict_move)
        return AI.key_with_max_val(self.dict_move)

    @staticmethod
    def key_with_max_val(dic):
        """ a) create a list of the dict's keys and values;
            b) return the key with the max value"""
        values = list(dic.values())
        keys = list(dic.keys())
        return keys[values.index(max(values))]

    def backtrack_helper(self, depth_temp, player, DEPTH):
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
        if timeout == AI.INSTANT_ALGORITHM_TIMEOUT:
            return self.instant_algorithm()
        if timeout == AI.FAST_ALGORITHM_TIMEOUT:
            return self.fast_algorithm()

    def get_last_found_move(self):
        pass


from ex12.game import Game


class Wipe(object):
    def __repr__(self):
        return '\n' * 1000


def check_win(game):
    if game.get_winner() == game.WHITE_WINS:
        print("The AI has won you easily!")
    if game.get_winner() == game.BLACK_WINS:
        print("You have done the impossible you won the AI!!")
    if game.get_winner() == game.TIE:
        print("TIE!")


wipe = Wipe()
if __name__ == "__main__":
    game = Game()
    while True:
        Wipe()
        check_win(game)
        ai = AI(game, Board.WHITE)
        column_cal = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
        print("Computer played: %s" % column_cal)
        game.make_move(column_cal)
        check_win(game)
        print(game)
        print("-----------------")
        print("<<0 1 2 3 4 5 6>>")
        try_again = True
        while try_again:
            col = int(input("Enter Your move:"))
            try:
                game.make_move(col)
                try_again = False
            except Exception:
                Wipe()
                print("Computer played: %s" % column_cal)
                print("Invalid Move")
                print(game)
                print("-----------------")
                print("<<0 1 2 3 4 5 6>>")
                try_again = True
