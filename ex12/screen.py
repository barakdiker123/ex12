#############################################################
# FILE : Screen.py
# WRITER : Noa Babliki, noa.babliki , 206090409
# WRITER : Barak Diker, barakdiker, 313538225
# EXERCISE : intro2cs ex12 2019-2018
# DESCRIPTION: A game of connect four. enjoy!
#############################################################

import tkinter as tk
import tkinter.messagebox
from ex12.game import *
from ex12.ai import *
from ex12.board import *
import random

LARGE_FONT = ("Verdana bold", 24)
MEDIUM_FONT = ("Verdana bold", 18)
SMALL_FONT = ("Verdana bold", 14)

WHITE = 1
BLACK = 2
TIE = 0

COLUMNS = 7


class Screen(tk.Tk):
    AI_PLAY = True
    PLAYER_PLAY = False
    NONE_PLAY = None

    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.container.pack(fill="both")
        self.geometry("700x700")
        self.main_color_dict = {"COLOR_1": "white", "COLOR_2": "black"}
        self.counter_dict = {"AI_1": Screen.NONE_PLAY,
                             "AI_2": Screen.NONE_PLAY}
        self.frames = {}
        for page in (GamePage, StartPage):
            frame = page(self.container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(page)

    def get_frame(self, cont):
        """This method returns the frames value"""
        return self.frames[cont]

    def show_frame(self, cont):
        """This is for switching frames"""
        frame = self.frames[cont]
        frame.tkraise()

    def main(self):
        """This is the mainloop"""
        self.mainloop()


###############################################################################
# CLASS StartPage
###############################################################################


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.create_main_menu()
        self.counter_dict = {self.ai_button_1: Screen.NONE_PLAY,
                             self.ai_button_2: Screen.NONE_PLAY}
        self.main_color_dict = {"COLOR_1": "white", "COLOR_2": "black"}
        self.color_dict_1 = {self.white: 0, self.red: 0, self.green: 0}
        self.color_dict_2 = {self.black: 0, self.yellow: 0, self.pink: 0}
        self.color_dict = {self.white: "antique white", self.red: "red",
                           self.green: "green4", self.black: "black",
                           self.yellow: "orange", self.pink: "deeppink2"}

    def create_main_menu(self):
        """
        This function creates main menu.
        """
        self.canvas = tk.Canvas(self, height=700, widt=700, bg="orange2")
        self.canvas.pack()
        self.welcome_msg = self.canvas.create_text(340, 50,
                                                   text="\nWelcome to", font=MEDIUM_FONT)
        self.welcome_msg_blue = self.canvas.create_text(340, 120,
                                                        text="CONNECT FOUR\n", font=LARGE_FONT,
                                                        fill="medium blue")
        self.menu_title = self.canvas.create_text(350, 185,
                                                  text="Choose how you want to play:\n\n", font=SMALL_FONT)

        self.player_one = self.canvas.create_text(160, 230, text="Player 1\n",
                                                  font=MEDIUM_FONT)
        self.human_button_1 = tk.Button(self, text="Human player",
                                        bg="medium blue", fg="white", command=lambda:
            self.change_button_color_human_1(self.human_button_1))
        self.human_button_1_window = self.canvas.create_window(155, 263,
                                                               window=self.human_button_1)
        self.ai_button_1 = tk.Button(self, text="AI player",
                                     bg="red3", command=lambda:
            self.change_button_color_ai_1(self.ai_button_1))
        self.ai_button_1_window = self.canvas.create_window(153, 300,
                                                            window=self.ai_button_1)

        self.player_two = self.canvas.create_text(540, 230, text="Player 2\n",
                                                  font=MEDIUM_FONT)
        self.human_button_2 = tk.Button(self, text="Human player",
                                        bg="medium blue", fg="white", command=lambda:
            self.change_button_color_human_2(self.human_button_2))
        self.human_button_2_window = self.canvas.create_window(540, 263,
                                                               window=self.human_button_2)
        self.ai_button_2 = tk.Button(self, text="AI player",
                                     bg="red3", command=lambda:
            self.change_button_color_ai_2(self.ai_button_2))
        self.ai_button_2_window = self.canvas.create_window(540, 300,
                                                            window=self.ai_button_2)
        self.choose_color = self.canvas.create_text(350, 440,
                                                    text="Please choose one colour for each player:\n\n\n\n\n\n",
                                                    font=SMALL_FONT)
        self.create_color_buttons()
        self.play_button = tk.Button(self, text="PLAY", bg="red", font="bold",
                                     width=10, command=lambda: self.if_play_pressed())
        self.play_button_window = self.canvas.create_window(333, 510,
                                                            window=self.play_button)

    def choose_ai_or_human_player(self):
        """
        This function checks which button was pressed, and returns True/None
        True for AI, None for human.
        :return: True/None
        """
        if self.counter_dict[self.ai_button_1] == Screen.AI_PLAY:
            self.controller.counter_dict["AI_1"] = Screen.AI_PLAY
        else:
            self.controller.counter_dict["AI_1"] = Screen.PLAYER_PLAY
        if self.counter_dict[self.ai_button_2] == Screen.AI_PLAY:
            self.controller.counter_dict["AI_2"] = Screen.AI_PLAY
        else:
            self.controller.counter_dict["AI_2"] = Screen.PLAYER_PLAY

    def change_button_color_ai_1(self, button):
        """
        This method changes the color of the button user choose
        """
        if self.counter_dict[button] == Screen.NONE_PLAY:
            button.configure(bg="white", fg="black")
            self.counter_dict[button] = Screen.AI_PLAY
        elif self.counter_dict[button] == Screen.PLAYER_PLAY:
            button.configure(bg="white", fg="black")
            self.human_button_1.configure(bg="medium blue", fg="white")
            self.counter_dict[button] = Screen.AI_PLAY

    def change_button_color_ai_2(self, button):
        """
        This method changes the color of the button user choose
        """
        if self.counter_dict[button] == Screen.NONE_PLAY:
            button.configure(bg="white", fg="black")
            self.counter_dict[button] = Screen.AI_PLAY
        elif self.counter_dict[button] == Screen.PLAYER_PLAY:
            button.configure(bg="white", fg="black")
            self.human_button_2.configure(bg="medium blue", fg="white")
            self.counter_dict[button] = Screen.AI_PLAY

    def change_button_color_human_1(self, button):
        """
        This method changes the color of the button user choose
        """
        if self.counter_dict[self.ai_button_1] == Screen.NONE_PLAY:
            button.configure(bg="white", fg="black")
            self.counter_dict[self.ai_button_1] = Screen.PLAYER_PLAY
        elif self.counter_dict[self.ai_button_1] == Screen.AI_PLAY:
            button.configure(bg="white", fg="black")
            self.ai_button_1.config(bg="red3")
            self.counter_dict[self.ai_button_1] = Screen.PLAYER_PLAY

    def change_button_color_human_2(self, button):
        """
        This method changes the color of the button user choose
        """
        if self.counter_dict[self.ai_button_2] == Screen.NONE_PLAY:
            button.configure(bg="white", fg="black")
            self.counter_dict[self.ai_button_2] = Screen.PLAYER_PLAY

        if self.counter_dict[self.ai_button_2] == Screen.AI_PLAY:
            button.configure(bg="white", fg="black")
            self.ai_button_2.configure(bg="red3")
            self.counter_dict[self.ai_button_2] = Screen.PLAYER_PLAY

    def if_play_pressed(self):
        """
        This method controls what happens when a user presses "play" button.
        """

        if self.counter_dict[self.ai_button_1] == Screen.NONE_PLAY:
            tkinter.messagebox.showinfo("ERROR", "You have to choose an"
                                                 " option for player 1")
        elif self.counter_dict[self.ai_button_2] == Screen.NONE_PLAY:
            tkinter.messagebox.showinfo("ERROR", "You have to choose an"
                                                 " option for player 2")
        else:
            self.color_chosen(self.color_dict_1, "white", "COLOR_1")
            self.color_chosen(self.color_dict_2, "black", "COLOR_2")
            self.choose_ai_or_human_player()
            self.controller.show_frame(GamePage)
            self.show_whos_playing()

    def show_whos_playing(self):
        """
        This method will change GamePage properties according to who will play
        ai or human
        """
        if self.controller.counter_dict["AI_1"] == Screen.AI_PLAY and \
                self.controller.counter_dict[
                    "AI_2"] == Screen.AI_PLAY:
            self.controller.get_frame(GamePage).change_main_menu_val()
            self.controller.get_frame(GamePage).its_ai_vs_ai(260, 560)
            self.controller.get_frame(GamePage).ai_vs_ai()

        if self.controller.counter_dict["AI_1"] == Screen.AI_PLAY and \
                self.controller.counter_dict[
                    "AI_2"] == Screen.PLAYER_PLAY:
            ai = AI(self.controller.get_frame(GamePage).game, WHITE)
            column_from_ai = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
            self.controller.get_frame(GamePage).player_move(
                self.controller.get_frame(GamePage).game.make_move(column_from_ai),
                "COLOR_1")
            self.controller.get_frame(GamePage).its_you_or_ai(220, 560)
        if self.controller.counter_dict["AI_1"] == Screen.PLAYER_PLAY and \
                self.controller.counter_dict[
                    "AI_2"] == Screen.PLAYER_PLAY:
            self.controller.get_frame(GamePage).its_your_turn(260)
        if self.controller.counter_dict["AI_1"] == Screen.PLAYER_PLAY and \
                self.controller.counter_dict[
                    "AI_2"] == Screen.AI_PLAY:
            self.controller.get_frame(GamePage).its_you_or_ai(520, 260)

    ###############################################################################
    # COLOR RELATED FITCHERS
    ###############################################################################

    def create_color_buttons(self):
        """
        This function creates color buttons for the main menu
        """
        self.white = tk.Button(self, bg="antique white", text="white",
                               command=lambda: self.choose_white(self.white,
                                                                 "antique white"))

        self.white_window = self.canvas.create_window(103, 432,
                                                      window=self.white)
        self.red = tk.Button(self, bg="red", text="red",
                             command=lambda: self.choose_red(self.red, "red"))
        self.red_window = self.canvas.create_window(158, 432, window=self.red)
        self.green = tk.Button(self, bg="green4", text="green",
                               command=lambda: self.choose_green(self.green, "green4"))
        self.green_window = self.canvas.create_window(215, 432,
                                                      window=self.green)
        self.black = tk.Button(self, bg="black", fg="white", text="black",
                               command=lambda: self.choose_black(self.black, "black"))
        self.black_window = self.canvas.create_window(482, 432,
                                                      window=self.black)
        self.yellow = tk.Button(self, bg="orange", text="yellow",
                                command=lambda: self.choose_yellow(self.yellow, "orange"))
        self.yellow_window = self.canvas.create_window(545, 432,
                                                       window=self.yellow)
        self.pink = tk.Button(self, bg="deeppink2", text="pink",
                              command=lambda: self.choose_pink(self.pink, "deeppink2"))
        self.pink_window = self.canvas.create_window(605, 432, window=self.pink)

    def choose_black(self, button, color):
        """This method is for choosing black"""
        if not self.color_dict_2[button] % 2:
            button.configure(bg="white", fg="black")
            self.yellow.configure(bg="orange")
            self.pink.configure(bg="deeppink2")
            self.color_dict_2[self.yellow] = 0
            self.color_dict_2[self.pink] = 0
            self.color_dict_2[button] = 1

    def choose_yellow(self, button, color):
        """This method is for choosing yellow"""
        if not self.color_dict_2[button] % 2:
            button.configure(bg="white", fg="black")
            self.black.configure(bg="black", fg="white")
            self.pink.configure(bg="deeppink2")
            self.color_dict_2[self.black] = 0
            self.color_dict_2[self.pink] = 0
            self.color_dict_2[button] = 1

    def choose_pink(self, button, color):
        """This method is for choosing pink"""
        if not self.color_dict_2[button] % 2:
            button.configure(bg="white", fg="black")
            self.yellow.configure(bg="orange")
            self.black.configure(bg="black", fg="white")
            self.color_dict_2[self.yellow] = 0
            self.color_dict_2[self.black] = 0
            self.color_dict_2[button] = 1

    def choose_white(self, button, color):
        """This method is for choosing white"""
        if not self.color_dict_1[button] % 2:
            button.configure(bg="white", fg="black")
            self.red.configure(bg="red")
            self.green.configure(bg="green4")
            self.color_dict_1[self.green] = 0
            self.color_dict_1[self.red] = 0
            self.color_dict_1[button] = 1

    def choose_red(self, button, color):
        """This method is for choosing red"""
        if not self.color_dict_1[button] % 2:
            button.configure(bg="white", fg="black")
            self.white.configure(bg="antique white")
            self.green.configure(bg="green4")
            self.color_dict_1[self.green] = 0
            self.color_dict_1[self.white] = 0
            self.color_dict_1[button] = 1

    def choose_green(self, button, color):
        """This method is for choosing green"""
        if not self.color_dict_1[button] % 2:
            button.configure(bg="white", fg="black")
            self.red.configure(bg="red")
            self.white.configure(bg="antique white")
            self.color_dict_1[self.white] = 0
            self.color_dict_1[self.red] = 0
            self.color_dict_1[button] = 1

    def color_chosen(self, color_dict_num, defult_color, change):
        """
        This method changes the color in the dictionary in class Screen
        """
        for key, val in color_dict_num.items():
            if val == 1:
                self.controller.main_color_dict[change] = self.color_dict[key]
            if all(value == 0 for value in color_dict_num.values()):
                self.controller.main_color_dict[change] = defult_color


###############################################################################
# GAMEPAGE
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
        self.checkers_lst = []
        self.turn_lst = []
        self.winning_lst = []
        self.last_ai_lst = []
        self.create_game_screen()
        self.canvas.bind("<Button-1>", self.return_column)
        self.__check_winner = True
        self.__main_menu = False

    ###############################################################################
    # CREATE GAME SCREEN
    ###############################################################################

    def create_game_screen(self):
        """
        This method draws the game screen
        """
        self.board = self.canvas.create_rectangle(1, 700, 700, 100,
                                                  fill="blue4", tag="board")
        self._draw_holes()
        self.create_game_screen_buttons()
        self.player_1 = self.canvas.create_text(110, 65, text="Player 1",
                                                font=MEDIUM_FONT, fill=self.controller.main_color_dict["COLOR_1"])
        self.player_2 = self.canvas.create_text(410, 65, text="Player 2",
                                                font=MEDIUM_FONT, fill=self.controller.main_color_dict["COLOR_2"])

    def create_game_screen_buttons(self):
        """
        This method creates the buttons in the game screen
        """
        self.button1 = tk.Button(self, text="Quit", command=self.quit_button,
                                 anchor="w")
        self.button1.configure(width=10, activebackground="red")
        self.button1_window = self.canvas.create_window(10, 10, anchor="nw",
                                                        window=self.button1)
        self.button2 = tk.Button(self, text="Main menu",
                                 command=self.main_menu_button, anchor="w")
        self.button2.configure(width=10, activebackground="blue")
        self.button2_window = self.canvas.create_window(100, 10, anchor="nw",
                                                        window=self.button2)
        self.button3 = tk.Button(self, text="Help", command=self.help_button,
                                 anchor="w")
        self.button3.configure(width=10, activebackground="blue")
        self.button3_window = self.canvas.create_window(200, 10, anchor="nw",
                                                        window=self.button3)

    def quit_button(self):
        """
        This method is binded to the quit button
        """
        msg = tkinter.messagebox.askquestion("QUIT", "Are you sure you want"
                                                     " to quit?")
        if msg == "yes":
            self.controller.destroy()
        else:
            return

    def main_menu_button(self):
        """
        This method is binded to the main menu button
        """
        msg = tkinter.messagebox.askquestion("Main menu", "Are you sure you "
                                                          "want to go back to main menu? \n Every change you've made"
                                                          " will be lost")
        if msg == "yes":
            self.__main_menu = True
            for checker in self.checkers_lst:
                self.canvas.delete(checker)
            self.game = Game()
            self.delete_turn()
            self.delete_last_ai()
            self.controller.show_frame(StartPage)
        else:
            return

    def help_button(self):
        """
        This method is binded to the help button
        """
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
                self.hole = self.canvas.create_oval(
                    9 + i, 560 - j, 90 + i, 640 - j, fill="grey")

    ###############################################################################
    # PLAYER VS PLAYER
    ###############################################################################

    def return_column(self, event):
        """
        This method is activated when a human player is chosen

        """

        col_width = self.canvas.winfo_width() / COLUMNS
        col = int(event.x // col_width)

        try:
            if self.controller.counter_dict["AI_1"] == Screen.PLAYER_PLAY and \
                    self.controller.counter_dict["AI_2"] == Screen.PLAYER_PLAY:
                self.human_vs_human(col)
            if self.controller.counter_dict["AI_1"] == Screen.PLAYER_PLAY and \
                    self.controller.counter_dict["AI_2"] == Screen.AI_PLAY:
                self.human_vs_ai(col)
            if self.controller.counter_dict["AI_1"] == Screen.AI_PLAY and \
                    self.controller.counter_dict["AI_2"] == Screen.PLAYER_PLAY:
                self.ai_vs_human(col)

        except Exception:
            return

    def human_vs_human(self, col):
        """
        This method is activated if user chose to play human va human
        """
        if self.check_turn() == WHITE:
            self.delete_turn()
            self.its_your_turn(560)
            self.player_move(self.game.make_move(col), "COLOR_1")
        elif self.check_turn() == BLACK:
            self.delete_turn()
            self.its_your_turn(260)
            self.player_move(self.game.make_move(col), "COLOR_2")

    def human_vs_ai(self, col):
        """
        This method is activated if user chose to play human vs ai
        """
        if self.check_turn() == WHITE:
            self.player_move(self.game.make_move(col), "COLOR_1")
        if not self.__check_winner:
            return
        self.delete_last_ai()
        self.after(200, self.ai_black)

    def ai_black(self):
        ai = AI(self.game, BLACK)
        column_from_ai = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
        self.player_move(self.game.make_move(column_from_ai), "COLOR_2")

    def ai_vs_human(self, col):
        """
        This method is activated when robots are rising (and if user chose
        to play ai vs human.
        """
        if self.check_turn() == BLACK:
            self.player_move(self.game.make_move(col), "COLOR_2")
        self.delete_last_ai()
        self.after(200, self.ai_white)

    def ai_white(self):
        ai = AI(self.game, WHITE)
        column_from_ai = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
        self.player_move(self.game.make_move(column_from_ai), "COLOR_1")

    def ai_vs_ai(self):
        """
        This method is activeted if user chooses to play ai vs ai
        """
        if self.__main_menu:
            return
        if self.check_turn() == WHITE:
            ai = AI(self.game, WHITE)
            column_from_ai = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
            self.player_move(self.game.make_move(column_from_ai), "COLOR_1")
            self.after(1000, self.ai_vs_ai)
        elif self.check_turn() == BLACK:
            ai = AI(self.game, BLACK)
            column_from_ai = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
            self.player_move(self.game.make_move(column_from_ai), "COLOR_2")
            self.after(1000, self.ai_vs_ai)

    def change_main_menu_val(self):
        self.__main_menu = False

    def player_move(self, tuple, color):
        """
        This method is in charge of  a single move in the game.
        """
        y, x = tuple
        i = x * 100
        j = y * 90

        self.checkers_lst.append(
            self.canvas.create_oval(9 + i, 110 + j, 90 + i, 190 + j,
                                    fill=self.controller.main_color_dict[color]))
        if self.controller.counter_dict["AI_1"] == Screen.AI_PLAY and \
                self.controller.counter_dict["AI_2"] == Screen.PLAYER_PLAY:
            if self.check_turn() == BLACK:
                self.show_last_ai(tuple)
        elif self.controller.counter_dict["AI_1"] == Screen.PLAYER_PLAY and \
                self.controller.counter_dict["AI_2"] == Screen.AI_PLAY:
            if self.check_turn() == WHITE:
                self.show_last_ai(tuple)
        self.__check_winner = self.check_winner()
        return

    ###############################################################################
    # METHODS FOR ALL PLAYERS
    ###############################################################################

    def check_winner(self):
        """This method checks the state of the game"""
        if self.game.get_winner() == Game.TIE:
            self.WIN_message(TIE)
            return False
        if self.game.get_winner() == Game.WHITE_WINS:
            self.WIN_message(WHITE)
            return False
        if self.game.get_winner() == Game.BLACK_WINS:
            self.WIN_message(BLACK)
            return False
        if self.game.get_winner() == Game.GAME_IN_PROGRESS:
            return True

    def check_turn(self):
        """This method checks whos turn is it"""
        if self.game.get_current_player() == WHITE:
            return WHITE
        if self.game.get_current_player() == BLACK:
            return BLACK

    ###############################################################################
    # END OF GAME
    ###############################################################################

    def WIN_message(self, player):
        """This is what happened when the game is over. it calls the
        animation and shows a messagebox that tells who wins and if the
        player wants to play again"""
        if player == WHITE or player == BLACK:
            for i in range(4):
                self.show_winning_seq(self.game.winning_coordinate[i])
        if player == WHITE:
            text = "PLAYER 1, YOU WON! \n\nwant to play again?"
        if player == BLACK:
            text = "PLAYER 2, YOU WON! \n\nwant to play again?"
        if player == TIE:
            text = "INCREDIBLE TIE! \n\nwant to play again?"
        win_message = tkinter.messagebox.askquestion("Game over", text)
        self.delete_turn()
        self.delete_last_ai()
        self.delete_winning_four()
        [self.animation() for _ in range(7)]
        if win_message == "yes":
            for checker in self.checkers_lst:
                self.canvas.delete(checker)
            self.game = Game()
            self.who_vs_who()
        else:
            self.controller.destroy()

    def who_vs_who(self):
        """This method shows if the player is ai or human in a new game"""
        if self.controller.counter_dict["AI_1"] == Screen.PLAYER_PLAY and \
                self.controller.counter_dict[
                    "AI_2"] == Screen.PLAYER_PLAY:
            self.its_your_turn(260)
        elif self.controller.counter_dict["AI_1"] == Screen.AI_PLAY and \
                self.controller.counter_dict[
                    "AI_2"] == Screen.PLAYER_PLAY:
            self.its_you_or_ai(220, 560)
        elif self.controller.counter_dict["AI_1"] == Screen.PLAYER_PLAY and \
                self.controller.counter_dict[
                    "AI_2"] == Screen.AI_PLAY:
            try:
                self.return_column(self, event)
                self.its_you_or_ai(520, 260)
            except NameError:
                self.its_you_or_ai(520, 260)
        elif self.controller.counter_dict["AI_1"] == Screen.AI_PLAY and \
                self.controller.counter_dict[
                    "AI_2"] == Screen.AI_PLAY:
            self.its_ai_vs_ai(560, 260)

    def animation(self):
        """
        This is the animation that happens when a player wins or when its
         a tie
         """
        try:
            for checker in self.checkers_lst:
                self.canvas.move(checker, random.randint(-400, 400),
                                 random.randint(-400, 400))
                self.update()
                self.after(10)
        except:
            return

    def show_winning_seq(self, coor):
        """This metod shows the winning sequal"""
        y, x = coor
        i = x * 100
        j = y * 90
        self.winning_lst.append(
            self.canvas.create_oval(9 + i, 110 + j, 90 + i, 190 + j,
                                    outline="dark violet", width="10"))

    def delete_winning_four(self):
        """This method deletes the winning sequal"""
        for win in self.winning_lst:
            self.canvas.delete(win)

    ###############################################################################
    # EXSTRAS I MADE COUSE IM OBSSESD
    ###############################################################################

    def its_your_turn(self, x):
        """This method creates text that says whos turn is it"""
        self.turn_lst.append(self.canvas.create_text(x, 67,
                                                     text="It's your turn!", font=SMALL_FONT, fill="medium blue"))

    def its_you_or_ai(self, x, y):
        """
        This method creates text that says whos turn is it
        """
        self.turn_lst.append(self.canvas.create_text(x, 67, text="AI",
                                                     font=SMALL_FONT, fill="medium blue"))
        self.turn_lst.append(self.canvas.create_text(y, 67, text="That's you!",
                                                     font=SMALL_FONT, fill="medium blue"))

    def its_ai_vs_ai(self, x, y):
        """
        This method creates text that says whos turn is it
        """
        self.turn_lst.append(self.canvas.create_text(x, 67, text="AI",
                                                     font=SMALL_FONT, fill="medium blue"))
        self.turn_lst.append(self.canvas.create_text(y, 67, text="AI",
                                                     font=SMALL_FONT, fill="medium blue"))

    def delete_turn(self):
        """
        This method deletes the text thst saya whos turn is it
        """
        for turn in self.turn_lst:
            self.canvas.delete(turn)

    def show_last_ai(self, coor):
        y, x = coor
        i = x * 100
        j = y * 90
        self.last_ai_lst.append(
            self.canvas.create_oval(9 + i, 110 + j, 90 + i, 190 + j,
                                    outline="blue", width="10"))

    def delete_last_ai(self):

        for last in self.last_ai_lst:
            self.canvas.delete(last)
