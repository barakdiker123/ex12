import unittest

from ex12.ai import *
from ex12.game import *


class TestAI(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()
        self.game.make_move(0)
        for i in range(3):
            self.game.make_move(1)
            self.game.make_move(0)

    def test_is_game_over1(self):
        with self.assertRaises(Exception):
            ai = AI(self.game, Game.WHITE)
        self.assertRaises(NoPossibleMovesAI, AI, self.game, Game.WHITE)

        # self.assertEqual(self.ai.is_game_over(), True)
