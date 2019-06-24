import tkinter as tk

from ai import *
from game import *
from screen import *
from board import *
#from try_gui import *

class FourInRow:

    def __init__(self, screen):
        self.__screen = screen


    def run(self):
        self.__screen.main()



if __name__ == '__main__':
    #root = tk.Tk()
    four_in_a_row = FourInRow(Screen())
    four_in_a_row.run()
