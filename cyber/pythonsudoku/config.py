# -*- coding: utf-8 -*-

"""Module with the configuration.

This exports:
  - localedir -- path to the locales
  - options -- options for the program


Copyright (C) 2005-2008  Xosé Otero <xoseotero@users.sourceforge.net>

"""

import sys
import os.path
import ConfigParser


__all__ = ["options"]


def _executable_path():
    """Return the path to the executable."""
    return os.path.dirname(os.path.realpath(os.path.abspath(sys.argv[0])))

def _exist(directory, filename):
    """Return if a filename is in a directory or in its subdirectories."""

    for root, dirs, files in os.walk(directory, topdown=False):
        if filename in files:
            return True
    return False

def _search_locales():
    """Search the locales directory.

    The localesc are searched in these locations:
    1. UNIX system directories.
    2. Installation path.

    If the locales are not found it returns the current directory.
    """

    localedirs = (os.path.join(_executable_path(), "locale/"),
                  "/usr/share/locale",
                  "/usr/share/games/locale",
                  "/usr/local/share/locale",
                  "/usr/local/share/games/locale")
    for dir in localedirs:
        if _exist(dir, "pythonsudoku.mo"):
            return dir

    # fall back to the current directory
    return "locale/"


class Options(ConfigParser.SafeConfigParser):
    def __init__(self):
        """Options for Python Sudoku."""

        ConfigParser.SafeConfigParser.__init__(self)
        self.load_defaults()
        self.load_user_cfg()

    def load_defaults(self):
        """Set the default values."""

        self.add_section("sudoku")
        self.set("sudoku", "difficulty", "normal")
        self.set("sudoku", "force", "False")
        self.set("sudoku", "handicap", "0")
        self.set("sudoku", "region_width", "3")
        self.set("sudoku", "region_height", "3")
        self.set("sudoku", "use_letters", "True")

        self.add_section("pdf")
        self.set("pdf", "page", "A4")
        self.set("pdf", "lines_colour", "black")
        self.set("pdf", "font", "Helvetica")
        self.set("pdf", "font_colour", "black")
        self.set("pdf", "font_size", "40")
        self.set("pdf", "title_font", "Helvetica")
        self.set("pdf", "title_colour", "black")
        self.set("pdf", "title_size", "72")
        self.set("pdf", "filename_font", "Helvetica")
        self.set("pdf", "filename_colour", "black")
        self.set("pdf", "filename_size", "24")

        self.add_section("print")
        # set the command to print a pdf
        # "" means command not know and so print is not possible
        # For UNIX:
        #self.set("print", "command", "lpr")
        # For MS Windows:
        #self.set("print", "command", "AcroRd32.exe /p /h") # Acrobat Reader
        #self.set("print", "command", "Acrobat.exe /p /h")  # Acrobat Writer
        self.set("print", "command", "")


        self.add_section("image")
        # set the format to always write the images in that format
        # "" means that the filename extension will be used as the format
        self.set("image", "format", "")
        self.set("image", "width", "300")
        self.set("image", "height", "300")
        self.set("image", "background", "white")
        self.set("image", "lines_colour", "black")
        self.set("image", "font", "/srv/arcnet/cyber/FreeSans.ttf")
        self.set("image", "font_colour", "black")
        self.set("image", "font_size", "24")

        self.add_section("gui")
        self.set("gui", "lines_colour", "black")
        self.set("gui", "font_colour", "black")

    def load_user_cfg(self):
        """Update the options with the content of the configuration files.

        The configuration files are searched in these locations:
        1. User's home directory (file .pysdk.cfg in UNIX and pysdk.cfg in the
           rest).
        2. Installation path (file pysdk.cfg).
        3. Current directory (file pysdk.cfg).
        """

        # path to the user configuration
        if os.name == "posix":
            usercfg = os.path.expanduser("~/.pysdk.cfg")
        else:
            usercfg = os.path.expanduser("~/pysdk.cfg")

        self.read((usercfg,
                   os.path.join(_executable_path(), "pysdk.cfg"),
                   "pysdk.cfg"))


# path to the locales
localedir = _search_locales()

# options for the program
options = Options()


# System dependent options
#options.set("print", "command", "COMMAND")
#options.set("image", "font", "PATH_TO_TTF_FONT")
#localedir = "DIRECTORY"
