from screen import *
from game import *

class AIorHuman:

    def __init__(self):
        self.__main_player_dict_1 = {"ai_player_1": 0, "human_player_1": 0}
        self.__main_player_dict_2 = {"ai_player_2": 0, "human_player_2": 0}

    def AI_or_human(self, player_chosen):
        """This method checks if the user chose human or AI, and repurts
        back to the GUI. It does that by checking values in a dictionary"""
        for player in player_chosen:
            if player in self.__main_player_dict_1:
                self.__main_player_dict_1[player] = 1
            else:
                self.__main_player_dict_2[player] = 1


    def get_dict_1(self):
        return self.__main_player_dict_1

    def get_dict_2(self):
        return self.__main_player_dict_2

    def get_player_1(self):
        for key in self.__main_player_dict_1:
            if self.__main_player_dict_1[key] == 1:
                return key


    def get_player_2(self):
        for key in self.__main_player_dict_2:
            if self.__main_player_dict_2[key] == 1:
                return key

