# -*- coding: utf-8 -*-

"""Module for Graphical User Interface.

This exports the class:
  - Gui -- the GUI

Copyright (C) 2005-2008  Xosé Otero <xoseotero@users.sourceforge.net>

"""

__all__ = ["Gui"]


import pygtk
pygtk.require('2.0')
import gtk
import pango

from check_modules import has_reportlab, has_PIL, has_pygtk
from board import Board, Value
from sudoku import Sudoku
from history import History
if has_reportlab:
    from pdf import PDF
    from printer import Printer
if has_PIL:
    from image import Image
from info import Info
from config import options


class Menu(gtk.MenuBar):
    def __init__(self, gui):
        gtk.MenuBar.__init__(self)

        self.__gui = gui

        self.__file_menu()
        self.__edit_menu()
        self.__sudoku_menu()
        self.__help_menu()

        self.show()

    def __file_menu(self):
        file_menu = gtk.Menu()

        open_item = gtk.MenuItem(_(u"_Open"))
        open_item.connect("activate", self.__gui.callback, "open")
        open_item.show()
        file_menu.append(open_item)

        save_sdk_item = gtk.MenuItem(_(u"_Save sudoku"))
        save_sdk_item.connect("activate", self.__gui.callback, "save")
        save_sdk_item.show()
        file_menu.append(save_sdk_item)

        if has_reportlab:
            save_pdf_item = gtk.MenuItem(_(u"Save as P_DF"))
            save_pdf_item.connect("activate", self.__gui.callback, "save_pdf")
            save_pdf_item.show()
            file_menu.append(save_pdf_item)

        if has_PIL:
            save_image_item = gtk.MenuItem(_(u"Save as _Image"))
            save_image_item.connect("activate", self.__gui.callback,
                                    "save_image")
            save_image_item.show()
            file_menu.append(save_image_item)

        if has_reportlab:
            print_item = gtk.MenuItem(_(u"_Print"))
            print_item.connect("activate", self.__gui.callback, "print")
            print_item.show()
            file_menu.append(print_item)

        quit_item = gtk.MenuItem(_(u"_Quit"))
        quit_item.show()
        quit_item.connect("activate", self.__gui.callback, "quit")
        file_menu.append(quit_item)

        file_item = gtk.MenuItem(_(u"_File"))
        file_item.set_submenu(file_menu)
        file_item.show()

        self.append(file_item)

    def __edit_menu(self):
        edit_menu = gtk.Menu()

        undo_item = gtk.MenuItem(_(u"_Undo"))
        undo_item.connect("activate", self.__gui.callback, "undo")
        undo_item.show()
        edit_menu.append(undo_item)

        redo_item = gtk.MenuItem(_(u"_Redo"))
        redo_item.connect("activate", self.__gui.callback, "redo")
        redo_item.show()
        edit_menu.append(redo_item)

        edit_item = gtk.MenuItem(_(u"_Edit"))
        edit_item.set_submenu(edit_menu)
        edit_item.show()

        self.append(edit_item)

    def __sudoku_menu(self):
        sudoku_menu = gtk.Menu()

        create_item = gtk.MenuItem(_(u"_Create"))
        create_item.connect("activate", self.__gui.callback, "create")
        create_item.show()
        sudoku_menu.append(create_item)

        check_item = gtk.MenuItem(_(u"C_heck"))
        check_item.connect("activate", self.__gui.callback, "check")
        check_item.show()
        sudoku_menu.append(check_item)

        solve_item = gtk.MenuItem(_(u"_Solve"))
        solve_item.connect("activate", self.__gui.callback, "solve")
        solve_item.show()
        sudoku_menu.append(solve_item)

        give_one_item = gtk.MenuItem(_(u"_Give one number"))
        give_one_item.connect("activate", self.__gui.callback, "give_one")
        give_one_item.show()
        sudoku_menu.append(give_one_item)

        sudoku_item = gtk.MenuItem(_(u"_Sudoku"))
        sudoku_item.set_submenu(sudoku_menu)
        sudoku_item.show()

        self.append(sudoku_item)

    def __help_menu(self):
        help_menu = gtk.Menu()

        about_item = gtk.MenuItem(_(u"_About"))
        about_item.connect("activate", self.__gui.callback, "about")
        about_item.show()
        help_menu.append(about_item)

        whatis_item = gtk.MenuItem(_(u"_What is"))
        whatis_item.connect("activate", self.__gui.callback, "whatis")
        whatis_item.show()
        help_menu.append(whatis_item)

        help_item = gtk.MenuItem(_(u"_Help"))
        help_item.set_submenu(help_menu)
        help_item.show()

        self.append(help_item)

