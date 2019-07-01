from ex12.board import Board
import unittest


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board()

    def test_sum_all_possibilities1(self):
        self.assertEqual(self.board.sum_all_possibilities(Board.WHITE, 0, 0), 3)

    def test_sum_all_possibilities2(self):
        self.assertEqual(self.board.sum_all_possibilities(Board.WHITE, 1, 0), 4)

    def test_sum_all_possibilities3(self):
        self.assertEqual(self.board.sum_all_possibilities(Board.WHITE, 1, 1), 6)

    def test_sum_all_possibilities4(self):
        self.assertEqual(self.board.sum_all_possibilities(Board.WHITE, 2, 2), 11)

    def test_find_coordinate_column1(self):
        self.assertEqual(self.board.find_coordinate_column(2, 2), ([(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]))
        self.assertEqual(self.board.find_coordinate_column(0, 2), ([(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]))

    def test_find_coordinate_row1(self):
        self.assertEqual(
            self.board.find_coordinate_row(2, 2), ([(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)]))

        self.assertEqual(
            self.board.find_coordinate_row(2, 0), ([(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)]))

    def test_find_coordinate_secondary_slant1(self):
        self.assertEqual(self.board.find_coordinate_secondary_slant(1, 1), ([(0, 2), (1, 1), (2, 0)]))

    def test_find_coordinate_main_slant1(self):
        self.assertEqual(
            self.board.find_coordinate_main_slant(1, 1), ([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]))

    def test_find_four_via_coordinate_tuple1(self):
        self.board.board[5, 1] = Board.WHITE
        self.board.board[5, 2] = Board.WHITE
        self.board.board[5, 3] = Board.WHITE
        self.board.board[5, 4] = Board.WHITE
        tup_of_coordinate = self.board.find_coordinate_row(5, 2)

        self.assertEqual(self.board.find_four_via_coordinate_tuple(tup_of_coordinate, Board.WHITE, 4),
                         [(5, 1), (5, 2), (5, 3), (5, 4)])

    def test_find_four_via_coordinate_tuple2(self):
        self.board.board[1, 1] = Board.WHITE
        self.board.board[2, 2] = Board.WHITE
        self.board.board[3, 3] = Board.WHITE
        self.board.board[4, 4] = Board.WHITE
        tup_of_coordinate = self.board.get_coordinate_tuple_winning_in_point(3, 3, 4)

        self.assertEqual(self.board.find_four_via_coordinate_tuple(tup_of_coordinate, Board.WHITE, 4),
                         [(1, 1), (2, 2), (3, 3), (4, 4)])

    def test_get_winning_tuple_coordinate(self):
        self.board.board[1, 1] = Board.WHITE
        self.board.board[2, 2] = Board.WHITE
        self.board.board[3, 3] = Board.WHITE
        self.board.board[4, 4] = Board.WHITE
        self.assertEqual(self.board.get_coordinate_tuple_winning_in_point(2, 2, 4), [(1, 1), (2, 2), (3, 3), (4, 4)])

    def test_get_winner(self):
        pass
