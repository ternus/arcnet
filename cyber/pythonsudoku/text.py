# -*- coding: utf-8 -*-

"""Module for command line interface.

This exports the functions:
  - draw_board -- Draw the board and numbers.
  - create_sudoku -- Create a sudoku.
  - solve_sudoku -- Solve a sudoku.
  - test_difficulty -- Get the difficulty of a sudoku.

Copyright (C) 2005-2008  Xosé Otero <xoseotero@users.sourceforge.net>

Modification history:
2005/10/12  Antti Kuntsi
	Better output.

"""

__all__ = ["draw_board", "create_sudoku", "solve_sudoku"]


import sys
import math

from sudoku import Sudoku, difficulty
from board import Board, Value
from config import options


def back(times):
    while times > 0:
        print "\b\b",
        times -= 1

def draw_board(board):
    """Draw the board and numbers.

    Arguments:
    board -- the board

    """
    for j in xrange(board.boardsize):
        for i in xrange(board.boardsize):
            if board.numbers[j][i] != 0:
                if options.getboolean("sudoku", "use_letters"):
                    format = " %1s"
                    text = str(Value(board.numbers[j][i]))
                else:
                    lenght = int(math.log10(board.boardsize)) + 1
                    format = " %%%ds" % lenght
                    text = str(Value(board.numbers[j][i]).integer())
                print format % text,
            else:
                if options.getboolean("sudoku", "use_letters"):
                    text = " _"
                else:
                    lenght = int(math.log10(board.boardsize)) + 1
                    text = " " + "".join(["_" for x in xrange(lenght)])
                print text,
            if (i + 1) % board.cellsize[0] == 0:
                print " ",
        print
        if (j + 1) % board.cellsize[1] == 0 and j != (board.boardsize - 1):
            print

def create_sudoku(filename):
    """Create a sudoku with handicap and save it to filename.

    The handicap are the extra numbers given.

    Arguments:
    filename -- the file name

    """
    while True:
        print _(u"Creating sudoku..."),
        sys.stdout.flush()

        sudoku = Sudoku(Board((options.getint("sudoku", "region_width"),
                               options.getint("sudoku", "region_height"))),
                        difficulty=options.get("sudoku", "difficulty"))
        sudoku.create(options.getint("sudoku", "handicap"))

        if options.getboolean("sudoku", "force") and \
           (difficulty(sudoku.to_board()) != options.get("sudoku",
                                                       "difficulty")):
            print _(u"sudoku with wrong difficulty!")
        else:
            sudoku.to_board().save(filename)
            print _(u"success!")
            break

    draw_board(sudoku.to_board())

    return True

def solve_sudoku(filename, filename_out=None):
    """Open a sudoku located in filename and solve it.

    If filename_out is not None, the solved sudoku is saved.

    Arguments:
    filename -- the file name

    Keyword arguments:
    filename_out -- the output file name (default None)

    """
    board = Board(filename=filename)
    draw_board(board)

    print _(u"Solving sudoku..."),
    sys.stdout.flush()

    # Use all the algos
    sudoku = Sudoku(board, difficulty="hard")
    success = False
    if sudoku.solve():
        print _(u"success!")
        success = True
    else:
        print _(u"can't be solved!")

    draw_board(sudoku.to_board())

    if filename_out:
        sudoku.to_board().save(filename_out)

    return success

def test_difficulty(filename):
    """Open a sudoku located in filename and get its the difficulty.

    Arguments:
    filename -- the file name

    """
    print _(u"The difficulty of the sudoku is..."),
    sys.stdout.flush()

    d = difficulty(Board(filename=filename))
    if d:
        print d
    else:
        print "unknown"
