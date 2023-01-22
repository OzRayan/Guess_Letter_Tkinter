#!/usr/bin/env python3

from random import choice
from csv import reader


"""
Degree:         Faculty of Creative Arts, Technologies and Science
Department:     Computer Science and Technology
University:     University of Bedfordshire
Author:         Oszkar Feher
Date:           21 October 2022
"""


def get_word(search_query):
    """Open the selected csv file and returns a random word"""
    # from csv import DictReader, DictWriter, reader, writer
    categories = ['animal', 'plant', 'object', 'geography',
                  'invention', 'history', 'sport']
    query = search_query
    if search_query == "random":
        query = choice(categories)
    try:
        with open(f'WORDS/{query}.csv', 'r') as file:
            raw_words = reader(file)
            words = []
            for item in raw_words:
                words.append(item[0].lower())
            word = choice(words)
        return word

    except FileNotFoundError as err:
        print(err)
        word = get_word('random')
        return word
