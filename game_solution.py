import tkinter as tk
from tkinter import *
from tkinter.font import Font
from random import *
import json
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox

# using leaderboard class for score handling and management


class Leaderboard:
    def __init__(self):
        self.scores = []    # empty list to store scores
        self.load_scores()  # load existing scores from file

    def load_scores(self):
        try:
            # opening leaderboard file in read mode
            with open("leaderboard.txt", "r") as file:
                # splitting each line by commas and removing extra spaces
                self.scores = [line.strip().split(",")
                               for line in file.readlines()]
        except FileNotFoundError:
            # if file is not found, set up scores as an empty list
            self.scores = []

    def save_scores(self):
        # writing current leaderboard scores into the file
        with open("leaderboard.txt", "w") as file:
            for name, score in self.scores:
                # write player's name and score to the file
                file.write(f"{name},{score}\n")

    def add_score(self, name, score):
        self.scores.append((name, score))   # add new scores to the leaderboard
        # sorting scores in desc order, x[1] refers to the second element of
        # each tuple
        self.scores.sort(key=lambda x: int(x[1]), reverse=True)
        self.scores = self.scores[:10]  # keeping only top 10 scores
        self.save_scores()  # saving updated leaderboard

    def show_leaderboard(self):
        # creating a new window to display leaderboard
        self.leaderboard_window = tk.Toplevel()
        self.leaderboard_window.title("Leaderboard")

        # creating labels for column headers
        tk.Label(
            self.leaderboard_window,
            text="Rank",
            font=(
                "Arial",
                16)).grid(
            row=0,
            column=0,
            padx=10,
            pady=5)
        tk.Label(
            self.leaderboard_window,
            text="Name",
            font=(
                "Arial",
                16)).grid(
            row=0,
            column=1,
            padx=10,
            pady=5)
        tk.Label(
            self.leaderboard_window,
            text="Score",
            font=(
                "Arial",
                16)).grid(
            row=0,
            column=2,
            padx=10,
            pady=5)

        # displaying each player's rank, name and score
        for i, (name, score) in enumerate(self.scores):
            tk.Label(
                self.leaderboard_window,
                text=str(
                    i + 1),
                font=(
                    "Arial",
                    16)).grid(
                row=i + 1,
                column=0,
                padx=10,
                pady=5)
            tk.Label(
                self.leaderboard_window,
                text=name,
                font=(
                    "Arial",
                    16)).grid(
                row=i + 1,
                column=1,
                padx=10,
                pady=5)
            tk.Label(
                self.leaderboard_window,
                text=score,
                font=(
                    "Arial",
                    16)).grid(
                row=i +
                1,
                column=2,
                padx=10,
                pady=5)

        # button to close leaderboard window
        close_button = tk.Button(
            self.leaderboard_window,
            text="Close",
            command=self.leaderboard_window.destroy)
        close_button.grid(row=len(self.scores) + 1, columnspan=3, pady=10)


