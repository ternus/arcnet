# -*- coding: utf-8 -*-

"""Module for print support.

This exports:
  - Printer -- Print a board.

Copyright (C) 2005-2008  Xosé Otero <xoseotero@users.sourceforge.net>

"""

__all__ = ["Printer"]


import sys
import os
import tempfile

from pdf import PDF
from config import options


class Printer(object):
    """Print a board."""
    def __init__(self, board):
        """Print a board.

        Arguments:
        board -- the board

        """
        if not options.get("print", "command"):
            print >> sys.stderr, _(u"Print command not set")
            return

        dirname = tempfile.mkdtemp()
        filename = os.path.join(dirname, "sudoku.pdf")
        PDF(board, filename)

        # print it
        os.system("%s %s" % (options.get("print", "command"), filename))

        # remove it
        os.unlink(filename)
        os.rmdir(dirname)
