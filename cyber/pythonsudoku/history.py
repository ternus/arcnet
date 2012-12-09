# -*- coding: utf-8 -*-

"""Module for history management.

This exports the class:
  - History -- Board with history management.

Copyright (C) 2005-2008  Xosé Otero <xoseotero@users.sourceforge.net>

"""

__all__ = ["History"]


import copy

from board import Board


class History(Board):
    """Board with history management."""
    def __init__(self, cellsize=3, board=None, filename=None):
        """Form a board with history.

        If board is not None, the numbers are loaded from the board.
        If filename is not None, the numbers are loaded from a filename file.
        If board and filename are None a void board is created, with the size
        specified by cellsize.

        Keyword arguments:
        cellsize -- integer of the cell side lenght, default 3 for a 9x9
                    board (cellsize must be > 1)
                 -- or a tuple/list of 2 integers for a H*W grid on W*H grids
        board -- source board
        filename -- the file name (default None)

        """
        Board.__init__(self, cellsize, board, filename)
        self.forget()

    def remember(self):
        """Add the values of the sudoku to history at the end."""
        if  self.history_position < (len(self.history) - 1):
            self.history = self.history[:self.history_position + 1]

        self.history.append(copy.deepcopy(self.numbers))
        self.history_position += 1

    def forget(self):
        """Clear the history."""
        self.history = []
        self.history_position = -1

        self.remember()

    def is_first_position(self):
        """Return if the actual position is at the beginning of the history."""
        return self.history_position == 0

    def is_last_position(self):
        """Return if the actual position is at the end of the history."""
        return self.history_position == (len(self.history) - 1)

    def undo(self):
        """Go one position back."""
        if self.history_position <= 0:
            return False

        self.history_position -= 1
        self.numbers = copy.deepcopy(self.history[self.history_position])

        return True

    def redo(self):
        """Go one position forward."""
        if self.history_position >= (len(self.history) - 1):
            return False

        self.history_position += 1
        self.numbers = copy.deepcopy(self.history[self.history_position])

        return True
