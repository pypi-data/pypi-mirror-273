"""FileMenu provides the file menu for the main application window. It
subclasses the AbstractMenu class. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QAction
from icecream import ic

from ezside.app.menus import AbstractMenu

ic.configureOutput(includeContext=True, )


class FileMenu(AbstractMenu):
  """FileMenu provides the file menu for the main application window. It
  subclasses the AbstractMenu class. """

  new: QAction
  open: QAction
  save: QAction
  saveAs: QAction
  preferences: QAction
  exit: QAction

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.new = self.addAction(self.tr('New'), 'new')
    self.open = self.addAction(self.tr('Open'), 'open')
    self.addSeparator()
    self.save = self.addAction(self.tr('Save'), 'save')
    self.saveAs = self.addAction(self.tr('Save As'), 'saveAs')
    self.addSeparator()
    self.preferences = self.addAction(self.tr('Preferences'), 'preferences')
    self.addSeparator()
    self.exit = self.addAction(self.tr('Exit'), 'exit')