class FileSelection(gtk.FileSelection):
    def __init__(self, text):
        gtk.FileSelection.__init__(self, text)

        self.ok_button.connect("clicked", self.callback_ok)
        self.cancel_button.connect("clicked", self.callback_cancel)

        self.show()

    def callback_ok(self, widget, data=None):
        self.destroy()

    def callback_cancel(self, widget, data=None):
        self.destroy()

class OpenWindow(FileSelection):
    def __init__(self, board):
        FileSelection.__init__(self, _(u"Open file"))

        self.__board = board

    def callback_ok(self, widget, data=None):
        self.__board.load(self.get_filename())
        self.destroy()

class SaveWindow(FileSelection):
    def __init__(self, board):
        FileSelection.__init__(self, _(u"Save file"))

        self.__board = board

    def callback_ok(self, widget, data=None):
        self.__board.save(self.get_filename())
        self.destroy()

class SavePDFWindow(FileSelection):
    def __init__(self, board):
        FileSelection.__init__(self, _(u"Save file as PDF"))

        self.__board = board

    def callback_ok(self, widget, data=None):
        PDF(self.__board, self.get_filename())
        self.destroy()

class SaveImageWindow(FileSelection):
    def __init__(self, board):
        FileSelection.__init__(self, _(u"Save file as an image"))

        self.__board = board

    def callback_ok(self, widget, data=None):
        Image(self.__board, self.get_filename())
        self.destroy()

class SelectValue(gtk.Window):
    def __init__(self, board, j, i):
        self.board = board
        self.j = j
        self.i = i

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_title(_(u"Select a number"))
        self.connect("delete_event", self.delete_event)
        self.show()

        solver = Sudoku(self.board, difficulty="easy")
        numbers = gtk.Table(self.board.cellsize[0], self.board.cellsize[1],
                            True)
        for j in xrange(self.board.cellsize[1]):
            for i in xrange(self.board.cellsize[0]):
                number = j * self.board.cellsize[0] + i + 1

                button = gtk.Button("_" + str(number))
                if number in solver.possible_values(self.j, self.i):
                    button.connect("clicked", self.callback, number)
                else:
                    button.set_sensitive(False)
                button.show()

                numbers.attach(button, i, i + 1, j, j + 1,
                               gtk.EXPAND | gtk.FILL,
                               gtk.EXPAND | gtk.FILL, 1, 1)
        numbers.show()

        button = gtk.Button(stock=gtk.STOCK_CANCEL)
        button.connect("clicked", self.callback)
        button.show()

        vbox = gtk.VBox(False, 0)
        vbox.pack_start(numbers, False, True, 0)
        vbox.pack_start(button, True, False, 0)
        vbox.show()

        self.add(vbox)

    def delete_event(self, widget, event, data=None):
        return False

    def callback(self, widget, data=None):
        if data:
            self.board[self.j, self.i] = data
        self.destroy()

