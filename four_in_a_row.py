import tkinter as tk

from ex12.ai import *
from ex12.game import *
from screen import *
from ex12.board import *


class FourInRow:

    def __init__(self, screen):
        self.__screen = screen


    def run(self):
        self.__screen.main()



if __name__ == '__main__':
    import pdb;pdb.set_trace()
    four_in_a_row = FourInRow(Screen(Game()))
    four_in_a_row.run()