# using game class to handle game setup and working
class Game:
    def __init__(self, window):
        self.window = window    # set the main game window
        self.window.title('Quarantine Quest')   # window title
        self.leaderboard = Leaderboard()    # initialize leaderboard instance
        self.window.geometry('1024x768')    # window size
        self.window.configure(bg="black")   # setting bg coor to black
        self.player_name = None  # placeholder for player's name
        self.is_paused = False  # game is not paused initially
        self.boss_key_active = False    # boss key is not active

        # setting up boss screen
        self.boss_screen = Canvas(self.window, width=1024, height=768)
        self.boss_image = ImageTk.PhotoImage(
            Image.open("boss.jpeg").resize((1024, 768)))
        self.boss_screen.create_image(0, 0, image=self.boss_image, anchor='nw')

        # calling function to show the start page
        self.show_start_page()

    def show_start_page(self):
        self.clear_window()  # clear existing widgets

    # set canvas size to match game window size
        self.start_canvas = Canvas(self.window, width=1024, height=768)
        self.start_canvas.grid(row=0, column=0)

    # loading bg image for the start page
        self.bg_image = ImageTk.PhotoImage(
            Image.open("qq.png").resize((1024, 768)))
    # displaying bg image for start page
        self.start_canvas.create_image(0, 0, image=self.bg_image, anchor='nw')

    # adjust grid column settings for even distribution of space
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

    # entry widget for the player's name
        self.name_label = Label(
            self.window, text="Enter your name", font=(
                "Arial", 20), fg="#151A7B", bg="#B19CD9")
        self.name_label.place(x=650, y=300)
        self.name_entry = Entry(self.window, font=("Arial", 20))
        self.name_entry.place(x=600, y=350)

    # Button 1: Start Game
        oval1 = self.start_canvas.create_oval(
            440, 420, 620, 460, fill="#4a90e2", outline="#2171cd", width=2)
        text1 = self.start_canvas.create_text(
            530, 440, text="Start Game", fill="white", font=(
                "Arial", 16, "bold"))
        self.start_canvas.tag_bind(
            oval1, "<Button-1>", lambda e: self.start_game())
        self.start_canvas.tag_bind(
            text1, "<Button-1>", lambda e: self.start_game())

    # Button 2: Leaderboard
        oval2 = self.start_canvas.create_oval(
            440, 490, 620, 530, fill="#4a90e2", outline="#2171cd", width=2)
        text2 = self.start_canvas.create_text(
            530, 510, text="Leaderboard", fill="white", font=(
                "Arial", 16, "bold"))
        self.start_canvas.tag_bind(
            oval2,
            "<Button-1>",
            lambda e: self.leaderboard.show_leaderboard())
        self.start_canvas.tag_bind(
            text2,
            "<Button-1>",
            lambda e: self.leaderboard.show_leaderboard())

    # Button 3: Instructions
        oval3 = self.start_canvas.create_oval(
            440, 560, 620, 600, fill="#4a90e2", outline="#2171cd", width=2)
        text3 = self.start_canvas.create_text(
            530, 580, text="Instructions", fill="white", font=(
                "Arial", 16, "bold"))
        self.start_canvas.tag_bind(
            oval3, "<Button-1>", lambda e: self.show_instructions())
        self.start_canvas.tag_bind(
            text3, "<Button-1>", lambda e: self.show_instructions())

    # Button 4: Continue Saved Game
        oval4 = self.start_canvas.create_oval(
            390, 630, 660, 670, fill="#4a90e2", outline="#2171cd", width=2)
        text4 = self.start_canvas.create_text(
            520, 650, text="Continue Saved Game", fill="white", font=(
                "Arial", 16, "bold"))
        self.start_canvas.tag_bind(
            oval4, "<Button-1>", lambda e: self.load_game())
        self.start_canvas.tag_bind(
            text4, "<Button-1>", lambda e: self.load_game())

    # Button 5: Customize Controls
        oval5 = self.start_canvas.create_oval(
            410, 700, 640, 740, fill="#4a90e2", outline="#2171cd", width=2)
        text5 = self.start_canvas.create_text(
            520, 720, text="Customize Controls", fill="white", font=(
                "Arial", 16, "bold"))
        self.start_canvas.tag_bind(
            oval5, "<Button-1>", lambda e: self.open_key_config())
        self.start_canvas.tag_bind(
            text5, "<Button-1>", lambda e: self.open_key_config())

    # default keys for movement(left and right)
        self.left_key = "<Left>"
        self.right_key = "<Right>"

    def show_instructions(self):
        # creating a new window to show the instructions
        instructions_window = Toplevel(window)
        instructions_window.title("Instructions")
        instructions_window.geometry("600x600")
        instructions_window.configure(bg="#c19adf")  # purple background color

    # font for bold text
        bold_font = Font(family="Arial", size=12, weight="bold")

    # text widget to display the instructions
        text_widget = Text(instructions_window, wrap=WORD, font=("Arial", 12))
        text_widget.pack(padx=20, pady=20)

    # instructions
        text_widget.insert(END, "Welcome to Quarantine Quest!\n\n")
        txt_1 = "Your goal is to survive the pandemic "
        txt_2 = "and achieve the highest score possible."
        txt_3 = " Here's how to play:\n\n"
        text_widget.insert(END, txt_1 + txt_2 + txt_3)

    # movement instructions
        text_widget.insert(END, "Movement:\n", "bold")
        txt_4 = "Use arrow keys to move your character across the screen.\n\n"
        text_widget.insert(END, txt_4)

    # scoring points instructions
        text_widget.insert(END, "Scoring Points:\n", "bold")
        txt_5 = "Catch masks and injections to score points.\n"
        txt_6 = "Each mask or injection normally gives you 10 points.\n\n"
        text_widget.insert(END, txt_5 + txt_6)

    # avoid danger instructions
        text_widget.insert(END, "Avoid Danger:\n", "bold")
        txt_7 = "Dodge the falling germs to protect your lives.\n"
        txt_8 = "Each time a germ hits you, you lose 1 life.\n\n"
        text_widget.insert(END, txt_7 + txt_8)

    # cheat codes for the game
        text_widget.insert(END, "Cheat Codes for Extra Boosts:\n", "bold")
        txt_9 = "During the game, type these "
        txt_10 = "cheat codes for special abilities:\n\n"
        text_widget.insert(END, txt_9 + txt_10)
        text_widget.insert(END, "    '123': ", "bold")
        text_widget.insert(END, "Instantly gain 3 extra lives.\n")
        text_widget.insert(END, "    '456': ", "bold")
        txt_11 = "Activates a shield that"
        txt_12 = "protects you from germs for 10 seconds. "
        txt_13 = "Germs won’t affect your lives during this time.\n"
        text_widget.insert(END, txt_11 + txt_12 + txt_13)
        text_widget.insert(END, "    '789': ", "bold")
        txt_14 = "Doubles your score for every mask or injection you catch. "
        txt_15 = "You’ll earn 20 points instead of the "
        txt_16 = "usual 10 for the duration of this boost.\n\n"
        text_widget.insert(END, txt_14 + txt_15 + txt_16)

    # objective of the game
        text_widget.insert(END, "Objective:\n", "bold")
        txt_17 = "Survive as long as possible "
        txt_18 = "and aim for the highest score!\n\n"
        text_widget.insert(END, txt_17 + txt_18)
        text_widget.insert(END, "Good luck and have fun!\n", "bold")

    # tag for bold text
        text_widget.tag_configure("bold", font=bold_font)

    # disable editing in the widget
        text_widget.config(state=DISABLED)

    # close button
        close_button = tk.Button(
            instructions_window,
            text="Close",
            command=instructions_window.destroy)
        close_button.pack(pady=10)

    def start_game(self):
        # get the player's name
        self.player_name = self.name_entry.get()
        if self.player_name:
            self.clear_window()  # clear current window
            self.setup_game()  # set up the game
        else:
            # give warning to user if no name is entered
            self.name_label.config(text="Please enter your name", fg="red")

    def clear_window(self):
        # detsroy all widgets in the window
        for widget in self.window.winfo_children():
            widget.destroy()

    def return_to_start_page(self, event=None):
        # pause the game if active
        self.is_paused = True

    # clear the current window
        self.clear_window()

    # show start page
        self.show_start_page()

    def setup_game(self):
        # unpause the game
        self.is_paused = False

        # bind Esc key to return to start page
        self.window.bind("<Escape>", self.return_to_start_page)

        # bind the 'p' key to toggle pause
        self.window.bind("<p>", self.toggle_pause)
        self.window.bind("<P>", self.toggle_pause)

        # bind the 'b' key for boss key
        self.window.bind("<b>", self.toggle_boss_key)  # Add boss key binding
        self.window.bind("<B>", self.toggle_boss_key)

        # unbinding left and right arrow keys
        self.window.unbind("<Left>")
        self.window.unbind("<Right>")

        # setting window title with player name
        self.window.title(f'Escape the Virus - Player: {self.player_name}')

        # setting bg color
        self.window.configure(bg="black")

        # create top canvas for score, lives and save game button
        self.top = Canvas(self.window, width=1024, height=50, bg="black")
        self.top.grid(column=0, row=0)

        # create playground canvas for game
        self.playground = Canvas(
            self.window,
            width=1024,
            height=718,
            bg="white")
        self.playground.grid(column=0, row=1)

        # adjust grid column settings for even distribution of space
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        # loading and displaying bg image
        self.background_image = ImageTk.PhotoImage(
            Image.open("new.png").resize((1024, 768)))
        self.playground.create_image(
            0, 0, image=self.background_image, anchor='nw')

        # initialize score to 0
        self.score = 0

        # initialize lives to 5
        self.lives = 5

        # initalize game so that game is not over
        self.game_over_flag = False

        # displaying score
        self.scoreLabel = Label(self.top, text="Score: " +
                                str(self.score),
                                bg="green",
                                fg="white",
                                font=(50))
        self.scoreLabel.place(x=30, y=15)

        # displaying lives
        self.livesLabel = Label(self.top,
                                text="Lives Left: " + str(self.lives),
                                bg="red",
                                fg="white",
                                font=(50))
        self.livesLabel.place(x=180, y=15)

        # save game button
        self.save_game_button = tk.Button(
            self.top, text="Save Game", font=(
                "Arial", 16), command=self.save_game_with_pause)
        self.save_game_button.place(x=850, y=15)

        # load in images for germ
        self.germ_images = [
            ImageTk.PhotoImage(Image.open("germpic.png").resize((80, 80))),
            ImageTk.PhotoImage(Image.open("purplegerm.png").resize((70, 70)))
        ]

        # load in images for cure
        self.cure_images = [
            ImageTk.PhotoImage(Image.open("masked.png").resize((60, 60))),
            ImageTk.PhotoImage(Image.open("vacc.png").resize((80, 80)))
        ]

        # load in player image
        self.player_image = ImageTk.PhotoImage(
            Image.open("boynew.png").resize((180, 200)))

        # place human at playground in the centre
        self.player = self.playground.create_image(
            550, 670, image=self.player_image)

        # binding left and right keys to move the player
        self.window.bind(self.left_key, self.moveleft)
        self.window.bind(self.right_key, self.moveright)

        # setting parameters for start of game
        self.fall_speed = 4  # speed for falling items
        # interval for creating new germs in miliseconds
        self.germ_creation_interval = 3000
        self.max_active_germs = 5  # max no. of germs at same time

        # initiaize list for active items and dict for storing item type
        self.active_items = []
        self.item_types = {}

        # initializing cheat code variabes
        self.current_input = ""
        self.shield_active = False
        self.double_points_active = False
        self.window.bind("<Key>", self.cheat_codes)  # bind key for cheat codes

        # set game canvas to playground
        self.game_canvas = self.playground

        # create falling items
        self.create_germ()
        self.create_cure()

    def open_key_config(self):
        # create a new window for key configuration
        self.config_window = tk.Toplevel(self.window)
        self.config_window.title("Customize Controls")
        self.config_window.geometry("400x300")

    # label and entry widgets for key configuration
        tk.Label(
            self.config_window,
            text="Move Left Key:",
            font=(
                "Arial",
                16)).pack(
            pady=10)
        self.left_key_entry = tk.Entry(self.config_window, font=("Arial", 16))
        self.left_key_entry.pack(pady=10)
        self.left_key_entry.insert(0, self.left_key.strip("<>"))

        tk.Label(
            self.config_window,
            text="Move Right Key:",
            font=(
                "Arial",
                16)).pack(
            pady=10)
        self.right_key_entry = tk.Entry(self.config_window, font=("Arial", 16))
        self.right_key_entry.pack(pady=10)
        self.right_key_entry.insert(0, self.right_key.strip("<>"))

    # save button for new keys
        tk.Button(
            self.config_window,
            text="Save Keys",
            font=(
                "Arial",
                16),
            command=self.save_key_config).pack(
            pady=20)

    def save_key_config(self):
        # get new key configurations
        new_left = self.left_key_entry.get()
        new_right = self.right_key_entry.get()

    # checking that keys are different and not empty
        condition_1 = new_left and new_right and new_left != new_right
        condition_2 = new_left.lower() not in ['b', 'p']
        condition_3 = new_right.lower() not in ['b', 'p']
        if (condition_1 and condition_2 and condition_3):
            # unbind previous keys
                self.window.unbind(self.left_key)
                self.window.unbind(self.right_key)

        # set new keys and bind them for both uppercase and lowercase
                self.left_key = f"<{new_left}>"
                self.right_key = f"<{new_right}>"

                self.window.bind(f"<{new_left.lower()}>", self.moveleft)
                self.window.bind(f"<{new_left.upper()}>", self.moveleft)
                self.window.bind(f"<{new_right.lower()}>", self.moveright)
                self.window.bind(f"<{new_right.upper()}>", self.moveright)

                self.config_window.destroy()    # close configuration window

        else:
            tk.messagebox.showerror(
                "Invalid Configuration",
                "Keys must be different and not empty(and not 'b' or 'p'!")

    def show_leaderboard(self):
        self.leaderboard.show_leaderboard()

        # creating germ items and cure items for the game
    def create_germ(self):
        # check if game is puased or over
        if self.is_paused or self.game_over_flag:
            return

        # no. of active germs shoud not exceed maximum
        if sum(1 for item in self.active_items if self.playground.type(
                item) == 'image') < self.max_active_germs:
            # get non-overlapping position for new germ
            xPosition, yPosition = self.get_non_overlapping_position()
            # select random germ image
            germ_image = self.germ_images[randint(
                0, len(self.germ_images) - 1)]
            # create germ at specific position
            germ = self.playground.create_image(
                xPosition, yPosition, image=germ_image)
            self.active_items.append(germ)  # add germs to active items list
            self.fall_item(germ, "germ")  # making germ fall

        self.window.after(
            self.germ_creation_interval,
            self.create_germ)  # next germ creation

    def create_cure(self):
        if self.is_paused or self.game_over_flag:
            return

        xPosition, yPosition = self.get_non_overlapping_position()

        if xPosition is not None and yPosition is not None:

            cure_image = self.cure_images[randint(
                0, len(self.cure_images) - 1)]
            cure = self.playground.create_image(
                xPosition, yPosition, image=cure_image)

            self.active_items.append(cure)
            self.fall_item(cure, "cure")

        self.window.after(7000, self.create_cure)

    def adjust_difficulty(self):
        # storing previous difficulty settings
        previous_speed = self.fall_speed
        previous_interval = self.germ_creation_interval
        previous_max_germs = self.max_active_germs

        # adjusting game difficulty based on player's scores
        if self.score >= 150:
            self.fall_speed = 7
            self.germ_creation_interval = 700
            self.max_active_germs = 10

        elif self.score >= 100:
            self.fall_speed = 6
            self.germ_creation_interval = 800
            self.max_active_germs = 8

        elif self.score >= 50:
            self.fall_speed = 5
            self.germ_creation_interval = 1000
            self.max_active_germs = 6

        # show msg on screen as difficulty increases
        if (self.fall_speed != previous_speed or
            self.germ_creation_interval != previous_interval or
                self.max_active_germs != previous_max_germs):
            self.show_message(
                "Difficulty Increasing!",
                fg_color="red",
                bg_color="#003366")

    def get_non_overlapping_position(self):
        # gets new position for an item that doesnt overlap with existing items

        # max attempts to find non overlapping position
        max_attempts = 10

        for _ in range(max_attempts):
            xPosition = randint(50, 974)  # random x position within playground
            yPosition = 0  # start from top
            # check if position is non-overlapping
            if not self.is_overlapping(
                    xPosition, yPosition):
                return xPosition, yPosition
        # if no non-overlapping position found, return last position
        return xPosition, yPosition

    def is_overlapping(self, xPosition, yPosition):
        # checks if given position overlaps with existing items
        for item in self.active_items:
            item_coords = self.playground.coords(
                item)  # current position of the item
            if item_coords:
                item_x, item_y = item_coords[0], item_coords[1]

            # bounding box around the item
                item_bbox = (
                    item_x -
                    40,
                    item_y -
                    40,
                    item_x +
                    40,
                    item_y +
                    40)  # Adjust this based on item size

            # check if new position overlaps with the existing item
                new_item_bbox = (
                    xPosition - 40,
                    yPosition - 40,
                    xPosition + 40,
                    yPosition + 40)

            # check if bounding boxes overlap
                if self.check_overlap_bboxes(new_item_bbox, item_bbox):
                    return True
        return False

    def check_overlap_bboxes(self, bbox1, bbox2):
        # checking if two bounding boxes overlap
        x1_min, y1_min, x1_max, y1_max = bbox1  # coord of first bb
        x2_min, y2_min, x2_max, y2_max = bbox2  # coord of second box

        return not (x1_max < x2_min or x1_min >
                    x2_max or y1_max < y2_min or y1_min > y2_max)

    def toggle_pause(self, event=None):
        # toggling pause key
        if not self.game_over_flag:
            self.is_paused = not self.is_paused  # flip pause state
            if self.is_paused:
                # unbind movt. keys when paused
                self.window.unbind("<Left>")
                self.window.unbind("<Right>")
                self.pause_game()   # show pause overlay
            else:
                # rebing movt. keys when resumed
                self.window.bind("<Left>", self.moveleft)
                self.window.bind("<Right>", self.moveright)
                self.resume_game()  # remove pause overlay and resume game

    def pause_game(self):
        # displaying PAUSED text on screen
        self.pause_text = self.playground.create_text(
            512, 360,
            text="PAUSED",
            font=("Arial", 48),
            fill="yellow",
            tags="pause_overlay"
        )

    def resume_game(self):
        # remove pause overlay if it exists
        try:
            self.playground.delete("pause_overlay")
        except BaseException:
            pass

        self.is_paused = False  # game marked as not paused

        # remove invaid items
        self.active_items = [
            item for item in self.active_items
            if self.playground.type(item) != "text" and
            self.playground.coords(item) is not None
        ]

        # restart falling for remaining valid items
        for item in self.active_items[:]:
            try:
                item_type = self.item_types.get(item)
                if item_type:
                    self.fall_item(item, item_type)
            except Exception:
                # remove item if it can't be processed
                if item in self.active_items:
                    self.active_items.remove(item)

    #   restart germ and cure generation
        self.create_germ()
        self.create_cure()

    def toggle_boss_key(self, event=None):
        # toggle boss key screen
        self.boss_key_active = not self.boss_key_active

        if self.boss_key_active:
            # is boss key is active, hide game elements and show boss screen
            self.is_paused = True
            try:
                if hasattr(
                        self,
                        'top') and self.top and self.top.winfo_exists():
                    self.top.grid_remove()

            except Exception:
                pass

            try:
                if (
                    hasattr(self, 'playground') and
                    self.playground and
                    self.playground.winfo_exists()
                ):
                    self.playground.grid_remove()

            except Exception:
                pass

            self.boss_screen.grid(row=0, column=0, rowspan=2)

        else:
            # deactivate boss key, hide boss screen and show game elements
            self.boss_screen.grid_remove()
            try:
                if hasattr(
                        self,
                        'top') and self.top and self.top.winfo_exists():
                    self.top.grid()
            except Exception:
                pass

            try:
                if (
                    hasattr(self, 'playground') and
                    self.playground and
                    self.playground.winfo_exists()
                ):
                    self.playground.grid()

            except Exception:
                pass

            self.is_paused = False  # resume the game
            self.resume_game()

    def clear_window(self):
        # remove all widgets except boss screen
        for widget in self.window.winfo_children():
            if widget != self.boss_screen:
                widget.destroy()

    def show_message(
            self,
            text,
            duration=2000,
            fg_color="red",
            bg_color="#003366"):
        # clear any existing message
        if hasattr(
                self,
                'message_label') and self.message_label.winfo_exists():
            self.message_label.destroy()

    # create a new message label
        self.message_label = tk.Label(
            self.window, text=text, font=(
                "Arial", 20), fg=fg_color, bg=bg_color)

        # place message at centre of window
        self.message_label.place(x=700, y=400, anchor='center')

    # remove the message after `duration of milliseconds
        self.window.after(duration, self.hide_message)

    def hide_message(self):
        # remove message label if it exists
        if hasattr(
                self,
                'message_label') and self.message_label.winfo_exists():
            self.message_label.destroy()

    def cheat_codes(self, event):

        # append keys to current input buffer
        self.current_input += event.char

        # checking for each cheat code
        if "123" in self.current_input:
            self.activate_life_cheat()  # gives 3 extra ives
            self.current_input = ""

        elif "456" in self.current_input:
            self.activate_shield_cheat()    # gives shield to player
            self.current_input = ""

        elif "789" in self.current_input:
            # gives 2x the points to the player
            self.activate_double_points_cheat()
            self.current_input = ""

        # reset input buffer if it gets too long
        if len(self.current_input) > 10:
            self.current_input = ""

        # defining cheat codes
    def activate_life_cheat(self):
        self.lives += 3
        self.livesLabel.config(text="Lives Left: " + str(self.lives))
        self.show_message(
            "Extra Lives Activated! (+3)",
            fg_color="#FFD700",
            bg_color="#003366")

    def activate_shield_cheat(self):
        self.shield_active = True
        self.show_message(
            "Shield Activated! (10 seconds)",
            fg_color="#FFD700",
            bg_color="#003366")
        self.window.after(10000, self.deactivate_shield)

    def deactivate_shield(self):
        self.shield_active = False
        self.show_message(
            "Shield Deactivated!",
            fg_color="#FFD700",
            bg_color="#003366")

    def activate_double_points_cheat(self):
        self.double_points_active = True
        self.show_message(
            "Double Points Activated! (10 seconds)",
            fg_color="#FFD700",
            bg_color="#003366")
        self.window.after(10000, self.deactivate_double_points)

    def deactivate_double_points(self):
        self.double_points_active = False
        self.show_message(
            "Double Points Deactivated!",
            fg_color="#FFD700",
            bg_color="#003366")

    def fall_item(self, item, item_type):
        # assign item type to item
        self.item_types[item] = item_type

        # check if game is paused/over
        if self.is_paused or self.game_over_flag:
            return

        # move item down by fall speed
        self.playground.move(item, 0, self.fall_speed)

        # retrieve current coordinates of item
        item_coords = self.playground.coords(item)
        current_y = item_coords[1]

        # check for collision with player
        if self.check_collision(item):
            if (item_type == "germ"):
                # if shield is not active, then only lose lives
                if not self.shield_active:
                    self.lives -= 1
                    self.livesLabel.config(
                        text="Lives Left: " + str(self.lives))
                    if self.lives <= 0:
                        self.game_over()

            else:
                # double points if shield is active otherise 10
                points = 20 if self.double_points_active else 10
                self.score += points
                self.scoreLabel.config(text="Score: " + str(self.score))
                self.adjust_difficulty()

            # remove items for playground and active_items
            self.playground.delete(item)
            self.active_items.remove(item)
            return

        # checking if item is still within the playground
        if current_y < self.playground.winfo_height():
            self.window.after(50, self.fall_item, item, item_type)
        else:
            # remove item if it goes out of bounds
            self.playground.delete(item)
            self.active_items.remove(item)

    def check_collision(self, item):
        # retrieve coordinates of player and item
        player_coords = self.playground.coords(self.player)
        item_coords = self.playground.coords(item)

        if player_coords and item_coords:
            player_x, player_y = player_coords[0], player_coords[1]
            item_x, item_y = item_coords[0], item_coords[1]

            # checking if item is within collision range of player
            return (player_x - 70 <= item_x <= player_x + 70 and
                    player_y - 100 <= item_y <= player_y + 100)
        return False

    def moveleft(self, event):
        current_pos = self.playground.coords(self.player)
    # keep the player within bounds while moving left
        if current_pos and current_pos[0] > 60:
            self.playground.move(self.player, -20, 0)

    def moveright(self, event):
        current_pos = self.playground.coords(self.player)
    # keep the player within bounds while moving right
        if current_pos and current_pos[0] < 964:
            self.playground.move(self.player, 20, 0)

    def save_game_with_pause(self):
        # pause the game
        self.is_paused = True
        self.pause_game()

    # save the game
        self.save_game()

    # return to start page
        self.window.after(2000, self.show_start_page)

    def save_game(self, event=None):
        # pause the game
        self.is_paused = True

        # collect all important game  data
        game_state = {
            'player_name': self.player_name,
            'score': self.score,
            'lives': self.lives,
            'player_position': self.playground.coords(self.player),
            'active_items': [],
            'shield_active': self.shield_active,
            'double_points_active': self.double_points_active,
            'fall_speed': self.fall_speed,
            'germ_creation_interval': self.germ_creation_interval,
            'max_active_germs': self.max_active_germs
        }

        # save active items positions and their types
        for item in self.active_items:
            if item in self.item_types:
                item_coords = self.playground.coords(item)
                game_state['active_items'].append({
                    'type': self.item_types[item],
                    'position': item_coords
                })

        # save to json file with player name
        filename = f"save_{self.player_name}.json"
        with open(filename, 'w') as f:
            json.dump(game_state, f)

        self.show_start_page()
        self.name_label.config(text="Game Saved Successfully!", fg="green")

    def load_game(self):
        try:
            # get the player's name
            player_name = self.name_entry.get()
            if not player_name:
                self.name_label.config(
                    text="Please enter your name to load game", fg="red")
                return

            # generate filename based on player's name
            filename = f"save_{player_name}.json"

            with open(filename, 'r') as f:  # open and read saved game file
                game_state = json.load(f)

            # initialize game with loaded data
            self.clear_window()
            self.setup_game()

            # restore game state from loaded data
            self.player_name = game_state['player_name']
            self.score = game_state['score']
            self.lives = game_state['lives']
            self.scoreLabel.config(text="Score: " +
                                   str(self.score))    # update score label
            self.livesLabel.config(text="Lives Left: " +
                                   str(self.lives))   # update lives label

            # move player to saved position
            player_pos = game_state['player_position']
            self.playground.coords(self.player, player_pos[0], player_pos[1])

            # restore game settings
            self.shield_active = game_state['shield_active']
            self.double_points_active = game_state['double_points_active']
            self.fall_speed = game_state['fall_speed']
            self.germ_creation_interval = game_state['germ_creation_interval']
            self.max_active_germs = game_state['max_active_germs']

            # recreate active items in saved positions
            for item_data in game_state['active_items']:
                if item_data['type'] == 'germ':
                    # select random germ image
                    germ_image = self.germ_images[randint(
                        0, len(self.germ_images) - 1)]

                    # create new germs at saved positions
                    item = self.playground.create_image(
                        item_data['position'][0],
                        item_data['position'][1],
                        image=germ_image)
                    # add new germ to list of active items
                    self.active_items.append(item)
                    self.item_types[item] = 'germ'

                    # make germ fall from current position
                    self.fall_item(item, 'germ')

                elif item_data['type'] == 'cure':
                    # select random cure image
                    cure_image = self.cure_images[randint(
                        0, len(self.cure_images) - 1)]

                    # create new cure at saved positions
                    item = self.playground.create_image(
                        item_data['position'][0],
                        item_data['position'][1],
                        image=cure_image)

                    self.active_items.append(item)
                    self.item_types[item] = 'cure'
                    self.fall_item(item, 'cure')

            # start generating new germs and cures
            self.create_germ()
            self.create_cure()

            self.show_message("Game Loaded Successfully!")

        except FileNotFoundError:
            # if saved game file does not exist
            self.name_label.config(
                text="No saved game found for this name", fg="red")
        except Exception as e:
            # handle other errors that occur while loading game
            self.name_label.config(text="Error loading game", fg="red")
            print(f"Error loading game: {e}")

    def game_over(self):
        # using game over flag to prevent further item generation
        self.game_over_flag = True

    # clear the playground
        self.playground.delete("all")

    # new canvas for game over screen
        game_over_screen = tk.Canvas(self.window, width=1024, height=768)
        game_over_screen.grid(row=1, column=0)

    # loading the game over image
        game_over_image = ImageTk.PhotoImage(
            Image.open("gameovernew.png").resize((1024, 768)))

    # dispaying the game over image
        game_over_screen.create_image(0, 0, image=game_over_image, anchor='nw')
        game_over_screen.image = game_over_image

    # displaying the final score
        game_over_screen.create_text(530,
                                     550,
                                     text="Final Score: " + str(self.score),
                                     font=("Arial",
                                           30),
                                     fill="white")

    # add player's score to leaderboard
        self.leaderboard.add_score(self.player_name, self.score)

    # main menu button
        main_menu_button = game_over_screen.create_oval(
            380, 620, 640, 660, fill="#4a90e2", outline="#2171cd", width=2)
        main_menu_text = game_over_screen.create_text(
            510, 640, text="Main Menu", fill="white", font=(
                "Arial", 16, "bold"))
        game_over_screen.tag_bind(
            main_menu_button,
            "<Button-1>",
            lambda e: self.show_start_page())
        game_over_screen.tag_bind(
            main_menu_text,
            "<Button-1>",
            lambda e: self.show_start_page())

    # leaderboard button
        leaderboard_button = game_over_screen.create_oval(
            380, 670, 640, 710, fill="#4a90e2", outline="#2171cd", width=2)
        leaderboard_text = game_over_screen.create_text(
            510, 690, text="Leaderboard", fill="white", font=(
                "Arial", 16, "bold"))
        game_over_screen.tag_bind(
            leaderboard_button,
            "<Button-1>",
            lambda e: self.show_leaderboard())
        game_over_screen.tag_bind(
            leaderboard_text,
            "<Button-1>",
            lambda e: self.show_leaderboard())


if __name__ == "__main__":
    window = tk.Tk()
    game = Game(window)
    window.mainloop()
