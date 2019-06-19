import unittest

from ex12.ai import *
from ex12.game import *
from ex12.board import *


class TestAI(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()
        self.game.make_move(0)
        for i in range(3):
            self.game.make_move(1)
            self.game.make_move(0)

    def test_is_game_over1(self):
        ai = AI(self.game, Board.WHITE)
        with self.assertRaises(Exception):
            ai.find_legal_move()
        self.assertRaises(NoPossibleMovesAI, ai.find_legal_move)

        # self.assertEqual(self.ai.is_game_over(), True)
