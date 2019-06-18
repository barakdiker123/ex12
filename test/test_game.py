
# import game
from ex12.game import *
import unittest


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game()

    def test_get_winner1(self):
        self.g.make_move(0)
        for i in range(3):
            self.g.make_move(1)
            self.g.make_move(0)
        self.assertEqual(self.g.get_winner(), Game.WHITE_WINS, msg="Cannot find win")

    def test_get_winner2(self):
        self.g.make_move(0)
        for i in range(2):
            self.g.make_move(1)
            self.g.make_move(0)
        self.assertEqual(self.g.get_winner(), Game.GAME_IN_PROGRESS, msg="game ended prematurely")

    def test_get_winner3(self):
        self.g.make_move(0)
        self.g.make_move(1)
        self.g.make_move(1)
        self.g.make_move(2)
        self.g.make_move(2)
        self.g.make_move(5)
        self.g.make_move(2)
        self.g.make_move(3)
        self.g.make_move(3)
        self.g.make_move(3)
        self.g.make_move(3)

        self.assertEqual(self.g.get_winner(), Game.WHITE_WINS, msg="Cannot find win in slant")

    def tearDown(self) -> None:
        del self.g
