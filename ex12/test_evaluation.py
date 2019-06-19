from ex12.board import Board
from ex12.evaluation import *
import numpy as np


def test_sum_possibilities():
    data = np.array([Board.EMPTY, Board.EMPTY, Board.EMPTY,
                     Board.BLACK, Board.EMPTY, Board.EMPTY,
                     Board.EMPTY, Board.EMPTY, Board.EMPTY,
                     Board.EMPTY], dtype=np.int8)
    player = Board.WHITE
    important_index = 6
    print(sum_possibilities(data, important_index, player))



test_sum_possibilities()
