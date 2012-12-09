# -*- coding: utf-8 -*-

"""Module to check modules existance.

This exports this booleans:
  - has_reportlab -- True if reportlab is found
  - has_PIL -- True if PIL is found
  - has_pygtk -- True if pygtk is found

Copyright (C) 2005-2008  Xosé Otero <xoseotero@users.sourceforge.net>

"""

__all__ = ["has_reportlab", "has_PIL", "has_pygtk"]


try:
    import reportlab
    has_reportlab = True
except ImportError:
    has_reportlab = False

try:
    import PIL
    has_PIL = True
except:
    has_PIL = False

try:
    import pygtk
    pygtk.require('2.0')
    import gtk
    import pango
    has_pygtk = True
except:
    has_pygtk = False
