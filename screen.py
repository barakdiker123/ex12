import tkinter as tk
import tkinter.messagebox
from ex12.game import *
import numpy as np
from ex12.ai import *
from ai_or_human import *
from board import *
import random

LARGE_FONT = ("Verdana bold", 24)
MEDIUM_FONT = ("Verdana bold", 18)
SMALL_FONT = ("Verdana bold", 14)

#################################################
#CANT FIGURE OUT WHY BLACK COME FIRST
#################################################

WHITE = 1
BLACK = 2

COLUMNS = 7

HUMAN_VS_HUMAN = 10
HUMAN_VS_AI = 20
AI_VS_HUMAN = 30
AI_VS_AI = 40


class Screen(tk.Tk):

    def __init__(self, game):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.container.pack(fill="both")
        self.geometry("700x700")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.main_color_dict = {"COLOR_1": "white", "COLOR_2": "black"}
        self.counter_dict = {"AI_1": False, "AI_2": False}
        self.frames = {}
        for page in (GamePage, StartPage):
            frame = page(self.container, self, self.counter_dict["AI_1"], self.counter_dict["AI_2"])
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(page)
        self.game = game


    def main_color_dict(self):
        return self.main_color_dict

    def get_container(self):
        return self.container


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


    def main(self):
        self.mainloop()


