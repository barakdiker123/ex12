from ex12.board import *


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
    evaluate = 0
    parse_data = data[min_index:max_index]
    list_of_list_of_possible_wins = scan(parse_data)
    for lst in list_of_list_of_possible_wins:
        if valid_combination(lst, player):
            evaluate += 1
    return evaluate


def valid_combination(lst, player):
    for ele in lst:
        if not ele == Board.EMPTY and not ele == player:
            return False
    return True


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


def sum_all_possibilities(board, player, x, y):
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
    column = board[:, y]
    total_eval = 0
    total_eval += sum_possibilities(column, x, player)

    row = board[x, :]
    total_eval += sum_possibilities(row, y, player)

    main_slant, pivot_index = self.__create_main_slant(x, y)
    total_eval += sum_possibilities(main_slant, pivot_index, player)

    secondry_slant, pivot_index = self.__create_secondary_slant(x, y)
    total_eval += sum_possibilities(secondry_slant, pivot_index, player)

    return Board.GAME_IN_PROGRESS
