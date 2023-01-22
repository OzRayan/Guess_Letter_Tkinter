#!/usr/bin/env python3

# Graphical elements to create a table style
from tkinter.ttk import Treeview, Style, Scrollbar

import variables as var


"""
Degree:         Faculty of Creative Arts, Technologies and Science
Department:     Computer Science and Technology
University:     University of Bedfordshire
Author:         Oszkar Feher
Date:           21 October 2022
"""


class Table:
    """Table class used to display a table with database rows."""
    def __init__(self, root, rem, data: list, fields: list, row: int, column: int):
        """
        Constructor.
        :param root: - the frame where it will be displayed the table.
        :param rem: - font size.
        :param data: - dataset.
        :param fields: - columns name.
        :param row: - row count.
        :param column: - column count.
        """
        col, height = tuple([i for i in range(len(fields))]), 20
        # Style for the treeview
        self.style = Style()
        # Modify the font of the body
        self.style.configure("Treeview", highlightthickness=3, bd=3, background=var.colours['bg'],
                             font=var.get_font_size(rem, 10))
        # Modify the font of the headings
        self.style.configure("Treeview.Heading", font=var.get_font_size(rem, 10))
        # Remove the borders
        self.style.layout("Treeview", [('Treeview.treearea', {'sticky': 'news'})])
        # Creating the Table
        self.table = Treeview(root, column=col,
                              height=height, show='headings', style='Treeview')
        self.table.grid(row=row, column=column, sticky="nws", padx=5, pady=5)
        # Creating scroll bar for the table
        self.scroll = Scrollbar(root, orient='vertical', command=self.table.yview)
        self.scroll.grid(row=row, column=column, sticky='nes', padx=5, pady=5)
        # Adding the scroll bar to the table
        self.table.configure(yscrollcommand=self.scroll.set)
        # First column/ID width
        for item in range(len(fields)):
            if item == 0:
                self.table.column(item, width=30)
            self.table.heading(item, text=fields[item], anchor='nw')
        # Populating the table with database rows
        for row_ in data:
            self.table.insert('', 'end', values=" ".join(str(i).strip("\'") for i in row_))
