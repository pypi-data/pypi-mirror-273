"""MainWindow subclasses the LayoutWindow and provides the main
application business logic."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QAction
from icecream import ic

from ezside.app import LayoutWindow
from ezside.app.menus import EditMenu, FileMenu, HelpMenu

ic.configureOutput(includeContext=True, )


class MainWindow(LayoutWindow):
  """MainWindow subclasses the LayoutWindow and provides the main
  application business logic."""

  fileMenu: FileMenu
  editMenu: EditMenu
  helpMenu: HelpMenu

  new: QAction
  open: QAction
  save: QAction
  saveAs: QAction
  preferences: QAction
  exit: QAction
  aboutQt: QAction
  aboutPySide6: QAction
  aboutConda: QAction
  aboutPython: QAction
  help: QAction
  undo: QAction
  redo: QAction
  selectAll: QAction
  copy: QAction
  cut: QAction
  paste: QAction

  def initSignalSlot(self) -> None:
    """Initialize the actions."""
    LayoutWindow.initSignalSlot(self)
    self.pulse.connect(self.clock.refresh)
