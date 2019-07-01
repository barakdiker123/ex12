from ex12.ai import *
from ex12.game import *
from ex12.screen import *
from ex12.board import *


class FourInRow:

    def __init__(self, screen):
        self.__screen = screen

    def run(self):
        self.__screen.main()


if __name__ == '__main__':

    four_in_a_row = FourInRow(Screen())
    four_in_a_row.run()
