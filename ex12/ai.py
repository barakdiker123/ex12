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
    ALL_POSSIBILITIES = 16
    WEIGH_POSSIBILITIES = 30
    WEIGH_AVOID_SECOND_ADD_WINNING = -100
    WEIGH_LOSING_FOR_SURE = -1000

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
        for move in self.list_of_moves():
            self.dict_move[move] = 0

    def is_game_over(self):
        "This function return False if the AI is not over"
        for i in range(Board.ROWS):
            for j in range(Board.COLUMNS):
                if self.__board_instance.check_win_in_point(i, j, Board.WHITE) \
                        != Board.GAME_IN_PROGRESS:
                    return True
                if self.__board_instance.check_win_in_point(i, j, Board.BLACK) \
                        != Board.GAME_IN_PROGRESS:
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

    def search_for_win_in_one_move(self):
        """
        return the number of the winning column in one
        if not found , return Board.NOT_FOUND = -1
        :return:
        """
        for column in self.list_of_moves():
            flag, x, y = self.__temp_board.update_board(column, self.__player)
            if self.__temp_board.check_win_in_point(x, y, self.__player):
                return column
            self.__temp_board.board[x, y] = Board.EMPTY
        return Board.NOT_FOUND

    def evaluate_via_centralize_point(self):
        """
        Using The sum_all_possibilities(player,x,y) from Board
        we gave grade to each move
        :return: update the self.dict_move
        """
        for column in self.list_of_moves():
            flag, x, y = self.__temp_board.update_board(column, self.__player)
            ratio = self.__temp_board.sum_all_possibilities(self.__player, x, y) / AI.ALL_POSSIBILITIES
            evaluation = ratio * AI.WEIGH_POSSIBILITIES
            self.dict_move[column] += evaluation
            self.__temp_board.board[x, y] = Board.EMPTY

    def evaluate_via_avoid_second_add_winning(self):
        """
        If adding 2 disk to certain column cause winning than
        avoid adding to column
        :return: update the self.dict_move
        """
        for column in self.list_of_moves():
            if self.__temp_board.you_can_add_two_or_more_disk(column):
                temp_player = Board.flip_color(self.__player)
                # add 2 disks
                self.__temp_board.update_board(column, temp_player)
                flag, x, y = self.__temp_board.update_board(column, self.__player)
                #
                if self.__temp_board.check_win_in_point(x, y, self.__player):
                    # Should decrease the value
                    self.dict_move[column] += AI.WEIGH_AVOID_SECOND_ADD_WINNING
                self.__temp_board.board[x, y] = Board.EMPTY  # init the higher
                self.__temp_board.board[x + 1, y] = Board.EMPTY  # 1 init below the higher

    def evaluate_via_avoid_second_add_losing(self):
        """
        If I add disk and my opponent add disk to the same column
        and I am losing for sure
        :return: update the self.dict_move
        """
        for column in self.list_of_moves():
            if self.__temp_board.you_can_add_two_or_more_disk(column):
                temp_player = Board.flip_color(self.__player)
                # add 2 disks
                self.__temp_board.update_board(column, self.__player)
                flag, x, y = self.__temp_board.update_board(column, temp_player)
                #
                if self.__temp_board.check_win_in_point(x, y, temp_player):
                    # Should decrease the value
                    self.dict_move[column] += AI.WEIGH_LOSING_FOR_SURE
                self.__temp_board.board[x, y] = Board.EMPTY  # init the higher
                self.__temp_board.board[x + 1, y] = Board.EMPTY  # 1 init below the higher

    def evaluate(self):
        """
        This function try to evaluate the situation on the board
        and based on our functions try to find the best move
        :return: update the self.dict_move
        """
        self.evaluate_via_centralize_point()
        self.evaluate_via_avoid_second_add_losing()
        self.evaluate_via_avoid_second_add_winning()

    def fast_algorithm(self):
        column_winning = self.search_for_win_in_one_move()
        if column_winning != Board.NOT_FOUND:
            return column_winning
        self.evaluate()
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
