import tkinter as tk
import tkinter.messagebox
from game import *
import numpy as np
from ai import *
from ai_or_human import *
from board import *
import random

LARGE_FONT = ("Verdana bold", 24)
MEDIUM_FONT = ("Verdana bold", 18)
SMALL_FONT = ("Verdana bold", 14)

#################################################
# CANT FIGURE OUT WHY BLACK COME FIRST
#################################################

WHITE = 1
BLACK = 2
TIE = 0

COLUMNS = 7

HUMAN_VS_HUMAN = 10
HUMAN_VS_AI = 20
AI_VS_HUMAN = 30
AI_VS_AI = 40


class Screen(tk.Tk):
    AI_PLAY = True
    PLAYER_PLAY = None
    NONE_PLAY = False
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
            frame = page(self.container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(page)
        self.game = game



    def get_frame(self,cont):
        """This method returns the frames value"""
        return self.frames[cont]


    def show_frame(self, cont):
        """This is for switching frames"""
        frame = self.frames[cont]
        frame.tkraise()

    def main(self):
        """This is the mainloop"""
        self.mainloop()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
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
        self.choose_color = self.canvas.create_text(350, 440,
                                                    text="Please choose one colour for each player:\n\n\n\n\n\n",
                                                    font=SMALL_FONT)
        self.create_color_buttons()
        play_button = tk.Button(self, text="PLAY", bg="red", font="bold", width=10,
                                command=lambda: self.if_play_pressed())
        play_button_window = self.canvas.create_window(333, 510, window=play_button)

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
            if self.controller.counter_dict["AI_1"] == Screen.AI_PLAY and self.controller.counter_dict[
                "AI_2"] == Screen.AI_PLAY:
                tkinter.messagebox.showinfo("INSTRUCTIONS", "Press any spot on the board to watch a single AI move")
            self.controller.show_frame(GamePage)
            if self.controller.counter_dict["AI_1"] == Screen.AI_PLAY and self.controller.counter_dict["AI_2"] == Screen.PLAYER_PLAY:
                ai = AI(self.controller.get_frame(GamePage).game, WHITE)
                column_from_ai = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
                self.controller.get_frame(GamePage).player_move(self.controller.get_frame(GamePage).game.make_move(column_from_ai), "COLOR_1")
            if self.controller.counter_dict["AI_1"] == Screen.PLAYER_PLAY and self.controller.counter_dict[
                "AI_2"] == Screen.PLAYER_PLAY:
                self.controller.get_frame(GamePage).its_your_turn(260)





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
        """This method is for choosing black"""
        if not self.color_dict_2[button] % 2:
            button.configure(bg="white", fg="black")
            self.yellow.configure(bg="orange")
            self.pink.configure(bg="deep pink2")
            self.color_dict_2[self.yellow] = 0
            self.color_dict_2[self.pink] = 0
            self.color_dict_2[button] = 1

    def choose_yellow(self, button, color):
        """This method is for choosing yellow"""
        if not self.color_dict_2[button] % 2:
            button.configure(bg="white", fg="black")
            self.black.configure(bg="black", fg="white")
            self.pink.configure(bg="deep pink2")
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
        """This method changes the color in the dictionary in class Screen"""
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
        self.create_game_screen()
        self.canvas.bind("<Button-1>", self.return_column)


    ###############################################################################
    # CREATE GAME SCREEN
    ###############################################################################

    def create_game_screen(self):
        """This method draws the game screen"""
        self.board = self.canvas.create_rectangle(1, 700, 700, 100, fill="blue4", tag="board")
        self._draw_holes()
        self.create_game_screen_buttons()
        self.player_1 = self.canvas.create_text(110, 65, text="Player 1", font=MEDIUM_FONT,
                                                fill=self.controller.main_color_dict["COLOR_1"])
        self.player_2 = self.canvas.create_text(410, 65, text="Player 2", font=MEDIUM_FONT,
                                                fill=self.controller.main_color_dict["COLOR_2"])



    def create_game_screen_buttons(self):
        """This method creates the buttons in the game screen"""
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
        """This method is binded to the quit button"""
        msg = tkinter.messagebox.askquestion("QUIT", "Are you sure you want to quit?")
        if msg == "yes":
            self.controller.destroy()
        else:
            return

    def main_menu_buton(self):
        """This method is binded to the main menu button"""
        msg = tkinter.messagebox.askquestion("Main menu", "Are you sure you "
                                                          "want to go back to main menu? \n Every change you've made will be lost")
        if msg == "yes":
            for checker in self.checkers_lst:
                self.canvas.delete(checker)
            self.game = Game()
            self.delete_turn()
            self.controller.show_frame(StartPage)
        else:
            return

    def help_button(self):
        """This method is binded to the help button"""
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
        """
        This method is activated when a human player is chosen

        """

        col_width = self.canvas.winfo_width() / COLUMNS
        col = int(event.x // col_width)

        try:
            if self.controller.counter_dict["AI_1"] == Screen.PLAYER_PLAY and self.controller.counter_dict["AI_2"] == Screen.PLAYER_PLAY:
                if self.check_turn() == WHITE:
                    self.delete_turn()
                    self.its_your_turn(560)
                    self.player_move(self.game.make_move(col), "COLOR_1")
                elif self.check_turn() == BLACK:
                    self.delete_turn()
                    self.its_your_turn(260)
                    self.player_move(self.game.make_move(col), "COLOR_2")
            if self.controller.counter_dict["AI_1"] == Screen.PLAYER_PLAY and self.controller.counter_dict["AI_2"] == Screen.AI_PLAY:

                if self.check_turn() == WHITE:
                    self.player_move(self.game.make_move(col), "COLOR_1")
                self.after(200)

                ai = AI(self.game, BLACK)
                column_from_ai = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
                self.player_move(self.game.make_move(column_from_ai), "COLOR_2")

            if self.controller.counter_dict["AI_1"] == Screen.AI_PLAY and self.controller.counter_dict["AI_2"] == Screen.PLAYER_PLAY:

                if self.check_turn() == BLACK:
                    self.player_move(self.game.make_move(col), "COLOR_2")
                    self.after(200)

                ai = AI(self.game, WHITE)
                column_from_ai = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
                self.player_move(self.game.make_move(column_from_ai), "COLOR_1")

            if self.controller.counter_dict["AI_1"] == Screen.AI_PLAY and self.controller.counter_dict["AI_2"] == Screen.AI_PLAY:

                if self.check_turn() == WHITE:
                    ai = AI(self.game, WHITE)
                    column_from_ai = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
                    self.player_move(self.game.make_move(column_from_ai), "COLOR_1")
                elif self.check_turn() == BLACK:
                    ai = AI(self.game, BLACK)
                    column_from_ai = ai.find_legal_move(AI.FAST_ALGORITHM_TIMEOUT)
                    self.player_move(self.game.make_move(column_from_ai), "COLOR_2")



            if self.controller.counter_dict["AI_1"] == None and self.controller.counter_dict["AI_2"] == True:

                if self.check_turn() == WHITE:
                    self.playe_move(self.game.make_move(col))
                else:
                    self.AI_move(self.game.make_move(random.randint(0, 7)))
            if self.controller.counter_dict["AI_1"] == True and self.controller.counter_dict["AI_2"] == None:
                self.AI_vs_Human()



        except Exception:
            return



    def player_move(self, tuple, color):
        """
        This method is in charge of  a single move in the game.
        """
        y, x = tuple
        i = x * 100
        j = y * 90

        self.checkers_lst.append(self.canvas.create_oval(9 + i, 110 + j, 90 + i, 190 + j,
                                                         fill=self.controller.main_color_dict[color]))

        self.check_winner()
        return




    ###############################################################################
    # METHODS FOR ALL PLAYERS
    ###############################################################################

    def check_winner(self):
        """This method checks the state of the game"""
        if self.game.get_winner() == TIE:  ###################################### NOTICe!!!! DOESNT WORK NOT SURE IF IN GAME RULES
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
            print("white")
            # self.delete_turn()
            # self.its_your_turn(560)
            return WHITE
        if self.game.get_current_player() == BLACK:
            print("black")
            # self.delete_turn()
            # self.its_your_turn(260)
            return BLACK

    ###############################################################################
    # END OF GAME
    ###############################################################################

    def WIN_message(self, player):
        """This is what happened when the game is over. it calls the
        animation and shows a messagebox that tells who wins and if the
        player wants to play again"""
        self.show_winning_circles(self.define_start_or_end((0,0),(0,3)))
        self.delete_turn()
        if player == WHITE:
            text = "PLAYER 1, YOU WON! \n\nwant to play again?"
        if player == BLACK:
            text = "PLAYER 2, YOU WON! \n\nwant to play again?"
        if player == TIE:
            text == "INCREDIBLE TIE! \n\nwant to play again?"
        win_message = tkinter.messagebox.askquestion("WE HAVE A WINNER!", text)
        self.delete_winning_four()
        [self.animation() for _ in range(7)]
        if win_message == "yes":
            for checker in self.checkers_lst:
                self.canvas.delete(checker)
            if self.controller.counter_dict["AI_1"] == Screen.PLAYER_PLAY and self.controller.counter_dict[
                "AI_2"] == Screen.PLAYER_PLAY:
                self.controller.get_frame(GamePage).its_your_turn(260)
            self.game = Game()

        else:
            self.controller.destroy()



    def animation(self):
        """This is the animation that happens when a player wins or when its a tie"""
        for checker in self.checkers_lst:
            self.canvas.move(checker, random.randint(-400, 400), random.randint(-400, 400))
            self.update()
            self.after(10)



    def show_winning_circles(self, tuple):
        start, end = tuple
        y1, x1 = start
        i1 = x1 * 100
        j1 = y1 * 90

        y2, x2 = end
        i2 = x2 * 100
        j2 = y2 * 90

        self.winning_lst.append(self.canvas.create_oval(9 + i1, 110 + j1, 90 + i1, 190 + j1,
                                                         outline="purple", width="10"))

        self.winning_lst.append(self.canvas.create_oval(9 + i2, 110 + j2, 90 + i2, 190 + j2,
                                                         outline="purple",width="10"))
        if y1 == y2:
            i3 = (x1 + 1) * 100
            i4 = (x1 + 2) * 100

            self.winning_lst.append(self.canvas.create_oval(9 + i3, 110 + j1, 90 + i3, 190 + j1,
                                                            outline="purple", width="10"))

            self.winning_lst.append(self.canvas.create_oval(9 + i4, 110 + j1, 90 + i4, 190 + j1,
                                                            outline="purple", width="10"))

        if x1 == x2:
            j3 = (y1 + 1) * 90
            j4 = (y1 + 2) * 90

            self.winning_lst.append(self.canvas.create_oval(9 + i1, 110 + j3, 90 + i1, 190 + j3,
                                                            outline="purple", width="10"))

            self.winning_lst.append(self.canvas.create_oval(9 + i1, 110 + j4, 90 + i1, 190 + j4,
                                                            outline="purple", width="10"))
        elif x1 < x2 and y1 != y2:
            i3 = (x1 + 1) * 100
            i4 = (x1 + 2) * 100

            j3 = (y1 + 1) * 90
            j4 = (y1 + 2) * 90

            self.winning_lst.append(self.canvas.create_oval(9 + i3, 110 + j3, 90 + i3, 190 + j3,
                                                            outline="purple", width="10"))

            self.winning_lst.append(self.canvas.create_oval(9 + i4, 110 + j4, 90 + i4, 190 + j4,
                                                            outline="purple", width="10"))

        elif x1 > x2 and y1 != y2:
            i3 = (x1 - 1) * 100
            i4 = (x1 - 2) * 100

            j3 = (y1 + 1) * 90
            j4 = (y1 + 2) * 90

            self.winning_lst.append(self.canvas.create_oval(9 + i3, 110 + j3, 90 + i3, 190 + j3,
                                                            outline="purple", width="10"))

            self.winning_lst.append(self.canvas.create_oval(9 + i4, 110 + j4, 90 + i4, 190 + j4,
                                                            outline="purple", width="10"))


    def define_start_or_end(self, coor1, coor2):
        y1, x1 = coor1
        y2, x2 = coor2

        if y1 < y2:
            return coor1, coor2
        if y1 > y2:
            return coor2, coor1
        elif x1 < x2:
            return coor1, coor2
        elif x1 > x2:
            return coor2, coor1




    def delete_winning_four(self):
        for win in self.winning_lst:
            self.canvas.delete(win)

    ###############################################################################
    # EXSTRAS I MADE COUSE IM OBSSESD
    ###############################################################################

    def its_your_turn(self, x):
        """This method creates text that says whos turn is it"""
        self.turn_lst.append(
            self.canvas.create_text(x, 67, text="It's your turn!", font=SMALL_FONT, fill="medium blue"))

    def delete_turn(self):
        """This method deletes the text thst saya whos turn is it"""
        for turn in self.turn_lst:
            self.canvas.delete(turn)
