#!/usr/bin/env python3

# for creating an ordered dictionary
from collections import OrderedDict
# for adding image to buttons
from PIL import Image, ImageTk
# for display a message
from tkinter import messagebox


"""
Degree:         Faculty of Creative Arts, Technologies and Science
Department:     Computer Science and Technology
University:     University of Bedfordshire
Author:         Oszkar Feher
Date:           21 October 2022
"""


# Alphabet for the buttons
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Category list for category buttons
categories = ['animal', 'plant', 'object', 'geography',
              'invention', 'history', 'sport', 'random']

# Difficulty level dictionary
int_to_levels = {1: 'easy', 2: 'medium', 3: 'hard'}

# Message for win and lose
result = {'won': 'Congratulation\n'
                 'You won\n'
                 '\n'
                 'Word: {}\n'
                 'level: {}\n'
                 'Guesses: {}\n'
                 '\n',
          'lose': 'Game over\n'
                  'You lost\n'}

# Message for game rule and info
prompt = {'Game Rules': "The game follows the same rules\n"
                        "as Hangman.\n"
                        "Every bad guess will decrease the\n"
                        "the countdown.\n"
                        "Every new game has 7 bad guesses.\n"
                        "The words.csv are selected automatically \n"
                        "from all categories if it's not \n"
                        "selected manually.\n"
                        "After every game the selection jumps\n"
                        "back to all categories\n"
                        "Happy gaming!",
          'Game Info': "You can play as a guest\n"
                       "You can review all time games\n"
                        "If you login, you can review your played games\n"
                        "Not member, you can join by pressing\n"
                        '"Become member\n"',
          'Bye': 'Thank you for playing\nBye!'}

# Colours used through the application
colours = OrderedDict([
    ('bg', '#d8d8d8'),
    ('fg', '#8B8C8C'),
    ('1', '#FF0000'),
    ('2', '#FF7700'),
    ('3', '#FFC400'),
    ('4', '#FFFB00'),
    ('5', '#B7FF00'),
    ('6', '#7BFF00'),
    ('7', '#00FF15'),
    ('bg_info', '#DBDBDB'),
    ('abg_info', '#8B8C8C'),
    ('afg_info', '#3F4040'),
    ('fg_back', '#0008E3'),
    ('bg_level', '#D18EC7'),
    ('fg_level', '#4A033F'),
    ('bg_score', '#734A94'),
    ('fg_score', '#22013D'),
    ('bg_cat_a', '#0f9'),
    ('fg_cat', '#004A2C'),
    ('abg_cat', '#09f'),
    ('afg_cat', '#229DAB'),
    ('bg_start', '#77FF73'),
    ('fg_start', '#00540D'),
    ('dfg_start', '#bf0000'),
    ('afg_start', '#E60000'),
    ('abg_start', '#011400'),
    ('abg_stop', '#290101'),
    ('bg_stop', '#FF6B7F'),
    ('bg_abc_a', '#A5C2D6'),
    ('fg_abc', '#09f'),
    ('dfg_abc', '#aaa'),
    ('dfg_abc_g', '#0f2'),
    ('dfg_abc_r', '#f66'),
    ('afg_abc', '#333'),
    ('abg_abc', '#aaa'),
    ('fg_word', '#222'),
    ('dfg_word', '#818581'),
    ('fg_title', '#FF8C00'),
    ('fg_enter', '#404040')])

# Button colour setup background, foreground, active background, active foreground, disabled foreground
button_colours = OrderedDict([
    ('info', ['bg', 'fg', 'bg', 'afg_info', 'bg']),
    ('rules', ['bg', 'fg', 'bg', 'afg_info', 'bg']),
    ('ok', ['bg', 'fg', 'bg', 'afg_info', 'bg']),
    ('exit', ['bg', 'dfg_start', 'bg', 'dfg_start', 'bg_info']),
    ('all games', ['bg_score', 'bg', 'bg_score', 'fg_score', 'bg']),
    ('my games', ['bg_score', 'bg', 'bg_score', 'fg_score', 'bg']),
    ('start', ['bg_start', 'fg_start', 'bg_start', 'fg_start', 'bg']),
    ('solve', ['bg_start', 'fg_start', 'bg_start', 'fg_start', 'bg']),
    ('stop', ['fg', 'fg_start', 'bg_stop', 'fg_start', 'bg']),
    ('guest', ['bg', 'fg_enter', 'bg', 'fg_enter', 'bg']),
    ('login', ['bg', 'fg_enter', 'bg', 'fg_enter', 'bg']),
    ('become', ['bg', 'fg_enter', 'bg', 'fg_enter', 'bg']),
    ('register', ['bg', 'fg_enter', 'bg', 'fg_enter', 'bg']),
    ('ok', ['bg', 'fg_enter', 'bg', 'fg_enter', 'bg']),
    ('cancel', ['bg', 'fg_enter', 'bg', 'fg_enter', 'bg']),
    ('back', ['bg', 'fg_back', 'bg', 'fg_back', 'bg']),
    ('easy', ['bg_level', 'fg_level', 'bg_level', 'fg_level', 'bg']),
    ('medium', ['bg_level', 'fg_level', 'bg_level', 'fg_level', 'bg']),
    ('hard', ['bg_level', 'fg_level', 'bg_level', 'fg_level', 'bg']),
    ('score', ['bg', 'fg_start']),
    ('timer', ['bg', 'fg_enter']),
    ('word', ['bg', 'fg_enter']),
    ('welcome', ['bg', 'fg_title']),
    ('title', ['bg', 'fg_title']),
    ('points', ['fg', 'bg'])
])


def get_png(var):
    """return Tk image object for button"""
    img = Image.open('PNG/{}.png'.format(var))
    photo = ImageTk.PhotoImage(img)
    return photo


def set_buttons_color(text):
    """Sets buttons color"""
    return (colours[i] for i in button_colours[text])


def message(key, value):
    """Info, Rules, Bye message"""
    messagebox.showinfo(key, value)


def sort(item, boolean=False):
    """Arranges the secret word letters in alphabetical order"""
    char_list = []
    for x in item:
        if x in char_list:
            continue
        elif x in [' ', '-']:
            continue
        elif x == item[0] or x == item[len(item) - 1]:
            if boolean:
                char_list.append(x)
            continue
        else:
            char_list.append(x)
    return char_list


def get_font_size(unit, size):
    """Font setter for all the widgets"""
    f, s, sy = 'Comic Sans MS', 1, 'bold'
    rem = int(unit / 100 * (size * 0.05 + s))
    return f, rem, sy


def get_time(seconds):
    """Returns a tuple of integers for timing"""
    return int(seconds / 60), int(seconds % 60)