class SudokuView(object):
    def __init__(self, board):
        self.board = board
        self.width = self.height = 30 * (self.board.boardsize + 1)
        self.square_width = 30
        self.square_height = 30

        fontname = "Arial 24"
        if self.board.boardsize > 9:
                fontname = "Arial 12"
                
        self.view = gtk.Alignment(0.5, 0.5)
        self.view.show()

        self.area = gtk.DrawingArea()
        self.area.set_size_request(self.width, self.height)
        self.area.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
        self.area.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.pangolayout = self.area.create_pango_layout("")
        self.pangolayout.set_font_description(pango.FontDescription(fontname))
        self.area.connect("expose-event", self.area_expose)
        self.area.connect("button-press-event", self.press)
        self.area.show()

        self.view.add(self.area)

    def draw_board(self):
        # margins
        x = self.square_width / 2                 # 5% left margin
        y = self.square_height / 2                # 5% top margin

        self.area.window.draw_rectangle(self.gc, False, x, y,
                                        self.width - 2 * x,
                                        self.height - 2 * y)

        # horizontal lines
        for i in xrange(self.square_height, self.height - self.square_height,
                        self.square_height):
            if i % (self.square_height * self.board.cellsize[1]) == 0:
                line_width = 2
            else:
                line_width = 1
            self.gc.set_line_attributes(line_width, self.gc.line_style,
                                        self.gc.cap_style,
                                        self.gc.join_style)
            self.area.window.draw_line(self.gc, x, y + i,
                                       x + self.width - self.square_width,
                                       y + i)

        # vertical lines
        for i in xrange(self.square_width, self.width - self.square_width,
                        self.square_width):
            if i % (self.square_width * self.board.cellsize[0]) == 0:
                line_width = 2
            else:
                line_width = 1
            self.gc.set_line_attributes(line_width, self.gc.line_style,
                                        self.gc.cap_style,
                                        self.gc.join_style)
            self.area.window.draw_line(self.gc, x + i, y,
                                       x + i,
                                       y + self.height - self.square_height)

    def draw_numbers(self):
        # margins
        x = self.square_width           # 5% margin + half square
        y = self.square_height          # 5% margin + half square

        for j in xrange(self.board.boardsize):
            for i in xrange(self.board.boardsize):
                if self.board[j, i]:
                    if options.getboolean("sudoku", "use_letters"):
                        text = str(Value(self.board[j, i]))
                    else:
                        text = str(Value(self.board[j, i]).integer())
                    self.pangolayout.set_text(text)
                    size = self.pangolayout.get_pixel_size()
                    self.area.window.draw_layout(self.gc,
                                                 x + i * self.square_width -
                                                 size[0] / 2,
                                                 y + j * self.square_height -
                                                 size[1] / 2,
                                                 self.pangolayout)


    def area_expose(self, area, event):
        self.gc = self.area.get_style().fg_gc[gtk.STATE_NORMAL]
        self.draw_board()
        self.draw_numbers()

    def press(self, widget, event):
        # margins
        x = self.square_width / 2                 # 5% left margin
        y = self.square_height / 2                # 5% top margin

        if event.x < x or event.x > (self.width - x) or \
           event.y < y or event.y > (self.height - y):
            return
        j = int((event.y - y) / self.square_height)
        i = int((event.x - x) / self.square_width)

        # outside board regions
        if i >= self.board.boardsize or j >= self.board.boardsize:
            return
        SelectValue(self.board, j, i)

    def widget(self):
        return self.view

class Progress(gtk.ProgressBar):
    def __init__(self, board):
        gtk.ProgressBar.__init__(self)
        self.__board = board

        done = float(self.__progress_done()) / self.__board.boardsize ** 2
        self.set_fraction(done)
        #self.pulse()
        self.set_text(str(int(done * 100)) + "%")
        self.show()

    def __progress_done(self):
        values = 0
        for j in xrange(self.__board.boardsize):
            for i in xrange(self.__board.boardsize):
                if self.__board[j, i]:
                    values += 1
        return values

