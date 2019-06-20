import unittest

from ex12.ai import *
from ex12.game import *
from ex12.board import *


class TestAI(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()

    def test_is_game_over1(self):
        self.game.make_move(0)
        for i in range(3):
            self.game.make_move(1)
            self.game.make_move(0)
        ai = AI(self.game, Board.WHITE)
        # ai.find_legal_move(AI.INSTANT_ALGORITHM_TIMEOUT)
        # with self.assertRaises(Exception):
        #     ai.find_legal_move(AI.INSTANT_ALGORITHM_TIMEOUT)
        # self.assertRaises(NoPossibleMovesAI, ai.find_legal_move(AI.INSTANT_ALGORITHM_TIMEOUT))

    def test_is_game_over2(self):
        for i in range(2):
            self.game.make_move(0)
        for i in range(2):
            self.game.make_move(1)
        for i in range(2):
            self.game.make_move(2)
        self.game.make_move(3)
        ai = AI(self.game, Board.BLACK)
        # self.assertRaises(NoPossibleMovesAI, ai.find_legal_move(AI.INSTANT_ALGORITHM_TIMEOUT))

    def test_find_legal_move1(self):
        for i in range(3):
            for j in range(6):
                self.game.make_move(i)
        self.game.make_move(6)
        for i in range(3, 5):
            for j in range(6):
                self.game.make_move(i)
        ai = AI(self.game, Board.BLACK)
        column_cal = ai.find_legal_move(AI.INSTANT_ALGORITHM_TIMEOUT)
        self.assertIn(column_cal, [Board.COLUMNS - 1, Board.COLUMNS - 2])

    def test_find_legal_move2(self):
        self.game.make_move(0)
        self.game.make_move(5)
        self.game.make_move(1)
        self.game.make_move(5)
        self.game.make_move(3)
        self.game.make_move(5)
        ai = AI(self.game, Board.WHITE)
        column_cal = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
        self.assertEqual(2, column_cal)
        # self.assertEqual(self.ai.is_game_over(), True)

    def test_find_legal_move3(self):
        """
        Check slant victory in one move
        :return:
        """
        self.game.make_move(0)
        self.game.make_move(1)
        self.game.make_move(1)
        self.game.make_move(2)
        self.game.make_move(2)
        self.game.make_move(5)
        self.game.make_move(2)
        self.game.make_move(3)
        self.game.make_move(3)
        self.game.make_move(3)
        self.game.make_move(6)
        self.game.make_move(0)
        # self.game.make_move(3) The move I want the computer to find
        ai = AI(self.game, Board.WHITE)
        column_cal = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
        self.assertEqual(3, column_cal)

    def test_find_legal_move3(self):
        self.game.make_move(3)
        ai = AI(self.game, Board.BLACK)
        column_cal = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
        self.assertEqual(3, column_cal)

    def test_find_legal_move4(self):
        self.game.make_move(2)
        self.game.make_move(2)
        self.game.make_move(3)
        self.game.make_move(3)
        self.game.make_move(4)
        self.game.make_move(4)
        ai = AI(self.game, Board.BLACK)
        column_cal = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
        print(column_cal)

        print(self.game)