class StartPage(tk.Frame):

    def __init__(self, parent, controller, AI_1, AI_2):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.create_main_menu()
        self.counter_dict = {self.ai_button_1: False, self.ai_button_2: False}
        self.main_color_dict = {"COLOR_1": "white", "COLOR_2": "black"}
        self.color_dict_1 = {self.white: 0, self.red: 0, self.green: 0}
        self.color_dict_2 = {self.black: 0, self.yellow: 0, self.pink: 0}
        self.color_dict = {self.white: "antique white", self.red: "red", self.green: "green4", self.black: "black",
                           self.yellow: "orange", self.pink: "deep pink2"}


    def create_main_menu(self):
        """This function creates main menu"""

        self.canvas = tk.Canvas(self, height=700, widt=700, bg="orange2")
        self.canvas.pack()
        self.welcome_msg = self.canvas.create_text(340, 50, text="\nWelcome to", font=MEDIUM_FONT)
        self.welcome_msg_blue = self.canvas.create_text(340, 120, text="CONNECT FOUR\n", font=LARGE_FONT,
                                                        fill="medium blue")
        self.menu_title = self.canvas.create_text(350, 185, text="Choose how you want to play:\n\n", font=SMALL_FONT)

        self.player_one = self.canvas.create_text(160, 230, text="Player 1\n", font=MEDIUM_FONT)
        self.human_button_1 = tk.Button(self, text="Human player", bg="medium blue", fg="white",
                                        command=lambda: self.change_button_color_human_1(self.human_button_1))
        self.human_button_1_window = self.canvas.create_window(155, 263, window=self.human_button_1)
        self.ai_button_1 = tk.Button(self, text="AI player", bg="red3",
                                     command=lambda: self.change_button_color_ai_1(self.ai_button_1))
        self.ai_button_1_window = self.canvas.create_window(153, 300, window=self.ai_button_1)

        self.player_two = self.canvas.create_text(540, 230, text="Player 2\n", font=MEDIUM_FONT)
        self.human_button_2 = tk.Button(self, text="Human player", bg="medium blue", fg="white",
                                        command=lambda: self.change_button_color_human_2(self.human_button_2))
        self.human_button_2_window = self.canvas.create_window(540, 263, window=self.human_button_2)
        self.ai_button_2 = tk.Button(self, text="AI player", bg="red3",
                                     command=lambda: self.change_button_color_ai_2(self.ai_button_2))
        self.ai_button_2_window = self.canvas.create_window(540, 300, window=self.ai_button_2)
        self.choose_color = self.canvas.create_text(350, 440, text="Please choose one colour for each player:\n\n\n\n\n\n",
                                                    font=SMALL_FONT)
        self.create_color_buttons()
        play_button = tk.Button(self, text="PLAY", bg="red", font="bold", width=10,
                                command=lambda: self.if_play_pressed())
        play_button_window = self.canvas.create_window(287, 510, window=play_button)


    def choose_ai_or_human_player(self):
        """
        This function checks which button was pressed, and returns True/None
        True for AI, None for human.
        :return: True/None
        """
        if self.counter_dict[self.ai_button_1] == True:
            self.controller.counter_dict["AI_1"] = True
        else:
            self.controller.counter_dict["AI_1"] = None
        if self.counter_dict[self.ai_button_2] == True:
            self.controller.counter_dict["AI_2"] = True
        else:
            self.controller.counter_dict["AI_2"] = None


    def change_button_color_ai_1(self, button):
        """
        This method changes the color of the button user choose
        """
        if self.counter_dict[button] == False:
            button.configure(bg="white", fg="black")
            self.counter_dict[button] = True
        elif self.counter_dict[button] == None:
            button.configure(bg="white", fg="black")
            self.human_button_1.configure(bg="medium blue", fg="white")
            self.counter_dict[button] = True


    def change_button_color_ai_2(self, button):
        """
        This method changes the color of the button user choose
        """
        if self.counter_dict[button] == False:
            button.configure(bg="white", fg="black")
            self.counter_dict[button] = True
        elif self.counter_dict[button] == None:
            button.configure(bg="white", fg="black")
            self.human_button_2.configure(bg="medium blue", fg="white")
            self.counter_dict[button] = True


    def change_button_color_human_1(self, button):
        """
        This method changes the color of the button user choose
        """
        if self.counter_dict[self.ai_button_1] == False:
            button.configure(bg="white", fg="black")
            self.counter_dict[self.ai_button_1] = None
        elif self.counter_dict[self.ai_button_1] == True:
            button.configure(bg="white", fg="black")
            self.ai_button_1.config(bg="red3")
            self.counter_dict[self.ai_button_1] = None


    def change_button_color_human_2(self, button):
        """
        This method changes the color of the button user choose
        """
        if self.counter_dict[self.ai_button_2] == False:
            button.configure(bg="white", fg="black")
            self.counter_dict[self.ai_button_2] = None

        if self.counter_dict[self.ai_button_2] == True:
            button.configure(bg="white", fg="black")
            self.ai_button_2.configure(bg="red3")
            self.counter_dict[self.ai_button_2] = None




    def if_play_pressed(self):
        """
        This method controls what happens when a user presses "play" button.
        """

        if self.counter_dict[self.ai_button_1] == False:
            tkinter.messagebox.showinfo("ERROR", "You have to choose an option for player 1")
        elif self.counter_dict[self.ai_button_2] == False:
            tkinter.messagebox.showinfo("ERROR", "You have to choose an option for player 2")
        else:
            self.color_chosen(self.color_dict_1, "white", "COLOR_1")
            self.color_chosen(self.color_dict_2, "black", "COLOR_2")
            self.choose_ai_or_human_player()
            GamePage(self.parent, self.controller, AI_1=self.controller.counter_dict["AI_1"], AI_2=self.controller.counter_dict["AI_2"])
            self.controller.show_frame(GamePage)


        # TEST FOR CHOOSING PLAYERS
        for key in self.counter_dict:
            if self.counter_dict[key] == True:
                print(key, self.counter_dict[key])
            else:
                print(key, self.counter_dict[key])
        # TEST FOR CHOOSINT COLOR
        for key, val in self.color_dict_1.items():
            if val == 1:
                print(self.color_dict[key])
        for key, val in self.color_dict_2.items():
            if val == 1:
                print(self.color_dict[key])

        ###############################################################################
        # COLOR RELATED FITCHERS
        ###############################################################################


    def create_color_buttons(self):
        """This function creates color buttons for the main menu"""
        self.white = tk.Button(self, bg="antique white", text="white",
                               command=lambda: self.choose_white(self.white, "antique white"))

        self.white_window = self.canvas.create_window(116, 432, window=self.white)
        self.red = tk.Button(self, bg="red", text="red", command=lambda: self.choose_red(self.red, "red"))
        self.red_window = self.canvas.create_window(155, 432, window=self.red)
        self.green = tk.Button(self, bg="green4", text="green",
                               command=lambda: self.choose_green(self.green, "green4"))
        self.green_window = self.canvas.create_window(194, 432, window=self.green)
        self.black = tk.Button(self, bg="black", fg="white", text="black",
                               command=lambda: self.choose_black(self.black, "black"))
        self.black_window = self.canvas.create_window(495, 432, window=self.black)
        self.yellow = tk.Button(self, bg="orange", text="yellow",
                                command=lambda: self.choose_yellow(self.yellow, "orange"))
        self.yellow_window = self.canvas.create_window(542, 432, window=self.yellow)
        self.pink = tk.Button(self, bg="deep pink2", text="pink",
                              command=lambda: self.choose_pink(self.pink, "deep pink2"))
        self.pink_window = self.canvas.create_window(587, 432, window=self.pink)


    def choose_black(self, button, color):
        if not self.color_dict_2[button] % 2:
            button.configure(bg="white", fg="black")
            self.yellow.configure(bg="orange")
            self.pink.configure(bg="deep pink2")
            self.color_dict_2[self.yellow] = 0
            self.color_dict_2[self.pink] = 0
            self.color_dict_2[button] = 1


    def choose_yellow(self, button, color):
        if not self.color_dict_2[button] % 2:
            button.configure(bg="white", fg="black")
            self.black.configure(bg="black", fg="white")
            self.pink.configure(bg="deep pink2")
            self.color_dict_2[self.black] = 0
            self.color_dict_2[self.pink] = 0
            self.color_dict_2[button] = 1


    def choose_pink(self, button, color):
        if not self.color_dict_2[button] % 2:
            button.configure(bg="white", fg="black")
            self.yellow.configure(bg="orange")
            self.black.configure(bg="black", fg="white")
            self.color_dict_2[self.yellow] = 0
            self.color_dict_2[self.black] = 0
            self.color_dict_2[button] = 1


    def choose_white(self, button, color):
        if not self.color_dict_1[button] % 2:
            button.configure(bg="white", fg="black")
            self.red.configure(bg="red")
            self.green.configure(bg="green4")
            self.color_dict_1[self.green] = 0
            self.color_dict_1[self.red] = 0
            self.color_dict_1[button] = 1


    def choose_red(self, button, color):
        if not self.color_dict_1[button] % 2:
            button.configure(bg="white", fg="black")
            self.white.configure(bg="antique white")
            self.green.configure(bg="green4")
            self.color_dict_1[self.green] = 0
            self.color_dict_1[self.white] = 0
            self.color_dict_1[button] = 1


    def choose_green(self, button, color):
        if not self.color_dict_1[button] % 2:
            button.configure(bg="white", fg="black")
            self.red.configure(bg="red")
            self.white.configure(bg="antique white")
            self.color_dict_1[self.white] = 0
            self.color_dict_1[self.red] = 0
            self.color_dict_1[button] = 1


    def color_chosen(self, color_dict_num, defult_color, change):
        for key, val in color_dict_num.items():
            if val == 1:
                self.controller.main_color_dict[change] = self.color_dict[key]
            if all(value == 0 for value in color_dict_num.values()):
                self.controller.main_color_dict[change] = defult_color
        # rev_dict = {}
        # for key, value in color_dict_num.items():
        #     rev_dict.setdefault(value, set()).add(key)
        # result = [key for key, values in rev_dict.items()
        #           if len(values) > 1]


