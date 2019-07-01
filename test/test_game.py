# import game
# from ex12.game import *
import unittest
from ex12.game import *


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

    def test_tie1(self):
        for i in range(3):
            for j in range(6):
                self.g.make_move(i)
        self.g.make_move(6)
        for i in range(3, 6):
            for j in range(6):
                self.g.make_move(i)
        for i in range(5):
            self.g.make_move(6)
        print(self.g)
        self.assertEqual(self.g.get_winner(), Game.TIE, msg="Random Fill the board")

    def test_get_current_player1(self):
        self.g.make_move(0)
        self.assertEqual(2, self.g.get_current_player(), msg="Wrong player flip")

    def test_get_current_player2(self):
        self.g.make_move(0)
        self.g.make_move(0)
        self.g.make_move(0)
        self.assertEqual(2, self.g.get_current_player(), msg="Wrong player flip")

    def test_get_player_at1(self):
        self.g.make_move(0)
        self.assertEqual(self.g.get_player_at(5, 0), 1)
        self.assertEqual(self.g.get_player_at(5, 6), None)

    def test_get_winner(self):
        pass

    def tearDown(self) -> None:
        del self.g