class Handicap(gtk.Window):
    def __init__(self, gui, callback):
        self.gui = gui
        self.cb = callback

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_title(_(u"Create sudoku"))
        self.connect("delete_event", self.delete_event)
        self.show()

        label = gtk.Label(_(u"Select your handicap"))
        label.show()

        self.spin = gtk.SpinButton(gtk.Adjustment(options.getint("sudoku",
                                                                 "handicap"),
                                                  0, 30, 1, 5))
        self.spin.show()

        button = gtk.Button(stock=gtk.STOCK_OK)
        button.connect("clicked", self.callback, "hide")
        button.connect("clicked", self.callback)
        button.connect("clicked", self.callback, "destroy")
        button.show()

        vbox = gtk.VBox(False, 10)
        vbox.pack_start(label, False, True, 0)
        vbox.pack_start(self.spin, False, True, 0)
        vbox.pack_start(button, False, True, 0)
        vbox.show()

        self.add(vbox)

    def delete_event(self, widget, event, data=None):
        return False

    def callback(self, widget, command=None):
        if command == "destroy":
            self.destroy()
        elif command == "hide":
            self.hide()
        else:
            self.cb(widget, self.spin.get_value_as_int())

class Create(object):
    def __init__(self, gui):
        self.gui = gui
        Handicap(gui, self.callback)

    def callback(self, widget, handicap):
        message = gtk.MessageDialog(self.gui, gtk.DIALOG_MODAL,
                                    gtk.MESSAGE_INFO, gtk.BUTTONS_NONE,
                                    _(u"Creating sudoku..."))
        message.show()

        self.gui.create(handicap)

        message.destroy()

class MessageInfo(gtk.MessageDialog):
    def __init__(self, gui, text):
        gtk.MessageDialog.__init__(self, gui, gtk.DIALOG_MODAL,
                                         gtk.MESSAGE_INFO,
                                         gtk.BUTTONS_CLOSE,
                                         text)
        self.show()

        self.connect("response", self.callback)

    def callback(self, widget, id=None):
        self.destroy()

class MessageError(gtk.MessageDialog):
    def __init__(self, gui, text):
        gtk.MessageDialog.__init__(self, gui, gtk.DIALOG_MODAL,
                                         gtk.MESSAGE_ERROR,
                                         gtk.BUTTONS_CLOSE,
                                         text)
        self.show()

        self.connect("response", self.callback)

    def callback(self, widget, id=None):
        self.destroy()

class About(gtk.AboutDialog):
    def __init__(self):
        gtk.AboutDialog.__init__(self)
        self.set_name(Info["name"])
        self.set_version(Info["version"])
        self.set_copyright(Info["copyright"])
        self.set_license(Info["license"])
        self.set_website(Info["website"])
        self.set_authors(Info["authors"])
        self.show()

