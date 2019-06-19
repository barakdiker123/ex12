import tkinter as tk
import tkinter.messagebox
from game import *
import numpy as np

LARGE_FONT = ("Verdana bold", 24)
MEDIUM_FONT = ("Verdana bold", 18)
SMALL_FONT = ("Verdana bold", 14)

WHITE = 1
BLACK = 2


class Screen(tk.Tk):

    def __init__(self, game):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(fill="both")
        container_2 = tk.Frame(self)
        container_2.pack(fill="both")
        self.geometry("700x700")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.main_color_dict = {"COLOR_1": "white", "COLOR_2": "black"}
        self.main_player_dict = {"ai_player_1": 0, "ai_player_2": 0, "human_player_1": 0, "human_player_2": 0}
        self.frames = {}
        for page in (GamePage, StartPage):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(page)
        self.game = game

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.welcome_msg = tk.Label(self, text="\nWelcome to", font=MEDIUM_FONT, bg="orange2")
        self.welcome_msg.pack()
        self.label = tk.Label(self, text="CONNECT FOUR\n", font=LARGE_FONT, bg="orange2", fg="medium blue")
        self.label.pack()
        self.menu_title = tk.Label(self, text="Choose how you want to play:\n\n", font=SMALL_FONT, bg="orange2")
        self.menu_title.pack()
        self.player_one_label = tk.Label(self, text="Player 1\n", font=MEDIUM_FONT, bg="orange2").place(x=100, y=200)
        self.human_button_1 = tk.Button(self, text="Human player", bg="medium blue", fg="white",
                                        command=lambda: self.change_button_color_human(self.human_button_1))
        self.human_button_1.place(x=110, y=250)
        self.ai_button_1 = tk.Button(self, text="AI player", bg="red3",
                                     command=lambda: self.change_button_color_ai(self.ai_button_1))
        self.ai_button_1.place(x=123, y=280)
        self.empty_label_1 = tk.Label(self, bg="orange2", text="\n")
        self.empty_label_1.pack()
        self.player_two_label = tk.Label(self, text="Player 2\n", font=MEDIUM_FONT, bg="orange2").place(x=480, y=200)
        self.human_button_2 = tk.Button(self, text="Human player", bg="medium blue", fg="white",
                                        command=lambda: self.change_button_color_human(self.human_button_2))
        self.human_button_2.place(x=490, y=250)
        self.ai_button_2 = tk.Button(self, text="AI player", bg="red3",
                                     command=lambda: self.change_button_color_ai(self.ai_button_2))
        self.ai_button_2.place(x=503, y=280)
        self.empty_label_2 = tk.Label(self, bg="orange2", text="\n\n\n\n\n").pack()
        self.choose_color = tk.Label(self, bg="orange2", text="Please choose one colour for each player:\n\n\n\n\n\n",
                                     font=SMALL_FONT).pack()
        self.white = tk.Button(self, bg="antique white", text="white",
                               command=lambda: self.choose_color_1(self.white, "antique white"))
        self.white.place(x=96, y=420)
        self.red = tk.Button(self, bg="red", text="red", command=lambda: self.choose_color_1(self.red, "red"))
        self.red.place(x=141, y=420)
        self.green = tk.Button(self, bg="green4", text="green",
                               command=lambda: self.choose_color_1(self.green, "green4"))
        self.green.place(x=174, y=420)
        self.black = tk.Button(self, bg="black", fg="white", text="black",
                               command=lambda: self.choose_color_2(self.black, "black"))
        self.black.place(x=476, y=420)
        self.yellow = tk.Button(self, bg="orange", text="yellow",
                                command=lambda: self.choose_color_2(self.yellow, "orange"))
        self.yellow.place(x=520, y=420)
        self.pink = tk.Button(self, bg="deep pink2", text="pink",
                              command=lambda: self.choose_color_2(self.pink, "deep pink2"))
        self.pink.place(x=570, y=420)
        self.play_button = tk.Button(self, text="PLAY", bg="red", font="bold", width=10, command=self.if_play_pressed)
        self.play_button.pack()
        self.configure(bg="orange2")
        self.counter_dict = {self.ai_button_1: 0, self.ai_button_2: 0, self.human_button_1: 0, self.human_button_2: 0}
        self.counter_dict_2 = {self.ai_button_1: "ai_player_1", self.ai_button_2: "ai_player_2",
                               self.human_button_1: "human_player_1", self.human_button_2: "human_player_2"}
        self.color_dict_1 = {self.white: 0, self.red: 0, self.green: 0}
        self.color_dict_2 = {self.black: 0, self.yellow: 0, self.pink: 0}
        self.color_dict = {self.white: "antique white", self.red: "red", self.green: "green4", self.black: "black",
                           self.yellow: "orange", self.pink: "deep pink2"}

    def choose_ai_or_human_player(self):
        for player in self.counter_dict:
            if self.counter_dict == 1:
                self.controller.main_player_dict[self.color_dict_2[player]] = 1

    def change_button_color_ai(self, button):
        """
        This method changes the color of the button user choose
        """
        if not self.counter_dict[button] % 2:
            button.configure(bg="white", fg="black")
        else:
            button.config(bg="red3")
        self.counter_dict[button] += 1

    def change_button_color_human(self, button):
        """
        This method changes the color of the button user choose
        """
        if not self.counter_dict[button] % 2:
            button.configure(bg="white", fg="black")
        else:
            button.config(bg="medium blue", fg="white")
        self.counter_dict[button] += 1

    def if_play_pressed(self):
        """
        This method controls what happens when a user presses "play" button.
        """
        if self.counter_dict[self.human_button_1] % 2 and self.counter_dict[self.ai_button_1] % 2:
            tkinter.messagebox.showinfo("ERROR", "You can choose either human or AI player, not both")
        elif self.counter_dict[self.human_button_2] % 2 and self.counter_dict[self.ai_button_2] % 2:
            tkinter.messagebox.showinfo("ERROR", "You can choose either human or AI player, not both")
        elif not self.counter_dict[self.human_button_1] % 2 and not self.counter_dict[self.ai_button_1] % 2:
            tkinter.messagebox.showinfo("ERROR", "You have to choose an option for player 1")
        elif not self.counter_dict[self.human_button_2] % 2 and not self.counter_dict[self.ai_button_2] % 2:
            tkinter.messagebox.showinfo("ERROR", "You have to choose an option for player 2")
        else:
            self.color_chosen(self.color_dict_1, "white", "COLOR_1")
            self.color_chosen(self.color_dict_2, "black", "COLOR_2")
            self.choose_ai_or_human_player()
            self.controller.show_frame(GamePage)

    def choose_color_1(self, button, color):
        if not self.color_dict_1[button] % 2:
            button.configure(bg="white", fg="black")
            self.color_dict_1[button] = 1
        else:
            button.config(bg=color)
            self.color_dict_1[button] = 0

    def color_chosen(self, color_dict_num, defult_color, change):
        for button in color_dict_num:
            if color_dict_num[button] == 1:
                self.controller.main_color_dict[change] = self.color_dict[button]
            if all(value == 0 for value in color_dict_num.values()):
                self.controller.main_color_dict[change] = defult_color
        rev_dict = {}
        for key, value in color_dict_num.items():
            rev_dict.setdefault(value, set()).add(key)
        result = [key for key, values in rev_dict.items()
                  if len(values) > 1]
        if result == [1]:
            if color_dict_num == self.color_dict_1:
                tkinter.messagebox.showinfo("Notice",
                                            "You chose more than one color for Player 1,\nso the pogram will choose one of them for you")
            if color_dict_num == self.color_dict_2:
                tkinter.messagebox.showinfo("Notice",
                                            "You chose more than one color for Player 2,\nso the pogram will choose one of them for you")

    def choose_color_2(self, button, color):
        if not self.color_dict_2[button] % 2:
            button.configure(bg="white", fg="black")
            self.color_dict_2[button] = 1
        else:
            button.config(bg=color)
            self.color_dict_2[button] = 0


