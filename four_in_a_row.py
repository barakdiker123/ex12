import tkinter as tk

from ai import *
from game import *
from screen import *
from board import *


class FourInRow:

    def __init__(self, screen):
        self.__screen = screen


    def run(self):
        self.__screen.main()



if __name__ == '__main__':
    four_in_a_row = FourInRow(Screen(Game()))
    four_in_a_row.run()
