#!/usr/bin/env python3
# NOTE: noinspection -> comments are only for Pycharm editor to comply with PEP8 regulations!
# for application exit
import sys
# for time display and idle
from time import strftime, sleep
# for password check
from werkzeug.security import check_password_hash
# All the graphical elements for the application
from tkinter import (Tk, Label, Button, Frame, StringVar, IntVar,
                     DISABLED, NORMAL, SUNKEN, SOLID, Entry,
                     RIGHT, BOTH, CENTER)

# project imports
import variables as var
from record import User, user, create_record
from record_display import all_time_records
from frames import LogIn, Register
from forms import UserForm
from secret_word import get_word

"""
This application it's based on the game Hangman, all rules applied with added difficulty levels.
Mainly it's built with Tkinter with some additional libraries listed in the requirements.txt.
Use:
    - as user:      - after registration can login with the <username>;
                    - can view all time played games;
                    - can view own played games;
                    - can play the game;
                    
    - as guest:     - can enter in game;
                    - view al time games;
                    - can play the game;

Degree:         Faculty of Creative Arts, Technologies and Science
Department:     Computer Science and Technology
University:     University of Bedfordshire
Author:         Oszkar Feher
Date:           21 October 2022
"""


class GameGUI:
    """
    GameGUI class, main application class which will be called later on using TK() class.
    All main functionality it's built in this class.
    Further functionality is explained in each method accordingly.
    :methods: - __init__(master=root) - constructor, GUI elements;
              - get_screen_dimensions() -> tuple: - sets width, height and position of main window
                                                and returns a tuple of 4 values;
              - screen() - sets main window size;
              - solve_screen() - calls a new Tk class to open a new window to enter solution;
              - get_frame_size() -> tuple: - sets the frame size and returns a tuple;
              - create_record(solved) - creates a game record;
              - button_builder() - returns a Button object for creating buttons;
              - build_frames() - building all frames for buttons, labels and new Tk window;
              - build_grids() - setting the grid of each frame;
              - build_title_label() - creates the label to category display;
              - build_countdown_label() - countdown label for missed guesses;
              - build_clock_label(*args) - creates a label for clock display;
              - build_timer_label() - creates a label for timer display for difficulty level 3;
              - build_word_label(*args) - creates a label to display the secret word to the user;
              - timer_alert() - checks if the time ended for the difficulty level 3;
              - draw_word() - sets the secret word into a dashed line;
              - game_status_action() - sets every parameter to default;
              - game_status() - sets game to default dependent on the game status;
              - build_abc_buttons() - creates all the buttons for the alphabet adding into a list;
              - build_category_buttons() - creates the category buttons adding into a list;
              - buttons() - creates all the remaining buttons on the application;
              - exit_button_event() - displays a message before exiting the application;
              - abc_buttons_event(item) - event handler for the alphabet buttons;
              - start_stop_action(text) - events for start and stop buttons event handler;
              - start_button_event() - start button event handler, sets the game to start;
              - stop_button_event() - stop button event handler, sets the game to default;
              - guest_button_event() - guest button event handler;
              - login_button_event() - login button event handler, checks login input and displays info messages;
              - become_button_event() - become member button event handler;
              - registration_button_event() - registration event handler, creates a new user if inputs are valid
                                            (not empty), displays info messages;
              - back_button_event() - sets the application to default state before login;
              - solve_button_event() - solve button event handler, calling the solve screen;
              - ok_solve_button_event() - checks entered word if is the secret word
              - cancel_button_event() - exits solve screen;
              - set_secret_word() - sets secret word from the csv files;
              - set_buttons_command(text) - sets and returns a point to a event handler;
              - category_buttons_event(text) - category button event handler, sets the buttons to default or disabled
                                             state;
              - level_buttons_event(text) - difficulty level buttons event handler, sets the buttons state;
              - set_level_buttons(level) - the same as above just from level status integer;
              - clear_login_fields() - clears entry input;
              - check_password() - checks if the entry input in the password area match;
              - update(): - updates main window every second (1000 millisecond)
    """
    def __init__(self, master=None):
        """Initializer of all widgets and frames"""

        # Main graphical window, it will be a Tk object
        self.master = master
        # font size related to main window size
        self.rem = self.master.winfo_screenwidth()
        # Member user ID
        self.user_id = None

        # Call of frame builders
        self.screen()
        self.build_frames()
        self.build_grids()

        # All displayed labels
        # Info text traces build_title_label()
        self.banner_text = StringVar()
        # set to empty string
        self.banner_text.set('')
        self.banner_text.trace('w', self.build_title_label)

        # Countdown value traces build_countdown()
        self.counter = StringVar()
        self.counter.trace('w', self.build_countdown_label)

        # Clock label text traces build_clock_label()
        self.clock_text = StringVar()
        self.clock_text.set('Clock')
        self.clock_text.trace('w', self.build_clock_label)

        # Displayed secret word text traces build_word_label()
        self.word_text = StringVar()
        self.word_text.set('Please select your category')
        self.word_text.trace('w', self.build_word_label)

        # Timer label text traces build_timer()
        self.timer_text = StringVar()
        self.timer_text.set(strftime("%H:%M"))
        self.timer_text.trace('w', self.build_timer_label)

        # Remaining time traces time_alert()
        self.time_left = IntVar()
        self.time_left.set(60)
        self.time_left.trace('w', self.timer_alert)

        # Secret word variable
        self.secret_word = StringVar()
        self.prompt = StringVar()
        self.prompt.set('random')

        # Predefined variables
        # guessed letters sorted form
        self.sorted_word = ''
        # Selected letter with any abc button
        self.selected_char = ''
        # difficulty level variable, default easy
        self.difficulty_status = 1
        # alphabet button list
        self.abc_buttons = []
        # categories button list
        self.category_buttons = []
        # difficulty button list
        self.difficulty_buttons = []
        # wrong letters list
        self.wrong_letters = []
        # guessed letters list
        self.guessed_letters = []
        # played words list
        self.played_words = []
        # first and last letter for easy difficulty
        self.first_last = []
        # alphabet dictionary to change the state of alphabet button
        self.abc_buttons_dict = {}
        # game status, default False
        self.running = False

        # Call of building functions
        # creates info label
        self.build_title_label()
        # creates displayed secret word label
        self.build_word_label()
        # creates countdown label
        self.build_countdown_label()
        # creates timer label
        self.build_timer_label()
        # creates clock label
        self.build_clock_label()
        # creates all buttons except two listed
        self.buttons()
        # creates category buttons
        self.build_category_buttons()
        # creates alphabet buttons
        self.build_abc_buttons()

        # Update time
        self.update()

    def get_screen_dimensions(self, mini=False) -> tuple:
        """Get the main screen size and return a tuple for geometry() method
        which sets position and size of main window"""
        # Main screen width
        width = self.master.winfo_screenwidth()
        # Main screen height
        height = self.master.winfo_screenheight()
        # Conditional id window display resolution lower than 1440 pixels
        if width <= 1440:
            # if condition true, sets dimensions to default
            x, y = 0, 1
        # Conditional if the dimension is for the solve screen
        elif mini:
            # If for the solve screen
            x, y = 600, 400
        # Conditional if all above is false
        else:
            x = int(float(65) * float(width) / 100)
            y = int(float(75) * float(height) / 100)
        # returns a tuple for easier use
        return x, y, (width // 2 - x // 2), (height // 2 - y // 2)

    def screen(self):
        """Main screen
        Minimal size 1024 / 600
        Closing and minimize functionality removed from main screen"""
        # Minimal size of the main screen
        self.master.minsize(1024, 600)
        # Removes close functionality by setting it to True
        self.master.overrideredirect(True)
        # Builds main screen size and place by unpacking a tuple generated by get_screen_dimensions
        self.master.geometry('{0}x{1}+{2}+{3}'.format(*self.get_screen_dimensions()))
        # Sets main screen to idle till further instructions
        self.master.update_idletasks()

    def solve_screen(self):
        """Creates a new Tk screen to display an entry for solution
        Added an informative label, entry for input, two buttons to confirm or cancel"""
        # New Tk object
        # noinspection PyAttributeOutsideInit
        self.master_3 = Tk()
        # Main frame where the widgets are placed
        frame = Frame(self.master_3, bg=var.colours['bg'],
                      highlightbackground=var.colours['fg_enter'],
                      highlightcolor=var.colours['fg_enter'],
                      highlightthickness=3
                      )
        # Removing closing and minimise functionality
        self.master_3.overrideredirect(True)
        # Builds solve screen size and place by unpacking a tuple generated by get_screen_dimensions
        self.master_3.geometry('{0}x{1}+{2}+{3}'.format(*self.get_screen_dimensions(True)))
        # Sets main screen to idle till further instructions
        self.master_3.update_idletasks()
        # Placing frame on main screen
        frame.pack(fill=BOTH, expand=True)

        # Configuring rows and columns on the frame, 3 rows, 2 columns
        for i in range(3):
            frame.grid_rowconfigure(i, weight=1, uniform=None)
        frame.grid_columnconfigure(0, weight=1, uniform=None)
        frame.grid_columnconfigure(1, weight=1, uniform=None)
        # Setting background and foreground colours of the informative label
        bg, fg = var.set_buttons_color('title')
        # Creates info label
        label = Label(frame, text='Type in the answer, if wrong you lose!',
                      bg=bg, fg=fg,
                      font=var.get_font_size(self.rem, 8),
                      justify=CENTER
                      )
        # Adding to the frame grid on row 0 and column 0
        label.grid(row=0, column=0, sticky='ew', padx=30, pady=20, columnspan=2)
        # Setting background and foreground colours of the entry input
        bg, fg = var.set_buttons_color('timer')
        # Creates an entry for input
        # noinspection PyAttributeOutsideInit
        self.entry = Entry(frame, bg=bg, fg=fg, bd=1, width=18,
                           font=var.get_font_size(self.rem, 10))
        # Adding to the main frame grid, row 1, column 0
        self.entry.grid(row=1, column=0, sticky='ew', padx=30, pady=20, columnspan=2)
        # Creates button for confirm
        ok = Button(frame, bg=var.colours['bg'],
                    bd=1, fg=var.colours['fg_enter'], font=var.get_font_size(self.rem, 3),
                    text='Ok', command=self.ok_solve_button_event,
                    activeforeground='black', activebackground=var.colours['fg'],
                    width=5
                    )
        # Adding onto main frame grid
        ok.grid(row=2, column=0, sticky='e', padx=30, pady=20)
        # Creates button to cancel input
        cancel = Button(frame, bg=var.colours['bg'],
                        bd=1, fg=var.colours['fg_enter'], font=var.get_font_size(self.rem, 3),
                        text='Cancel', command=self.cancel_button_event,
                        activeforeground='black', activebackground=var.colours['fg'],
                        width=5
                        )
        # Adding onto main frame grid
        cancel.grid(row=2, column=1, sticky='w', padx=30, pady=20)

    def get_frame_size(self, code) -> tuple:
        """Return a tuple of frame sizes dependent on the row"""
        wa, wb, ha, hb = None, None, None, None
        # Conditional for main screen
        if code == 'm':
            wa, wb, ha, hb = 1, 1, 1, 1
        # Conditional for the rest of the frames
        elif code == 'r2':
            wa, wb, ha, hb = 1, 1, 3, 5
        elif code in ['r0', 'r1', 'r3']:
            wa, wb, ha, hb = 1, 1, 1, 5
        width = self.master.winfo_width() * wa // wb,
        height = self.master.winfo_height() * ha // hb
        # returns a tuple
        return width, height

    def create_record(self, solved=False):
        """Creates a record by default with not solved field"""
        if self.user_id:
            create_record(self.user_id, self.difficulty_status, solved,
                          len(self.guessed_letters), len(self.wrong_letters))
        # Message text with the word, difficulty level and guessed letters
        result = var.result['won'].format(self.secret_word.get(),
                                          var.int_to_levels[self.difficulty_status].capitalize(),
                                          self.guessed_letters)
        # Displaying the message
        var.message("YOU WON!", result)
        self.game_status_action()
        # Adding played word to a list to not be picked again
        self.played_words.append(self.secret_word.get())

    def button_builder(self, frame, text):
        """Creates and return a button object"""
        # font for the button
        font = None
        # Sets button event to a function which wil point to each event
        # handler based on the name given by text
        command = self.set_buttons_command(text)
        # State of the button set to None, later whe it will used will be set
        state = None
        # Background, foreground, active background, active foreground and
        # disabled foreground colours for buttons dependent on the name of the button provided by text
        bg, fg, abg, afg, dfg = var.set_buttons_color(text)
        button = Button(
            frame, text=text.capitalize(), bg=bg, fg=fg, font=font, bd=1,
            command=command, justify='center', overrelief=SUNKEN,
            anchor=CENTER, state=state, disabledforeground=dfg,
            activeforeground=afg, activebackground=abg, image=None
        )
        return button

    def build_frames(self):
        """Creates all frames for the main window"""
        # Width and height for login, register and mainframe
        width, height = self.get_frame_size("m")
        # New login frame imported from frames.py. Configuring and placing onto main screen
        # noinspection PyAttributeOutsideInit
        self.login = LogIn(self.master, self.rem)
        self.login.config(width=width, height=height)
        self.login.pack(fill=BOTH, expand=True)

        # New register frame imported from frames.py. Configuring and placing onto main screen
        # Than unmapping to not be visible till is called
        # noinspection PyAttributeOutsideInit
        self.signup = Register(self.master, self.rem)
        self.signup.config(width=width, height=height)
        self.signup.pack(fill=BOTH, expand=True)
        self.signup.pack_forget()

        # Main frame where all the game elements are added. Placed on main screen than unmapped.
        # noinspection PyAttributeOutsideInit
        self.mainframe = Frame(self.master, bg=var.colours['bg'],
                               width=width, height=height,
                               highlightbackground='black',
                               highlightcolor='black',
                               highlightthickness=2)
        self.mainframe.pack(fill=BOTH, expand=True)
        self.mainframe.pack_forget()
        # Row 0
        # Width and height for all the row except countdown_word row
        width, height = self.get_frame_size("r0")
        # Start and stop buttons column on the first row (0) and column (0)
        # noinspection PyAttributeOutsideInit
        self.row_start_buttons = Frame(self.mainframe, bg=var.colours['bg'],
                                       width=width, height=height)
        self.row_start_buttons.grid(row=0, column=0, sticky='news', pady=10)
        # Row 0 Column 1
        # Game record and solve buttons column on the first row (0) and second column (1)
        # noinspection PyAttributeOutsideInit
        self.column_game_record = Frame(self.row_start_buttons, bg=var.colours['bg'],
                                        highlightbackground=var.colours['fg'],
                                        highlightcolor=var.colours['bg_start'],
                                        highlightthickness=2)
        self.column_game_record.grid(row=0, column=1, rowspan=2,
                                     sticky='news', pady=7)
        # Row 0 Column 2
        # Timer display column on first row (0) and third column (2)
        # noinspection PyAttributeOutsideInit
        self.column_timer = Frame(self.row_start_buttons, bg=var.colours['bg'],
                                  highlightbackground=var.colours['fg'],
                                  highlightcolor=var.colours['bg_start'],
                                  highlightthickness=2)
        self.column_timer.grid(row=0, column=2, rowspan=2,
                               sticky='news', padx=20, pady=6)
        # Row 0 Column 3
        # Difficulty level buttons column on first row (0) and fourth column (3)
        # noinspection PyAttributeOutsideInit
        self.column_level_buttons = Frame(self.row_start_buttons, bg=var.colours['bg'])
        self.column_level_buttons.grid(row=0, column=3, rowspan=2, columnspan=2,
                                       sticky='news', padx=3, pady=4)
        # Row 1
        # Alphabet buttons row on second row (1) and first column (0)
        # noinspection PyAttributeOutsideInit
        self.row_abc_buttons = Frame(self.mainframe, bg=var.colours['bg'],
                                     width=width, height=height)
        self.row_abc_buttons.grid(row=1, column=0, sticky='news', padx=13)

        # Row 3
        # Category buttons row on fourth row (3) and first column
        # noinspection PyAttributeOutsideInit
        self.row_category_buttons = Frame(self.mainframe, bg=var.colours['bg'],
                                          width=width, height=height)
        self.row_category_buttons.grid(row=3, column=0, sticky='news', padx=5, pady=5)

        # Row 2
        # Width and height for countdown_word row
        width, height = self.get_frame_size("r0")
        # Countdown label and word display label row on third row (2) and first column (0)
        # noinspection PyAttributeOutsideInit
        self.row_countdown_word = Frame(self.mainframe, bg=var.colours['bg'],
                                        width=width, height=height)
        self.row_countdown_word.grid(row=2, column=0, sticky='news')

    def build_grids(self):
        """Grid layout for all the frames"""
        # Uniform values set to None
        u, u2 = None, None
        # Main Frame
        # 1 column
        self.mainframe.columnconfigure(0, weight=1, uniform=u)
        # 4 rows: upper button, alphabet buttons, word display and category button
        for m in range(0, 4):
            self.mainframe.rowconfigure(m, weight=1, uniform=u2)
        # Row 0
        # 15 columns: start-stop buttons, game record and solve buttons, timer label, difficulty level button
        # and info label for 10 column span
        for y in range(15):
            self.row_start_buttons.columnconfigure(y, weight=1, uniform=u)
        # 2 rows
        self.row_start_buttons.rowconfigure(0, weight=1, uniform=u2)
        self.row_start_buttons.rowconfigure(1, weight=1, uniform=u2)
        # Row 0 Column 1
        # 1 column
        self.column_game_record.columnconfigure(0, weight=1, uniform=u)
        # 3 rows: solve, my games and all games buttons
        for c in range(3):
            self.column_game_record.rowconfigure(c, weight=1, uniform=u2)
        # Row 0 Column 2
        # 1 column
        self.column_timer.columnconfigure(0, weight=1, uniform=u)
        # 3 rows for times display, row span 3
        for c2 in range(3):
            self.column_timer.rowconfigure(c2, weight=1, uniform=u2)
        # Row 0 Column 3
        # 1 column
        self.column_level_buttons.columnconfigure(0, weight=1, uniform=u)
        # 3 rows for each difficulty button
        for c3 in range(3):
            self.column_level_buttons.rowconfigure(c3, weight=1, uniform=u2)
        # Row 1 Alphabet letters
        # 13 columns half of the English alphabet buttons
        for x in range(13):
            self.row_abc_buttons.columnconfigure(x, weight=1, uniform=u)
        # 2 rows: 2 x 13 = 26 letters
        self.row_abc_buttons.rowconfigure(0, weight=1, uniform=u2)
        self.row_abc_buttons.rowconfigure(1, weight=1, uniform=u2)
        # Row 2 countdown and word labels
        # Row 2 place of the remaining chances and secret word
        # 2 columns: countdown label, word display label
        self.row_countdown_word.columnconfigure(0, weight=1, uniform=u)
        self.row_countdown_word.columnconfigure(1, weight=1, uniform=u)
        # 1 row
        self.row_countdown_word.rowconfigure(0, weight=1, uniform=u2)
        # Row 3 categories
        # 4 columns: half of the category buttons
        for n in range(0, 4):
            self.row_category_buttons.columnconfigure(n, weight=1, uniform=u)
        # 2 row: 2 x 4 = 8 categories including random button
        self.row_category_buttons.rowconfigure(0, weight=1, uniform=u2)
        self.row_category_buttons.rowconfigure(1, weight=1, uniform=u2)

    # noinspection PyUnusedLocal
    def build_title_label(self, *args):
        """Informative label to display a greeting if logged in and category selection display"""
        # Setting background and foreground colours of the informative label
        bg, fg = var.set_buttons_color('title')
        title = Label(
            self.row_start_buttons, text=self.banner_text.get(),
            bg=bg, fg=fg,
            font=var.get_font_size(self.rem, 10),
            width=6
        )
        # Adding to firs row and last 10 columns
        title.grid(
            row=0, column=5, rowspan=2, columnspan=10,
            sticky='ew', padx=5, pady=2
        )

    # noinspection PyUnusedLocal
    def build_countdown_label(self, *args):
        """Creates a label for countdown"""
        # setting font size related to main window size
        em = self.master.winfo_width() // 50
        # Countdown label added to first row (0) and column (0)
        # noinspection PyAttributeOutsideInit
        self.count = Label(
            self.row_countdown_word, textvariable=self.counter,
            bg=var.colours['bg'], fg=var.colours['7'],
            font=('Times new Roman', int(4.5*em), 'bold'),
        )
        self.count.grid(
            row=0, column=0,
            sticky='nws', padx=2*em, pady=5
        )

    # noinspection PyUnusedLocal
    def build_clock_label(self, *args):
        """Creates a label to display time"""
        # Label colour
        bg, fg = var.set_buttons_color('points')
        # Time label added to first row and column
        # noinspection PyAttributeOutsideInit
        self.clock = Label(
            self.column_timer, textvariable=self.clock_text,
            bg=bg, fg=fg,
            font=var.get_font_size(self.rem, 0),
            bd=0,
            width=2
        )
        self.clock.grid(row=0, column=0, sticky='news', padx=0, pady=0)

    # noinspection PyUnusedLocal
    def build_timer_label(self, *args):
        """Creates label for timer"""
        # Label colour added to second row and first column
        bg, fg = var.set_buttons_color('timer')
        # noinspection PyAttributeOutsideInit
        self.timer = Label(
            self.column_timer,
            text=self.timer_text.get(),
            bg=bg, fg=fg,
            font=var.get_font_size(self.rem, 14)
        )
        self.timer.grid(row=1, column=0, rowspan=2, sticky='nsew')

    # noinspection PyUnusedLocal
    def build_word_label(self, *args):
        """Creates label to display secret word"""
        # Label colour added to first row and second column
        bg, fg = var.set_buttons_color('word')
        # noinspection PyAttributeOutsideInit
        self.secret_word_label = Label(
            self.row_countdown_word, textvariable=self.word_text,
            bg=bg, fg=fg, justify=RIGHT,
            font=var.get_font_size(self.rem, 16), anchor='e'
        )
        self.secret_word_label.grid(row=0, column=1,
                                    sticky='nse',
                                    padx=20, pady=5)

    # noinspection PyUnusedLocal
    def timer_alert(self, *args):
        """Display a message if timer ended"""
        if not self.time_left.get():
            var.message("YOU LOST!", var.result['lose'])
            self.game_status_action()

    def draw_word(self):
        """Drawing the secret word displayed in undescores"""
        # output list later converted to string
        output = []
        # Draws the displayed word after each letter choice
        for x in self.secret_word.get():
            # Conditional for difficulty level, easy than add first and last letters
            if self.difficulty_status == 1:
                # Conditional for each letter in secret word if it's in first or last letter or already guessed letter
                if x in self.first_last \
                        or x in self.guessed_letters \
                        or x in [' ', '-']:
                    # if one of them true add to the letter to the output list
                    output.append(x)
                # conditional if is the selected letter
                elif x == self.selected_char:
                    output.append(self.selected_char)
                # Conditional if all above fails
                else:
                    output.append('_')
            # Conditional for difficulty level medium and hard displaying only dashes
            elif self.difficulty_status >= 2:
                # Conditional for secret letter if is in guessed letter or equals with empty space or dash
                if x in self.guessed_letters or x in [' ', '-']:
                    # if conditional true add to output list
                    output.append(x)
                # Conditional if secret letter is the selected letter than adding the selected letter to the list
                elif x == self.selected_char:
                    output.append(self.selected_char)
                # Conditional if all above fails, adds an underscore
                else:
                    output.append('_')

        # Joining the characters from the list to form the output string
        self.word_text.set(' '.join(output))

    def game_status_action(self):
        """Events to be handled when it's called"""
        # Secret word set to main info for category selection
        self.word_text.set('Choose your category')
        # Countdown set to empty string to not display anything
        self.counter.set('')
        # Start and stop buttons event call for stop
        self.start_stop_action('stop')
        # Info label set to Random
        self.banner_text.set('Random')
        # Quit button enabled
        self.quit.config(state=NORMAL)
        # Back button enabled
        self.back.config(state=NORMAL)
        # Solve button disabled and foreground changed to default
        self.solve.config(state=DISABLED, bg=var.colours['fg'])
        # Sets difficulty level buttons state to default
        self.set_level_buttons(self.difficulty_status)
        # set timer label to time
        self.timer_text.set(strftime("%H:%M"))

    def game_status(self):
        """Checks if it's a win or a loss
        Also changes the countdown label foreground color
        depending to the misses"""
        # Conditional for missed guesses
        if len(self.wrong_letters) == 7:
            # Displays a message
            var.message("YOU lost!", var.result['lose'])
            self.game_status_action()
        # Boolean for record
        # Conditional for sorted guessed letters and the secret word, if true creates a new game record
        if sorted(self.guessed_letters) == sorted(self.sorted_word):
            # creates a game record solved=False
            self.create_record()

    def build_abc_buttons(self):
        """Creates the alphabet buttons"""
        # noinspection PyAttributeOutsideInit
        r, c = 0, 0
        # Looping through alphabet
        for item in var.ALPHABET:
            b = Button(
                self.row_abc_buttons, text='%s' % item,
                bg=var.colours['bg'], fg=var.colours['fg_abc'],
                font=var.get_font_size(self.rem, 1),
                command=lambda i=item: self.abc_buttons_event(i),
                justify='center', overrelief=SUNKEN,
                anchor=CENTER, bd=0, state=DISABLED,
                disabledforeground=var.colours['dfg_abc'],
                activeforeground=var.colours['afg_abc'],
                activebackground=var.colours['abg_abc'],
            )
            # Conditional to change row when 13 letters reached
            if c == 13:
                r += 1
                # sets column to first (0)
                c = 0
            b.grid(row=r, column=c, sticky='news', padx=7, pady=6)
            # Adding button to the button list
            self.abc_buttons.append(b)
            c += 1

        # print(type(self.abc[0]))

    def build_category_buttons(self):
        """Creates category buttons"""
        # row, column, background, state of the button
        r, c, bg, s = 0, 0, var.colours['bg_cat_a'], NORMAL
        # Looping through category names
        for item in var.categories:
            # Conditional for checking the category if it's random
            if item == 'random':
                bg = var.colours['fg']
                s = DISABLED
            # lambda to point the event to another function
            b = Button(
                self.row_category_buttons, text='%s' % item.capitalize(),
                bg=bg, fg=var.colours['fg_cat'],
                font=var.get_font_size(self.rem, 8),
                command=lambda i=item: self.category_buttons_event(i),
                overrelief=SUNKEN,
                anchor=CENTER, bd=1, state=s,
                disabledforeground=var.colours['bg'],
                activeforeground=var.colours['fg_cat'],
                activebackground=var.colours['bg_cat_a'],
                width=1
            )
            # Conditional for column if reached 4, increment row by 1 and set column back to first (0)
            if c == 4:
                r += 1
                c = 0
            b.grid(row=r, column=c, sticky='news', padx=15, pady=10)
            # Adding button to the category list
            self.category_buttons.append(b)
            c += 1

    def buttons(self):
        """Crates the rest of the buttons which are not alphabet or category"""
        # Start button
        # noinspection PyAttributeOutsideInit
        self.start = self.button_builder(self.row_start_buttons, 'start')
        self.start.config(width=2, font=var.get_font_size(self.rem, -2))
        self.start.grid(row=0, column=0,
                        sticky='news', padx=20, pady=7)
        # Stop button
        # noinspection PyAttributeOutsideInit
        self.stop = self.button_builder(self.row_start_buttons, 'stop')
        self.stop.config(state=DISABLED, width=2, font=var.get_font_size(self.rem, -2))
        self.stop.grid(row=1, column=0,
                       sticky='news', padx=20, pady=7)
        # Solve button
        # noinspection PyAttributeOutsideInit
        self.solve = self.button_builder(self.column_game_record, 'solve')
        self.solve.config(font=var.get_font_size(self.rem, -2),
                          overrelief=None, relief=SOLID, bd=1, state=DISABLED,
                          bg=var.colours['fg'])
        self.solve.grid(row=0, column=0, sticky='news', padx=0, pady=0)

        # My games button
        # noinspection PyAttributeOutsideInit
        self.my_games = self.button_builder(self.column_game_record, 'my games')
        self.my_games.config(font=var.get_font_size(self.rem, -2),
                             overrelief=None, relief=SOLID, bd=1,
                             command=lambda: all_time_records(self.rem, self.user_id))
        self.my_games.grid(row=1, column=0, sticky='news', padx=0, pady=0)
        # All games button
        # noinspection PyAttributeOutsideInit
        self.all_games = self.button_builder(self.column_game_record, 'all games')
        self.all_games.config(font=var.get_font_size(self.rem, -2),
                              overrelief=None, relief=SOLID, bd=1,
                              command=lambda: all_time_records(self.rem))
        self.all_games.grid(row=2, column=0, sticky='news')

        # Gign in button
        # noinspection PyAttributeOutsideInit
        self.signin = self.button_builder(self.login, 'login')
        self.signin.config(font=var.get_font_size(self.rem, 16),
                           text='Play as member', bd=1)
        self.signin.grid(row=3, column=1, sticky='news', padx=110, pady=10)
        # Register confirm button
        # noinspection PyAttributeOutsideInit
        self.register = self.button_builder(self.signup, 'register')
        self.register.config(font=var.get_font_size(self.rem, 12),
                             text='Join', bd=1)
        self.register.grid(row=6, column=1, sticky='news', padx=110, pady=10)
        # Guest enter button
        # noinspection PyAttributeOutsideInit
        self.guest_enter = self.button_builder(self.login, 'guest')
        self.guest_enter.config(font=var.get_font_size(self.rem, 12),
                                text='Play as guest', bd=1)
        self.guest_enter.grid(row=4, column=1, sticky='news', padx=110, pady=15)
        # Become button
        # noinspection PyAttributeOutsideInit
        self.to_reg = self.button_builder(self.login, 'become')
        self.to_reg.config(font=var.get_font_size(self.rem, 6),
                           text='Become a member', bd=0, fg=var.colours['fg_abc'])
        self.to_reg.grid(row=5, column=1, sticky='news', padx=110, pady=15)

        # creating png variblas to be added later on to the buttons
        close = var.get_png('quit')
        info = var.get_png('help')
        rule = var.get_png('rule')
        back = var.get_png('back')
        # Information button
        # noinspection PyAttributeOutsideInit
        self.info = self.button_builder(self.login, 'info')
        self.info.config(font=var.get_font_size(self.rem, 0),
                         command=lambda: var.message('Game Info', var.prompt['Game Info']),
                         image=info, bd=0)
        # Adding the image to the button
        self.info.image = info
        self.info.place(relx=0.01, rely=0.02, anchor='nw')
        # Rule button
        # noinspection PyAttributeOutsideInit
        self.rule = self.button_builder(self.master, 'rules')
        self.rule.config(font=var.get_font_size(self.rem, 0), bd=0,
                         command=lambda: var.message('Game Rules', var.prompt['Game Rules']),
                         image=rule)
        # Adding the image to the button
        self.rule.image = rule
        self.rule.place(relx=0.96, rely=0.02, anchor='ne')
        # Exit button
        # noinspection PyAttributeOutsideInit
        self.quit = self.button_builder(self.master, 'exit')
        self.quit.config(font=var.get_font_size(self.rem, 1),
                         image=close, bd=0)
        # Adding image to the button
        self.quit.image = close
        self.quit.place(relx=0.99, rely=0.02, anchor='ne')
        # Back button
        # noinspection PyAttributeOutsideInit
        self.back = self.button_builder(self.master, 'back')
        self.back.config(font=var.get_font_size(self.rem, 1),
                         image=back, bd=0, state=DISABLED)
        # Adding image to the button
        self.back.image = back
        self.back.place(relx=0.93, rely=0.02, x=0, y=0, anchor='ne')

        r, s, bg = 0, NORMAL, var.colours['bg_level']
        # Looping through difficulty levels
        for item in ['hard', 'medium', 'easy']:
            b = self.button_builder(self.column_level_buttons, item)
            # Conditional to set the button state disabled as default the first choice
            if item == 'easy':
                s = DISABLED
                bg = var.colours['fg']
            b.config(state=s, font=var.get_font_size(self.rem, -4),
                     command=lambda i=item: self.level_buttons_event(i), bg=bg)
            b.grid(row=r, column=0, sticky='news', pady=3)
            self.difficulty_buttons.append(b)
            r += 1

    @staticmethod
    def exit_button_event():
        """Static method to display a goodbye message and exit application"""
        var.message('Bye', var.prompt['Bye'])
        try:
            # Adding a little delay before exit
            sleep(0.6)
            sys.exit()
        except NotImplementedError:
            pass

    def abc_buttons_event(self, item):
        """Sets the alphabet buttons to the desired state
        depending to guesses and misses.
        calls the draw_word and game_status methods
        """
        # Setting the selected char to alphabet button letter
        self.selected_char = item
        # background, disabled foreground colours, state
        bg, dfg, s = var.colours['bg'], var.colours['dfg_abc_r'], DISABLED
        # Conditional to check letter in secret word
        if item in self.secret_word.get():
            # Resetting the above variables if true
            bg, dfg, s = var.colours['bg'], var.colours['dfg_abc_g'], DISABLED
            # letter added to guessed letters list
            self.guessed_letters.append(item)
        else:
            # If condition fails add to the wrongly guessed list
            self.wrong_letters.append(item)
        index = 0
        # Looping through alphabet
        for x in var.ALPHABET:
            # Adding letters to a dictionary paired with an index value to configure later
            # the corresponding button index in the button list
            # The letters are in alphabetical order positioned as a list
            self.abc_buttons_dict.update({x: index})
            index += 1
        # Updating the corresponding button related to item = letter
        self.abc_buttons[self.abc_buttons_dict[item]].config(state=s, bg=bg, disabledforeground=dfg)
        # Setting up a variable for the countdown label to display the remaining chances
        c = 7 - len(self.wrong_letters)
        if c == 0:
            c = 7
        self.counter.set(f'{c}')
        # setting the countdown colour
        self.count.config(fg=var.colours[f'{c}'])
        # redrawing the word if guessed
        self.draw_word()
        # calling game status
        self.game_status()

    def start_stop_action(self, text):
        """Event for start and stop buttons event handler"""
        # bc = background colour for category button for 7 buttons
        # ba = background colour for category button for 1 selected
        # bb = background colour for abc buttons
        # dfg = disabled foreground colour
        # s = state for start button
        # s_2 = state for stop button
        # s_3 = state for abc buttons
        bc, ba, bb, dfg, s, s_2, s_3 = None, None, None, None, None, None, None
        sbg, stbg = None, None
        if text == 'start':
            # Conditional to set Time label to timer if difficulty level is 3
            if self.difficulty_status == 3:
                self.clock_text.set('Timer')
            # Looping through difficulty level to set the state disabled while game running
            for x in range(3):
                if self.difficulty_buttons[x].cget('state') == 'disabled':
                    continue
                else:
                    self.difficulty_buttons[x].config(state=DISABLED)
            # Resetting variables to different colour when start event it's called
            bc, ba, bb, dfg = var.colours['fg'], var.colours['fg'], var.colours['bg_abc_a'], var.colours['bg']
            s, s_2, s_3 = DISABLED, NORMAL, NORMAL
            sbg, stbg = var.colours['fg'], var.colours['bg_stop']

        if text == 'stop':
            # If conditional true, game stopped:
            # first_last list cleared
            self.first_last.clear()
            # the guessed list cleared
            self.sorted_word = ''
            # Info label set to empty string
            self.banner_text.set('')
            # sets Timer label to Time
            self.clock_text.set('Clock')
            # game running is false
            self.running = False
            # resets difficulty level buttons to default
            self.set_level_buttons(self.difficulty_status)
            # Resetting variables to different colour when stop event it's called
            bc, ba, bb, dfg = var.colours['bg_cat_a'], var.colours['fg'], var.colours['bg'], var.colours['fg']
            s, s_2, s_3 = NORMAL, DISABLED, DISABLED
            sbg, stbg = var.colours['bg_start'], var.colours['fg']

        # Setting start and stop buttons to default
        self.start.config(state=s, bg=sbg)
        self.stop.config(state=s_2, bg=stbg)
        # Looping through category buttons and setting state and background to selected category
        for a in range(8):
            if self.category_buttons[a].cget('text').lower() == self.prompt.get():
                self.category_buttons[a].config(state=DISABLED, bg=ba)
            else:
                self.category_buttons[a].config(state=s, bg=bc)
        # Looping through abc buttons to disable which letter are already guessed in first_last list
        for i in range(0, 26):
            if self.difficulty_status == 1:
                if self.abc_buttons[i].cget('text') in self.first_last:
                    self.abc_buttons[i].config(bg=var.colours['bg'], state=DISABLED,
                                               disabledforeground=var.colours['dfg_abc_g'])
                else:
                    self.abc_buttons[i].config(bg=bb, disabledforeground=dfg, state=s_3)
            else:
                self.abc_buttons[i].config(bg=bb, disabledforeground=dfg, state=s_3)

    def start_button_event(self):
        """Start button event handler"""
        # resetting timer variable to 1 minute
        self.time_left.set(60)
        # game running true
        self.running = True
        # countdown set to default 7
        self.counter.set('7')
        # setting the secret word and displaying the hidden letters
        self.set_secret_word()
        # disable quit and back buttons
        self.quit.config(state=DISABLED)
        self.back.config(state=DISABLED)
        # enable solve button
        self.solve.config(state=NORMAL, bg=var.colours['bg_start'])
        # calling event for start button
        self.start_stop_action('start')

    def stop_button_event(self):
        """Stop button event handler"""
        # setting displayed secret word text to information status
        self.word_text.set('Choose your category')
        # setting countdown to empty string
        self.counter.set('')
        # enable quit and back buttons
        self.quit.config(state=NORMAL)
        self.back.config(state=NORMAL)
        # enable solve button
        self.solve.config(state=DISABLED, bg=var.colours['fg'])
        # calling event for stop
        self.start_stop_action('stop')
        # set time text to current time
        self.timer_text.set(strftime("%H:%M"))

    def guest_button_event(self):
        """Guest enter button event handler"""
        # clears login entry fields for new input
        self.clear_login_fields()
        # Unmapping login frame
        self.login.pack_forget()
        # disable my games button for guest
        self.my_games.config(state=DISABLED, bg=var.colours['fg'])
        # mainframe remapping to main screen
        self.mainframe.pack(fill=BOTH, expand=True)

    def login_button_event(self):
        """Login button event"""
        # variable for username and password got from input entry fields
        username, password = (self.login.entries[i].get() for i in range(2))
        # user data from database for verification
        query = user(username)
        # Conditional to check data existence
        if query.exists():
            # Conditional for password check
            if check_password_hash(query.first().password, password):
                # setting user id for game record
                self.user_id = query.first().id
                # clear entry fields
                self.clear_login_fields()
                # setting info label to greeting with added user name
                self.banner_text.set("Welcome " + query.first().first_name)
                # enable my games button for registered user
                self.my_games.config(state=NORMAL, bg=var.colours['bg_score'])
                # unmapping login frame
                self.login.pack_forget()
                # remapping mainframe
                self.mainframe.pack(fill=BOTH, expand=True)
            else:
                # if password check fails display password error message
                var.message("Password Error", "Password not correct!")
        else:
            # if data doesn't exists display not existing user error message
            var.message("Query Error", "This user doesn't exists!")

    def become_button_event(self):
        """Become button event to launch registration"""
        # Clear login frame entry fields
        self.clear_login_fields()
        # Unmapping login frame
        self.login.pack_forget()
        # Remapping signup frame
        self.signup.pack(fill=BOTH, expand=True)

    def registration_button_event(self):
        """Registration button event"""
        # validator form for registration from forms.py
        validator = UserForm()
        # data dictionary
        data = {}
        # registration fields list for dictionary
        reg_fields = ['first_name', 'last_name', 'username', 'password']
        # tuple of tuple pair: filed count and registration fields
        entries = zip(range(len(self.signup.entries)), reg_fields)
        # Looping through tuple pair and adding each field with input entry to data dictionary
        for index, d in entries:
            data.update({d: self.signup.entries[index].get()})
        # validating data dictionary with the validator form defined above
        validator.validate(data)
        # Conditional for checking any validation error (missing input) and check password match
        if len(validator.errors.values()) == 0 and self.check_password():
            # creates a new user returning any exception error
            u = User().create_user(**data)
            # Conditional to check the above error
            if u is None:
                # if none registration is successful
                var.message("Success", "Registration successful")
                # Looping through input entries to focus cursor on first field
                for i in range(len(self.signup.entries)):
                    if i == 0:
                        self.signup.entries[i].focus()
                    # deleting input from each field
                    self.signup.entries[i].delete(0, "end")
                # signup frame unmapping
                self.signup.pack_forget()
                # remapping login frame
                self.login.pack(fill=BOTH, expand=True)
                # disable back button
                self.back.config(state=DISABLED)
            else:
                # if condition fails, shows the returned error
                var.message("Record Error", u)
        # if validation error exists, shows validation error message
        elif len(validator.errors.values()) != 0:
            var.message("Validation Error", validator.errors)

    def back_button_event(self):
        """Back button event"""
        # Unmapping mainframe
        self.mainframe.pack_forget()
        # Unmapping signup frame
        self.signup.pack_forget()
        sleep(0.4)
        # Remapping login frame
        self.login.pack(fill=BOTH, expand=True)
        # sets user id to none
        self.user_id = None
        # sets info and secret word to empty string
        self.banner_text.set("")
        self.secret_word.set("")
        # enable 1 difficulty level button
        self.difficulty_buttons[0].config(state=NORMAL)
        # enable 2 difficulty level button
        self.difficulty_buttons[1].config(state=NORMAL)
        # disable 3 difficulty level button
        self.difficulty_buttons[2].config(state=DISABLED)
        # enable my games button and sets background to default
        self.my_games.config(state=NORMAL, bg=var.colours['bg_score'])
        # setting difficulty level to easy
        self.difficulty_status = 1
        # sets difficulty buttons background and foreground
        self.set_level_buttons(1)
        # enable back button
        self.back.config(state=DISABLED)
        # clears first and last letters from the list
        self.first_last.clear()

    def solve_button_event(self):
        """Calls solve window"""
        self.solve_screen()

    def ok_solve_button_event(self):
        """Solve screen ok button event"""
        # for adding to database
        # Conditional to check entered word matches secret word, lowered cases to avoid error
        if self.entry.get().lower() == self.secret_word.get().lower():
            # resetting timer to 1 minute
            self.time_left.set(60)
            # creates a game record solved=True
            self.create_record(True)
        else:
            # if condition fails shows message with negative result
            var.message("YOU LOST!", var.result['lose'])
            # calling game status events
            self.game_status_action()
            # exits screen
            self.master_3.destroy()

    def cancel_button_event(self):
        """Cancel button. Game continues, solved screen destroyed"""
        self.master_3.destroy()

    def set_secret_word(self):
        """Sets the secret word by the user category choice choice or random by default"""
        # clears guessed letters list
        self.guessed_letters.clear()
        # clears missed letters list
        self.wrong_letters.clear()
        # selected char set to empty string
        self.selected_char = ''
        # selected category
        search = self.prompt.get()
        # list of all categories
        categories = var.categories

        # Conditional t check if selected category is random
        if search.lower() == 'random':
            from random import choice
            # if true a random category is selected
            search_query = choice(categories)
        else:
            # if selected not random than remains selected
            search_query = search.lower()

        # Opens available words.csv from csv file
        try:
            # get a random word and set to upper case all letters
            word = get_word(search_query).upper()
            # Conditional to check if word was played before
            if word in self.played_words:
                # if true get again another word set to upper case
                word = get_word(search_query).upper()
            # setting secret word
            self.secret_word.set(word)
            # Looping through word letter by letter
            for x in word:
                # Conditional to add first and last letters to a list for easy level
                if x == word[0] or x == word[len(word) - 1]:
                    if x.upper() in self.first_last:
                        continue
                    self.first_last.append(x.upper())
            # Conditional to add the first and last letter for easy level
            if self.difficulty_status == 1:
                self.sorted_word = var.sort(word)
            else:
                # the medium and hard difficulty level
                self.sorted_word = var.sort(word, True)
            # redrawing the displayed secret word
            self.draw_word()
            # setting info label to selected category
            self.banner_text.set(search_query.capitalize())
        except NotImplementedError:
            pass

    def set_buttons_command(self, text):
        """Returns a direction to text related button event.
        NOTE: without () the function it's not called!"""
        command = None
        if text == 'start':
            command = self.start_button_event
        elif text == 'stop':
            command = self.stop_button_event
        elif text == 'exit':
            command = self.exit_button_event
        elif text == 'guest':
            command = self.guest_button_event
        elif text == 'login':
            command = self.login_button_event
        elif text == 'become':
            command = self.become_button_event
        elif text == 'register':
            command = self.registration_button_event
        elif text == 'back':
            command = self.back_button_event
        elif text == 'solve':
            command = self.solve_button_event
        elif text == 'ok':
            command = self.ok_solve_button_event
        return command

    def category_buttons_event(self, text):
        """Category buttons state event to set buttons availability"""
        self.prompt.set(text)
        # Looping through each category button including random button to enable or disable
        for a in range(8):
            if self.category_buttons[a].cget('text').lower() == text:
                self.category_buttons[a].config(state=DISABLED, bg=var.colours['fg'])
            else:
                self.category_buttons[a].config(state=NORMAL, bg=var.colours['bg_cat_a'])

    def level_buttons_event(self, text):
        """Difficulty level buttons state event to set buttons state"""
        if text == 'hard':
            self.difficulty_status = 3
        if text == 'medium':
            self.difficulty_status = 2
        if text == 'easy':
            self.difficulty_status = 1
        # Looping through difficulty buttons to enable or disable
        for x in range(3):
            if self.difficulty_buttons[x].cget('text').lower() == text:
                self.difficulty_buttons[x].config(state=DISABLED, bg=var.colours['fg'])
            else:
                self.difficulty_buttons[x].config(state=NORMAL, bg=var.colours['bg_level'])

    def set_level_buttons(self, level):
        """same function as above just from integer variable set the state of the buttons"""
        for i in range(3):
            if self.difficulty_buttons[i].cget('text').lower() == var.int_to_levels[level]:
                self.difficulty_buttons[i].config(state=DISABLED, bg=var.colours['fg'])
            else:
                self.difficulty_buttons[i].config(state=NORMAL, bg=var.colours['bg_level'])

    def clear_login_fields(self):
        """Clears login input and enables back button"""
        self.login.entries[0].delete(0, "end")
        self.login.entries[0].focus()
        self.login.entries[1].delete(0, "end")
        sleep(0.6)
        self.back.config(state=NORMAL)

    def check_password(self):
        """
        Password and check-password check. Makes sure that both passwords are the same
        in case of registration of user or driver.
        :returns: - boolean
        """
        # Conditional to check last to inputs, password fields
        if self.signup.entries[-1].get() != self.signup.entries[-2].get():
            var.message("Password error", "Password doesn't match!")
            return False
        return True

    def update(self):
        """Master window refresh rate, 1 second"""
        # time left for hard difficulty level
        time_left = self.time_left.get()
        # 3 conditions to set timer
        if self.running and time_left and self.difficulty_status == 3:
            minutes, seconds = var.get_time(time_left)
            # Timer text set to 1 minute
            self.timer_text.set(
                '{:0>2}:{:0>2}'.format(minutes, seconds)
            )
            # than subtracting 1 each 1000 millisecond
            self.time_left.set(time_left - 1)
        # call main screen after 1000 millisecond
        self.master.after(1000, self.update)


if __name__ == '__main__':
    # new TK object with defined class name
    root = Tk(className='Guess Letter v1.0')
    # Calling GUI class with Tk as master
    GameGUI(root)
    # call of a loop method witch prevents closing of the main screen
    root.mainloop()
