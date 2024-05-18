"""HelpMenu provides a help menu for the main application window. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QAction

from ezside.app.menus import AbstractMenu


class HelpMenu(AbstractMenu):
  """HelpMenu provides a help menu for the main application window. """

  aboutQt: QAction
  aboutPySide6: QAction
  aboutConda: QAction
  aboutPython: QAction
  help: QAction

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.aboutQt = self.addAction(self.tr('About Qt'), 'aboutQt')
    self.aboutPySide6 = self.addAction(self.tr('About PySide6'),
                                       'aboutPySide6')
    self.aboutConda = self.addAction(self.tr('About Conda'), 'aboutConda')
    self.aboutPython = self.addAction(self.tr('About Python'),
                                      'aboutPython')
    self.help = self.addAction(self.tr('Help'), 'help')
