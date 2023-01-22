#!/usr/bin/env python3
# NOTE: noinspection -> comments are only for Pycharm editor to comply with PEP8 regulations!
# Graphical elements for a new frame
from tkinter import Frame, Label, Entry, CENTER
import variables as var


"""
Degree:         Faculty of Creative Arts, Technologies and Science
Department:     Computer Science and Technology
University:     University of Bedfordshire
Author:         Oszkar Feher
Date:           21 October 2022
"""


class BaseFrame(Frame):
    """BaseFrame class for all Frames.
    :inherit: Frame from tkinter"""
    def __init__(self, master=None):
        """Constructor"""
        # Call of constructor of parent class Frame.
        Frame.__init__(self, master)
        self.master = master
        self.config(bg=var.colours['bg'])
        self.build_grid()

    def build_grid(self):
        """Default grid layout for each Frame."""
        # uniform, weight column, weight row
        u, wc, wr = None, 1, 0
        self.grid_columnconfigure(0, weight=wc, uniform=u)
        self.grid_rowconfigure(0, weight=wr, uniform=u)


class LogIn(BaseFrame):
    """LogIn class for log in input display.
    :inherit: BaseFrame"""
    def __init__(self, master=None, rem=None):
        """Constructor"""
        # Call of constructor of parent class BaseFrame to overwrite
        BaseFrame.__init__(self, master)
        self.rem = rem
        self.entries = []

        self.build_labels()
        self.build_entry()

    def build_grid(self):
        """Creates grid for frame."""
        BaseFrame.build_grid(self)
        # uniform, weight for column, weight for row
        u, wc, wr = None, 1, 0
        # 3 columns and 6 rows for the input field, label and button
        for i in range(3):
            self.grid_columnconfigure(i, weight=wc, uniform=u)
        for r in range(6):
            self.grid_rowconfigure(r, weight=wr, uniform=u)

    def build_labels(self):
        """Creates labels."""
        # background, foreground colours for welcome label added to first row and column
        bg, fg = var.set_buttons_color('title')
        welcome = Label(self,
                        text='Welcome to Guess Letters',
                        bg=bg, fg=fg,
                        font=var.get_font_size(self.rem, 24),
                        justify=CENTER
                        )
        welcome.config(font=var.get_font_size(self.rem, 24), )
        welcome.grid(row=0, column=0, sticky='ns', padx=30, pady=30, columnspan=3)

        # Input label names
        labels = ['Username', 'Password']
        # background, foreground colours for the labels added on to rows with a loop
        bg, fg = var.set_buttons_color('score')
        for i in range(len(labels)):
            Label(self, text=labels[i],
                  bg=bg, fg=fg,
                  font=var.get_font_size(self.rem, 5)
                  ).grid(row=i + 1, column=0, sticky='nes', padx=5, pady=35)

    def build_entry(self):
        """Creates input entry."""
        # parameter to show the input value to the user or to not show
        show = ""
        # background, foreground colours for the input entry
        bg, fg = var.set_buttons_color('timer')
        # Looping through the input fields to hide the password
        for i in range(2):
            if i == 1:
                show = "*"
            e = Entry(self, show=show,
                      bg=bg, fg=fg, bd=1, width=20,
                      font=var.get_font_size(self.rem, 10))
            e.grid(row=1 + i, column=1, sticky='ns', padx=0, pady=30, columnspan=1)
            # Adding entries to the entry list
            self.entries.append(e)


class Register(BaseFrame):
    """Register class for registration input display.
    :inherit: BaseFrame"""

    def __init__(self, master=None, rem=None):
        """Constructor"""
        # Call of constructor of parent class BaseFrame to overwrite
        BaseFrame.__init__(self, master)
        # base font size
        self.rem = rem
        # entry fields list
        self.entries = []

        self.build_labels()
        self.build_entry()

    def build_grid(self):
        """Creates grid for frame."""
        BaseFrame.build_grid(self)
        # uniform, weight column, weight row
        u, wc, wr, r = None, 1, 0, 7
        # 3 columns and 7 rws
        for i in range(3):
            self.columnconfigure(i, weight=wc, uniform=u)
        for i in range(r):
            self.rowconfigure(i, weight=wr, uniform=u)

    def build_labels(self):
        """Creates labels."""
        # background, foreground colours for label
        bg, fg = var.set_buttons_color('title')
        # Info label
        prompt = Label(self,
                       text='Create an account',
                       bg=bg, fg=fg,
                       font=var.get_font_size(self.rem, 12),
                       justify=CENTER
                       )
        prompt.grid(row=0, column=0, sticky='ns', padx=30, pady=30, columnspan=3)
        # background, foreground colours for input labels
        bg, fg = var.set_buttons_color('score')
        # Input fields name
        labels = ['First Name', 'Last Name', 'Username', 'Password', 'Check-password']
        for i in range(len(labels)):
            Label(self, text=labels[i],
                  bg=bg, fg=fg,
                  font=var.get_font_size(self.rem, 5)
                  ).grid(row=i+1, column=0, sticky='nes', padx=5, pady=15)

    def build_entry(self):
        """Creates input entry"""
        # show (for password), rows to be selected for hidden input, number of rows
        show, rows, r = "", [3, 4], 5
        # background, foreground colours for input entry
        bg, fg = var.set_buttons_color('timer')
        for i in range(r):
            if i in rows:
                # To hide password input
                show = "*"
            e = Entry(self, show=show,
                      bg=bg, fg=fg, bd=1, width=20,
                      font=var.get_font_size(self.rem, 10))
            e.grid(row=i+1, column=1, sticky='ns', padx=5, pady=15)
            # Adding to the entry list
            self.entries.append(e)
