"""MainStatusBar provides a status bar for the main application window."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QStatusBar
from icecream import ic

from ezside.widgets import DigitalClock

ic.configureOutput(includeContext=True)


class MainStatusBar(QStatusBar):
  """StatusBar provides a status bar for the main application window."""

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the MainStatusBar."""
    QStatusBar.__init__(self, *args, **kwargs)
    self.digitalClock = DigitalClock(id='statusBarClock')
    self.digitalClock.initUi()
    self.addPermanentWidget(self.digitalClock, )
    self.initUi()

  def initUi(self, ) -> None:
    """Initializes the user interface for the status bar."""
    self.setStyleSheet("""background-color: #e0e0e0; color: #000000;
    border-top: 1px solid #000000; border-left: 1px solid #000000;
    border-right: 1px solid #000000; border-bottom: 1px solid #000000;""")

  def initSignalSlot(self, ) -> None:
    """Initialize the signal and slot connections."""

  @Slot()
  def updateTime(self, ) -> None:
    """Update the time."""
    self.digitalClock.refresh()