###############################################################################
#GAMEPAGE
###############################################################################



class GamePage(tk.Frame):


    def __init__(self, parent, controller, AI_1=False, AI_2=False):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.AI_1 = AI_1
        self.AI_2 = AI_2
        self.game = Game()
        self.canvas = tk.Canvas(self, height=700, widt=700, bg="grey")
        self.canvas.pack()
        self.make_move_value = True
        self.create_game_screen()
        self.checkers_lst = []

        self.who_vs_who()
        self.canvas.bind("<Button-1>", self.return_column)
        if AI_1 == True and AI_2 == True:
            self.AI_move()



    def who_vs_who(self): #callback
        """This is a callback mathod"""
        if self.AI_1 == None and self.AI_2 == None:
            print("human_vs_human")
            return HUMAN_VS_HUMAN
        if self.AI_1 == None and self.AI_2 == True:
            print("human_vs_AI")
            return HUMAN_VS_AI
        if self.AI_1 == True and self.AI_2 == None:
            print("AI vs human")
            return AI_VS_HUMAN
        if self.AI_1 == True and self.AI_2 == True:
            print("AI VS AI")
            return AI_VS_AI



    ###############################################################################
    # CREATE GAME SCREEN
    ###############################################################################


    def create_game_screen(self):
        """This method draws the game screen"""
        self.board = self.canvas.create_rectangle(1, 700, 700, 100, fill="blue4", tag="board")
        self._draw_holes()
        self.create_game_screen_buttons()



    def create_game_screen_buttons(self):
        self.button1 = tk.Button(self, text="Quit", command=self.quit_button, anchor="w")
        self.button1.configure(width=10, activebackground="red")
        self.button1_window = self.canvas.create_window(10, 10, anchor="nw", window=self.button1)
        self.button2 = tk.Button(self, text="Main menu", command=self.main_menu_buton, anchor="w")
        self.button2.configure(width=10, activebackground="blue")
        self.button2_window = self.canvas.create_window(100, 10, anchor="nw", window=self.button2)
        self.button3 = tk.Button(self, text="Help", command=self.help_button, anchor="w")
        self.button3.configure(width=10, activebackground="blue")
        self.button3_window = self.canvas.create_window(190, 10, anchor="nw", window=self.button3)


    def quit_button(self):
        msg = tkinter.messagebox.askquestion("QUIT", "Are you sure you want to quit?")
        if msg == "yes":
            self.destroy()
        else:
            return

    def main_menu_buton(self):
        msg = tkinter.messagebox.askquestion("Main menu", "Are you sure you "
                                                          "want to go back to main menu? \n Every change you've made will be lost")
        if msg == "yes":
            for checker in self.checkers_lst:
                self.canvas.delete(checker)
            self.game = Game()
            self.controller.show_frame(StartPage)
        else:
            return

    def help_button(self):
        msg = tkinter.messagebox.showinfo("Help", "WELCOME TO CONNECT FOUR! "
                                                  "\n\n HOW TO PLAY? \n\nThis is a game for 2 players. \nEvery player,"
                                                  " at their turn, chooses a column to insert a checker.\n"
                                                  "The winner gets 4 checkers in a row! the 4-in-a-row can be"
                                                  " horizontal, vartical, or diagonal. \n\nABOUT THE CREATORS: \n\n"
                                                  "Barak Diker and Noa Babliki are students at Hebrew university of "
                                                  "jerusalem. \nThis is their final project for Introduction to"
                                                  " computer science.")

    def _draw_holes(self):
        """
        This method draws holes
        i is a x parameter, j is a y parameter.
        """
        for i in range(0, 700, 100):
            for j in range(0, 500, 90):
                self.hole = self.canvas.create_oval(9 + i, 560 - j, 90 + i, 640 - j, fill="grey")


    ###############################################################################
    # HUMAN VS HUMAN
    ###############################################################################


    def return_column(self, event):
        """This method is activated when a human player is chosen"""
        col_width = self.canvas.winfo_width() / COLUMNS
        # row_height = self.canvas.winfo_height() / self.num_of_rows
        col = int(event.x // col_width)
        # row = int(event.y // row_height)
        try:
            if self.controller.counter_dict["AI_1"] == None and self.controller.counter_dict["AI_2"] == None:
                print("H")
                if self.make_move_value == True:
                    self.player_move(self.game.make_move(col))
            if self.controller.counter_dict["AI_1"] == None and self.controller.counter_dict["AI_2"] == True:
                print("HA")
                if self.make_move_value == True:
                    if self.check_turn() == WHITE:
                        self.playe_move(self.game.make_move(col))
                    else:
                        self.AI_move(self.game.make_move(random.randint(0,7)))
            if self.controller.counter_dict["AI_1"] == True and self.controller.counter_dict["AI_2"] == None:
                self.AI_vs_Human()
            else:
                print("A")
                self.AI_move(random.randint(0, 7))

        except Exception:
            return


    def AI_vs_Human(self):
        print("AH")
        if self.make_move_value == True:
            while self.check_turn() == BLACK:
                self.playe_move(self.game.make_move(col))
            while self.check_turn() == WHITE:
                self.AI_move()



    def player_move(self, tuple):
        """
        This method is in charge of  a single move in the game.
        """
        y, x = tuple
        i = x * 100
        j = y * 90
        if y == -1:
            return

        elif self.check_turn() == WHITE:
            self.checkers_lst.append(self.canvas.create_oval(9 + i, 110 + j, 90 + i, 190 + j,
                                                             fill=self.controller.main_color_dict["COLOR_1"]))
            self.check_winner()
            return

        elif self.check_turn() == BLACK:
            self.checkers_lst.append(self.canvas.create_oval(9 + i, 110 + j, 90 + i, 190 + j,
                                                             fill=self.controller.main_color_dict["COLOR_2"]))
            self.check_winner()
            return




    def AI_move(self):
        """
        This method is in charge of  a single move in the game.
        """
        while self.check_winner() == Game.GAME_IN_PROGRESS:
            val = 0
            while val < 5:
                tuple = self.game.make_move(random.randint(0, 6))
                print(tuple)
                y, x = tuple
                i = x * 100
                j = y * 90
                print(val)
                val += 1
            while val == 5:
                if self.check_turn() == WHITE:
                    self.checkers_lst.append(self.canvas.create_oval(9 + i, 110 + j, 90 + i, 190 + j,
                                                                     fill=self.controller.main_color_dict["COLOR_1"]))

                    val = 0


                elif self.check_turn() == BLACK:
                    self.checkers_lst.append(self.canvas.create_oval(9 + i, 110 + j, 90 + i, 190 + j,
                                                                     fill=self.controller.main_color_dict["COLOR_2"]))
                    val = 0




        ###############################################################################
        # METHODS FOR ALL PLAYERS
        ###############################################################################

    def check_winner(self):
        if self.game.get_winner() == Game.TIE:
            self.make_move_value = False
            self.TIE_massage()
        if self.game.get_winner() == Game.WHITE_WINS:
            self.WIN_message("Player 1")
            self.make_move_value = False
        if self.game.get_winner() == Game.BLACK_WINS:
            self.WIN_message("Player 2")
            self.make_move_value = False
        if self.game.get_winner() == Game.GAME_IN_PROGRESS:
            self.make_move_value = True

    def check_turn(self):
        if self.controller.game.get_current_player() == Game.WHITE:
            return Game.WHITE
        if self.controller.game.get_current_player() == Game.BLACK:
            return Game.BLACK








