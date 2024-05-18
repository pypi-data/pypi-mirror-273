"""The 'ezside.app.menus' package provides the menus for the main
application window."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._abstract_menu import AbstractMenu
from ._file_menu import FileMenu
from ._edit_menu import EditMenu
from ._help_menu import HelpMenu
from ._debug_menu import DebugMenu

from ._main_menu_bar import MainMenuBar
from ._main_status_bar import MainStatusBar