class GamePage(tk.Frame):
    num_of_columns = 7
    num_of_rows = 7
    WHITE = 1
    BLACK = 2

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.make_move_value = True
        self.canvas = tk.Canvas(self, height=700, widt=700)
        self.canvas.pack()
        button1 = tk.Button(self, text="Quit", command=self.quit_button, anchor="w")
        button1.configure(width=10, activebackground="red")
        button1_window = self.canvas.create_window(10, 10, anchor="nw", window=button1)
        button2 = tk.Button(self, text="Main menu", command=self.main_menu_buton, anchor="w")
        button2.configure(width=10, activebackground="blue")
        button2_window = self.canvas.create_window(100, 10, anchor="nw", window=button2)
        button3 = tk.Button(self, text="Help", command=self.help_button, anchor="w")
        button3.configure(width=10, activebackground="blue")
        button3_window = self.canvas.create_window(190, 10, anchor="nw", window=button3)
        self.player_1 = tk.Label(self, text="Player 1:", font=MEDIUM_FONT, bg="grey",
                                 fg=self.controller.main_color_dict["COLOR_1"]).place(x=50, y=50)
        self.player_1 = tk.Label(self, text="Player 2:", font=MEDIUM_FONT, bg="grey",
                                 fg=self.controller.main_color_dict["COLOR_2"]).place(x=350, y=50)
        self.disc_canvas = tk.Canvas(self)
        self.disc_canvas.pack()
        # self.canvas.bind("<Button-1>", self.callback)
        #self.canvas.bind("<Motion>", self.ai_or_human)
        self.canvas.bind("<Button-1>", self.return_location)
        self.board = self.canvas.create_rectangle(1, 700, 700, 100, fill="blue4")
        self.outside = self.canvas.create_rectangle(1, 100, 700, 1, fill="grey")
        self._draw_holes()
        self.val = 0
        self.checkers_lst = []
        self.turn_lst = []
        self.show_turn()

    def show_turn(self):
        if self.val % 2 == 0:
            for turn in self.turn_lst:
                self.turn_lst.remove(turn)
            self.turn_lst.append(tk.Label(self, text="It's your turn!", font=SMALL_FONT, bg="grey").place(x=180, y=55))
        if self.val % 2 != 0:
            for turn in self.turn_lst:
                self.turn_lst.remove(turn)
            self.turn_lst.append(tk.Label(self, text="It's your turn!", font=SMALL_FONT, bg="grey").place(x=380, y=55))

    def quit_button(self):
        msg = tkinter.messagebox.askquestion("QUIT", "Are you sure you want to quit?")
        if msg == "yes":
            self.controller.destroy()
        else:
            return

    def main_menu_buton(self):
        msg = tkinter.messagebox.askquestion("Main menu", "Are you sure you "
                                                          "want to go back to main menu? \n Every change you've made will be lost")
        if msg == "yes":
            for checker in self.checkers_lst:
                self.canvas.delete(checker)
            self.controller.game = Game()
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

    def callback(self, event):
        """
        This method prints the col and the row of circle in the board
        """
        col_width = self.canvas.winfo_width() / self.num_of_columns
        row_height = self.canvas.winfo_height() / self.num_of_rows
        col = int(event.x // col_width)
        row = int(event.y // row_height)
        print("col:" + str(col) + "," + "row:" + str(row - 1))

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
            self.val += 1
        elif self.check_turn() == BLACK:
            self.checkers_lst.append(self.canvas.create_oval(9 + i, 110 + j, 90 + i, 190 + j,
                                                             fill=self.controller.main_color_dict["COLOR_2"]))
            self.val += 1
        self.check_winner()

    def return_location(self,event):
        """
        This method returns the location of the mouse in the board as a tuple.
        The numbers represents the location in the matrix this cell is.
        """
        col_width = self.canvas.winfo_width() / self.num_of_columns
        # row_height = self.canvas.winfo_height() / self.num_of_rows
        col = int(event.x // col_width)
        # row = int(event.y // row_height)
        if self.make_move_value == True:
            self.player_move(self.controller.game.make_move(col))



    def check_winner(self):
        if self.controller.game.get_winner() == Game.TIE:
            print("Tie")
            self.make_move_value = False
        if self.controller.game.get_winner() == Game.WHITE_WINS:
            print("WHITE WON")
            self.make_move_value = False
        if self.controller.game.get_winner() == Game.BLACK_WINS:
            print("BLACK WON")
            self.make_move_value = False
        if self.controller.game.get_winner() == Game.GAME_IN_PROGRESS:
            print("PROGRESS...")
            self.make_move_value = True

    def check_turn(self):
        if self.controller.game.get_current_player() == Board.WHITE:
            return WHITE
        if self.controller.game.get_current_player() == Board.BLACK:
            return BLACK



root = Screen(Game())
root.mainloop()
