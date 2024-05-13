"""DebugMenu provides a debug menu for the main application window. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QAction

from ezside.app.menus import AbstractMenu


class DebugMenu(AbstractMenu):
  """DebugMenu provides a debug menu for the main application window. """

  debug1: QAction
  debug2: QAction
  debug3: QAction
  debug4: QAction
  debug5: QAction
  debug6: QAction
  debug7: QAction
  debug8: QAction
  debug9: QAction

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.debug1 = self.addAction(self.tr('Debug1'), 'debug1')
    self.debug2 = self.addAction(self.tr('Debug2'), 'debug2')
    self.debug3 = self.addAction(self.tr('Debug3'), 'debug3')
    self.debug4 = self.addAction(self.tr('Debug4'), 'debug4')
    self.debug5 = self.addAction(self.tr('Debug5'), 'debug5')
    self.debug6 = self.addAction(self.tr('Debug6'), 'debug6')
    self.debug7 = self.addAction(self.tr('Debug7'), 'debug7')
    self.debug8 = self.addAction(self.tr('Debug8'), 'debug8')
    self.debug9 = self.addAction(self.tr('Debug9'), 'debug9')
