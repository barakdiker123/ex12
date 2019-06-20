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
    # AI constant used for evaluation
    ALL_POSSIBILITIES = 16
    WEIGH_POSSIBILITIES = 30
    WEIGH_AVOID_SECOND_ADD_WINNING = -100
    WEIGH_LOSING_FOR_SURE = -10000
    WEIGH_WINNING = 50

    #
    def __init__(self):
        self.__board = np.zeros((Board.ROWS, Board.COLUMNS), dtype=np.int8)
        # Boolean list which start at true
        # In Python 1 is True and 0 is False
        self.__possible_moves = np.ones(Board.COLUMNS, dtype=np.bool)

    def __str__(self):
        return str(self.__board)

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

    def __find_first_non_empty_helper(self, column):
        column_data = self.__board[:, column]
        for i, ele in enumerate(column_data):
            if ele != Board.EMPTY:
                return i
        return Board.NOT_FOUND  # if not found

    def find_first_non_empty(self, column):
        item_index = self.__find_first_non_empty_helper(column)
        if item_index == Board.NOT_FOUND:
            return Board.ROWS - 1, column
        else:
            return item_index - 1, column

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
        if self.__board[0, column] != Board.EMPTY:
            return Board.FAILED, Board.NOT_FOUND, Board.NOT_FOUND
        # Scan the column
        x, y = self.find_first_non_empty(column)
        self.__board[x, y] = np.int8(current_turn)
        return Board.SUCCESS, x, y

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

        main_slant, _ = self.__create_main_slant(x, y)
        if Board.__search_for_victory(main_slant, player):
            return Board.WINNER_DICT[player]

        secondry_slant, _ = self.__create_secondary_slant(x, y)
        if Board.__search_for_victory(secondry_slant, player):
            return Board.WINNER_DICT[player]
        return Board.GAME_IN_PROGRESS

    def __create_main_slant(self, x, y):
        pivot_index = 0
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
            pivot_index += 1
        arr = np.array(arr)
        return arr, pivot_index

    def __create_secondary_slant(self, x, y):
        pivot_index = 0
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
            pivot_index += 1
        arr = np.array(arr)
        return arr, pivot_index

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

    @staticmethod
    def sum_possibilities(data, important_index, player):

        """
        get all possible combination
        :param data: line of column or slant from data
        :param important_index: pivot index
        :param player: Board.EMPTY or Board.WHITE or Board.BLACK
        :return: sum of possible combination
        """
        # boundary conditions
        min_index = max(important_index - 3, 0)
        max_index = min(important_index + 4, len(data))
        if len(data) < 4:
            return 0
        evaluate = 0
        parse_data = data[min_index:max_index]
        list_of_list_of_possible_wins = Board.scan(parse_data)
        for lst in list_of_list_of_possible_wins:
            if Board.valid_combination(lst, player):
                evaluate += 1
        return evaluate

    @staticmethod
    def valid_combination(lst, player):
        for ele in lst:
            if not ele == Board.EMPTY and not ele == player:
                return False
        return True

    @staticmethod
    def scan(data):

        """
        Return lst of lst of possbile data
        :param data: lst of lst
        :return:
        """
        lst = list()
        for i in range(len(data) - 3):
            temp_list = list()
            for j in range(4):
                temp_list.append(data[i + j])
            lst.append(temp_list)
        return lst

    def sum_all_possibilities(self, player, x, y):
        """
        sum all the possibilies a single point can reach
        Its important function for AI Evaluation
        :param board: board type instance
        :param player: Board.BLACK or Board.WHITE
        :param x: coordinate int
        :param y: coordinate int
        :return: number of possibilities
        """
        # A variable in board has to be (Board.EMPTY,Board.WHITE,Board.BLACK)
        column = self.__board[:, y]
        total_eval = 0
        total_eval += Board.sum_possibilities(column, x, player)

        row = self.__board[x, :]
        total_eval += Board.sum_possibilities(row, y, player)

        main_slant, pivot_index = self.__create_main_slant(x, y)
        total_eval += Board.sum_possibilities(main_slant, pivot_index, player)

        secondry_slant, pivot_index = self.__create_secondary_slant(x, y)
        total_eval += Board.sum_possibilities(secondry_slant, pivot_index, player)

        return total_eval

    @staticmethod
    def flip_color(current_turn):
        """
        Change the color
        :return:
        """
        if current_turn == Board.WHITE:
            return Board.BLACK
        if current_turn == Board.BLACK:
            return Board.WHITE

    def you_can_add_two_or_more_disk(self, column):
        if self.__board[1, column] != Board.EMPTY:
            return False
        return True

    def search_for_win_in_one_move(self, __player):
        """
        return the number of the winning column in one
        if not found , return Board.NOT_FOUND = -1
        :return:
        """
        for column in self.list_of_moves():
            flag, x, y = self.update_board(column, __player)
            if self.check_win_in_point(x, y, __player):
                return column
            self.__board[x, y] = Board.EMPTY
        return Board.NOT_FOUND

    def evaluate_via_centralize_point(self, __player, dict_move):
        """
        Using The sum_all_possibilities(player,x,y) from Board
        we gave grade to each move
        :return: update the self.dict_move
        """
        for column in self.list_of_moves():
            flag, x, y = self.update_board(column, __player)
            ratio = self.sum_all_possibilities(__player, x, y) / Board.ALL_POSSIBILITIES
            evaluation = ratio * Board.WEIGH_POSSIBILITIES
            dict_move[column] += evaluation
            self.__board[x, y] = Board.EMPTY

    def evaluate_via_avoid_second_add(self, __player, dict_move):
        """
        if __player == self.__player
        If adding 2 disk to certain column cause winning than
        avoid adding to column
        if __player == not self.__player
        If I add disk and my opponent add disk to the same column
        and I am losing for sure
        :return: update the self.dict_move
        """
        for column in self.list_of_moves():
            if self.you_can_add_two_or_more_disk(column):
                temp_player = Board.flip_color(__player)
                # add 2 disks
                self.update_board(column, temp_player)
                flag, x, y = self.update_board(column, __player)
                #
                if self.check_win_in_point(x, y, __player):
                    # Should decrease the value
                    if __player == __player:
                        dict_move[column] += Board.WEIGH_AVOID_SECOND_ADD_WINNING
                    if __player == Board.flip_color(__player):
                        dict_move[column] += Board.WEIGH_LOSING_FOR_SURE

                self.__board[x, y] = Board.EMPTY  # init the higher
                self.__board[x + 1, y] = Board.EMPTY  # 1 init below the higher

    def get_count_of_possible_wins(self, __player):
        """
        Returns the number of possible absulote winning moves
        :param __player:
        :return:integer from 0 to COLUMNS
        """
        count = 0
        self.update_possible_moves()
        for column in self.list_of_moves():
            flag, x, y = self.update_board(column, __player)
            # print(self.__board)
            if self.check_win_in_point(x, y, __player):  # is not Board.GAME_IN_PROGRESS:
                count += 1
            self.__board[x, y] = Board.EMPTY
        return count

    def evaluate_player_has_two_or_more_possible_wins_next_turn(self, __player, dict_move):
        for column in self.list_of_moves():
            flag, x, y = self.update_board(column, __player)
            if self.get_count_of_possible_wins(__player) >= 2:
                dict_move[column] += Board.WEIGH_WINNING
            self.__board[x, y] = Board.EMPTY

    def evaluate(self, __player, dict_move):
        """
        This function try to evaluate the situation on the board
        and based on our functions try to find the best move
        :return: update the self.dict_move
        """
        self.evaluate_via_centralize_point(__player, dict_move)
        self.evaluate_via_avoid_second_add(Board.flip_color(__player), dict_move)
        self.evaluate_via_avoid_second_add(__player, dict_move)
        self.evaluate_player_has_two_or_more_possible_wins_next_turn(__player, dict_move)
        self.evaluate_player_has_two_or_more_possible_wins_next_turn(
            Board.flip_color(__player),
            dict_move)

    def list_of_moves(self):
        """
        This function get all possible moves
        :return: lst of all possible moves
        """
        lst = []
        for i, ele in enumerate(self.possible_moves):
            if ele:
                lst.append(i)
        return lst


