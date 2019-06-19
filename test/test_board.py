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
