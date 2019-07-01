#############################################################
# FILE : four_in_a_row.py
# WRITER : Noa Babliki, noa.babliki , 206090409
# WRITER : Barak Diker, barakdiker, 313538225
# EXERCISE : intro2cs ex12 2019-2018
# DESCRIPTION: A game of connect four. enjoy!
#############################################################

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
    four_in_a_row = FourInRow(Screen())
    four_in_a_row.run()
