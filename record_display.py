#!/usr/bin/env python3
# NOTE: noinspection -> comments are only for Pycharm editor to comply with PEP8 regulations!

from tkinter import Tk, Frame, Button, BOTH
import variables as st
from record import User, GameRecord
from table import Table


"""
Degree:         Faculty of Creative Arts, Technologies and Science
Department:     Computer Science and Technology
University:     University of Bedfordshire
Author:         Oszkar Feher
Date:           21 October 2022
"""


def all_time_records(rem, user_id=None):
    """Crates a new window to display records"""
    # New Tk class
    # noinspection PyAttributeOutsideInit
    master = Tk(className="All records")
    # Frame for the window
    # noinspection PyAttributeOutsideInit
    frame = Frame(master, bg=st.colours['fg'],
                  highlightbackground=st.colours['fg_enter'],
                  highlightcolor=st.colours['fg_enter'],
                  highlightthickness=3)
    # width, height of the window
    x, y = 850, 550
    # for the user one column less, the window has to be smaller
    if user_id:
        x, y = 646, 550
    # dimensions for geometry: width, height, x position, y position on the mani screen
    dimensions = (x, y, int(master.winfo_screenwidth() // 2 - x / 2),
                  int(master.winfo_screenheight() // 2 - y / 2))
    # creating the screen
    master.geometry('{}x{}+{}+{}'.format(*dimensions))
    # Removing minimise and closing ability
    master.overrideredirect(True)
    # Idle till further instructions
    master.update_idletasks()
    # frame added to main window
    frame.pack(fill=BOTH, expand=True)

    # Dataset list to be displayed in a table
    data = [i for i in GameRecord.select(GameRecord.id, User.first_name,
                                         GameRecord.level, GameRecord.guesses,
                                         GameRecord.misses).join(User).tuples()]
    # columns for the table
    fields = ['Nr', 'User', 'Difficulty', 'Guesses', 'Missed']
    # if there is a user change the dataset and columns
    if user_id:
        data = [i for i in GameRecord.select(GameRecord.id, GameRecord.level, GameRecord.guesses,
                                             GameRecord.misses).join(User).where(GameRecord.user_id == user_id).tuples()]
        fields = ['Nr', 'Difficulty', 'Gueses', 'Missed']
    # Creates a table
    Table(frame, rem, data, fields, 0, 0)

    # Creates a button for main window
    ok = Button(frame, bg=st.colours['bg'],
                bd=1, fg=st.colours['fg_enter'], font=st.get_font_size(rem, 3),
                text='Ok', command=lambda: master.destroy(),
                activeforeground='black', activebackground=st.colours['fg'], width=10)
    ok.place(relx=0.5, rely=0.96, anchor='s')
