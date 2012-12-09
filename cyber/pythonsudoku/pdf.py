# -*- coding: utf-8 -*-

"""Module for PDF output.

This exports the class:
  - PDF -- Save a board as PDF.

This exports the function:
  - show_fonts -- Print the available fonts to console.

Copyright (C) 2005-2008  Xosé Otero <xoseotero@users.sourceforge.net>

"""

__all__ = ["PDF"]


import reportlab.pdfbase.pdfmetrics
import reportlab.pdfgen.canvas
import reportlab.lib.pagesizes

from board import Value
from config import options


class PDF(object):
    """Save a board as PDF."""
    def __init__(self, board, filename):
        """Save a board as PDF.

        Arguments:
        board -- the board
        filename -- the filename

        """
        self.page_size = getattr(reportlab.lib.pagesizes,
                                 options.get("pdf", "page"))
        self.c = reportlab.pdfgen.canvas.Canvas(filename)

        self.draw_title()

        if isinstance(board, list) or isinstance(board, tuple):
            self.c.scale(0.5, 0.5)

            # third
            self.numbers = board[2].numbers
            self.filename = board[2].filename
            self.cellsize = board[2].cellsize
            self.boardsize = board[2].boardsize

            self.c.translate(0, 0)
            self.draw_filename()
            self.draw_board()
            self.draw_numbers()

            # fourth
            self.numbers = board[3].numbers
            self.filename = board[3].filename
            self.cellsize = board[3].cellsize
            self.boardsize = board[3].boardsize

            self.c.translate(self.page_size[0], 0)
            self.draw_filename()
            self.draw_board()
            self.draw_numbers()

            # first
            self.numbers = board[0].numbers
            self.filename = board[0].filename
            self.cellsize = board[0].cellsize
            self.boardsize = board[0].boardsize

            self.c.translate(- self.page_size[0], self.page_size[1] / 1.3)
            self.draw_filename()
            self.draw_board()
            self.draw_numbers()

            # second
            self.numbers = board[1].numbers
            self.filename = board[1].filename
            self.cellsize = board[1].cellsize
            self.boardsize = board[1].boardsize

            self.c.translate(self.page_size[0], 0)
            self.draw_filename()
            self.draw_board()
            self.draw_numbers()

        else:
            self.numbers = board.numbers
            self.filename = board.filename
            self.cellsize = board.cellsize
            self.boardsize = board.boardsize

            self.draw_filename()
            self.draw_board()
            self.draw_numbers()

        self.c.showPage()
        self.c.save()

    def draw_title(self):
        """Draw the title "sudou"."""
        if options.getint("pdf", "title_size") > 0:
            self.c.setFillColor(options.get("pdf", "title_colour"))
            self.c.setFont(options.get("pdf", "title_font"),
                           options.getint("pdf", "title_size"))
            face = reportlab.pdfbase.pdfmetrics.getFont("Helvetica").face
            height = (face.ascent - face.descent) * \
                     options.getint("pdf", "title_size") / 1000.0
            self.c.drawCentredString(self.page_size[0] / 2,
                                     (3 * self.page_size[1] + \
                                      0.9 * self.page_size[0]) / 4 - \
                                     options.getint("pdf", "title_size") / 2 + \
                                     height / 2,
                                     "sudoku")

    def draw_filename(self):
        """Draw the filename."""
        if options.getint("pdf", "filename_size") > 0 and self.filename:
            self.c.setFillColor(options.get("pdf", "filename_colour"))
            self.c.setFont(options.get("pdf", "filename_font"),
                           options.getint("pdf", "filename_size"))
            face = reportlab.pdfbase.pdfmetrics.getFont("Helvetica").face
            height = (face.ascent - face.descent) * \
                     options.getint("pdf", "filename_size") / 1000.0
            self.c.drawCentredString(self.page_size[0] / 2,
                                     (self.page_size[1] - \
                                      self.page_size[0] * 0.9) / 2 + \
                                     self.page_size[0] * 0.9 + \
                                     height / 2,
                                     "(" + str(self.filename) + ")")

    def draw_board(self):
        """Draw the board.

        Only the board, to draw numbers draw_numbers it is used.

        """
        self.c.setStrokeColor(options.get("pdf", "lines_colour"))

        if self.page_size[0] < self.page_size[1]:
            x = self.page_size[0] / 20
            y = (self.page_size[1] - self.page_size[0] * 0.9) / 2
            square_length = self.page_size[0] / (self.boardsize) * 0.9
        else:
            y = self.page_size[1] / 20
            x = (self.page_size[0] - self.page_size[1] * 0.9) / 2
            square_length = self.page_size[1] / (self.boardsize) * 0.9

        self.c.rect(x, y,
                    self.page_size[0] * 0.9, self.page_size[0] * 0.9, fill=0)

        # vertical lines
        for i in xrange(self.boardsize):
            if i > 0 and i % self.cellsize[0] == 0:
                self.c.setLineWidth(2)
            else:
                self.c.setLineWidth(1)
            self.c.line(x + i * square_length, y,
                        x + i * square_length,
                        y + square_length * self.boardsize)

        # horizontal lines
        for i in xrange(self.boardsize):
            if i > 0 and i % self.cellsize[1] == 0:
                self.c.setLineWidth(2)
            else:
                self.c.setLineWidth(1)
            self.c.line(x, y + i * square_length,
                        x + square_length * self.boardsize,
                        y + i * square_length)

    def draw_numbers(self):
        """Draw the numbers."""
        self.c.setFillColor(options.get("pdf", "font_colour"))
        self.c.setFont(options.get("pdf", "font"),
                       options.getint("pdf", "font_size"))

        face = reportlab.pdfbase.pdfmetrics.getFont("Helvetica").face
        height = (face.ascent - face.descent) * \
                 options.getint("pdf", "font_size") / 1000.0
        if self.page_size[0] < self.page_size[1]:
            square_length = self.page_size[0] / (self.boardsize) * 0.9
            x = self.page_size[0] / 20 + square_length / 2
            y = (self.page_size[1] - self.page_size[0] * 0.9 + \
                 square_length - height) / 2
        else:
            square_length = self.page_size[1] / (self.boardsize) * 0.9
            y = self.page_size[1] / 20 + square_length / 2
            x = (self.page_size[0] - self.page_size[1] * 0.9 + \
                 square_length - height) / 2

        for i in xrange(self.boardsize):
            for j in xrange(self.boardsize):
                if self.numbers[self.boardsize - 1 - j][i] != 0:
                    if options.getboolean("sudoku", "use_letters"):
                        text = str(Value(self.numbers[self.boardsize - 1 - j][i]))
                    else:
                        text = str(Value(self.numbers[self.boardsize - 1 - j][i]).integer())
                    self.c.drawCentredString(x + i * square_length,
                                             y + j * square_length,
                                             text)

def show_fonts():
    """Print the available fonts to console."""
    for font in reportlab.pdfgen.canvas.Canvas("").getAvailableFonts():
        print font