class Gui(History, gtk.Window):
    """The GUI."""
    def __init__(self, filename=None):
        """Create a new gui.

        Keyword arguments:
        filename -- the file name of the sudoku to open (default None)

        """
        History.__init__(self, (options.getint("sudoku", "region_width"),
                                options.getint("sudoku", "region_height")),
                         filename=filename)

        if not filename:
            self.create(options.getint("sudoku", "handicap"))

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_title(Info["name"])
        self.connect("delete_event", lambda w,e: gtk.main_quit())
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.callback, "quit")

        self.menu = Menu(self)

        self.sudoku = SudokuView(self).widget()

        self.undo_button = gtk.Button(stock=gtk.STOCK_UNDO)
        self.undo_button.connect("clicked", self.callback, "undo")
        self.undo_button.set_sensitive(False)
        self.undo_button.show()
        self.redo_button = gtk.Button(stock=gtk.STOCK_REDO)
        self.redo_button.connect("clicked", self.callback, "redo")
        self.redo_button.set_sensitive(False)
        self.redo_button.show()

        self.progress = Progress(self)

        self.hbox = gtk.HBox(False, 10)
        self.hbox.pack_start(self.undo_button, False, False, 10)
        self.hbox.pack_start(self.progress, False, False, 10)
        self.hbox.pack_end(self.redo_button, False, False, 10)
        self.hbox.show()

        self.view = gtk.VBox(False, 0)
        self.view.pack_start(self.menu, False, False, 3)
        self.view.pack_start(self.sudoku, False, False, 3)
        self.view.pack_end(self.hbox, False, False, 3)
        self.view.show()

        self.add(self.view)

        self.show()

        gtk.main()

    def __setitem__(self, (row, column), value):
        """Set the number to a position.

        Arguments:
        (row, column) -- a tuple/list/iterable with 2 values
        value -- the number

        """
        History.__setitem__(self, (row, column), value)
        self.update()

    def solve(self):
        """Solve the sudoku."""
        solver = Sudoku(self, difficulty="hard")
        retval = solver.solve()
        self.load_board(solver.to_board())

        return retval

    def create(self, handicap=0):
        """Create a new sudoku with handicap.

        The handicap are the extra numbers given.

        Keyword arguments:
        handicap -- the handicap (default 0)

        """
        creator = Sudoku(Board(cellsize=(options.getint("sudoku",
                                                        "region_width"),
                                         options.getint("sudoku",
                                                        "region_height"))),
                         difficulty=options.get("sudoku",
                                                "difficulty"))
        retval = creator.create(handicap)
        self.load_board(creator.to_board())
        self.forget()

        return retval

    def finished(self):
        """Return if the sudoku if finished."""
        for j in xrange(self.boardsize):
            for i in xrange(self.boardsize):
                if not self[j, i]:
                    return False

        return True

    def update(self, change_history=True):
        """Update the board.

        The actual values of the sudoku will be added to the history.
        Sometimes this is not wanted (sudoku created or loaded), to do this,
        call update(False).

        Keyword arguments:
        change_history -- if True the change will be added to history
                          (default True)

        """
        if change_history:
            self.remember()

        self.sudoku.destroy()
        self.progress.destroy()

        self.sudoku = SudokuView(self).widget()

        self.undo_button.set_sensitive(not self.is_first_position())
        self.redo_button.set_sensitive(not self.is_last_position())
        self.progress = Progress(self)

        self.view.pack_start(self.sudoku, False, False, 3)

        self.hbox.pack_start(self.progress, False, False, 10)

        if self.finished():
            MessageInfo(self, _(u"Solved!"))

    def callback(self, widget, function):
        """Gtk callback function.

        Arguments:
        widget -- the widget
        function -- string with the command to do ("open", "save", etc)

        """
        if function == "open":
            OpenWindow(self)
        elif function == "save":
            SaveWindow(self)
        elif function == "save_pdf":
            SavePDFWindow(self)
        elif function == "save_image":
            SaveImageWindow(self)
        elif function == "print":
            Printer(self.to_board())
        elif function == "quit":
            gtk.main_quit()
        elif function == "undo":
            if self.undo():
                self.update(False)
        elif function == "redo":
            if self.redo():
                self.update(False)
        elif function == "create":
            Create(self)
        elif function == "check":
            if self.solve():
                MessageInfo(self, _(u"This sudoku can be solved."))
            else:
                MessageInfo(self, _(u"This sudoku can't be solved."))
        elif function == "solve":
            if not self.solve():
                MessageError(gui, _(u"This sudoku can't be solved."))
            self.update()
        elif function == "give_one":
            # Use all the algols
            sdk1 = Sudoku(self, difficulty="hard")
            sdk1.solve()
            sdk2 = Sudoku(self, difficulty="easy")
            sdk2.give_numbers(sdk1.to_board(), 1)
            self.load_board(sdk2.to_board())
            self.update()
        elif function == "about":
            About()
        elif function == "whatis":
            MessageInfo(self, Info["whatis"])

    def delete_event(self, widget, event, data=None):
        return False
