"""DebugWindow subclasses the MainWindow class allowing for debugging."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSettings
from PySide6.QtGui import QAction
from icecream import ic

from ezside.app import MainWindow
from ezside.app.menus import DebugMenu

ic.configureOutput(includeContext=True, )


class DebugWindow(MainWindow):
  """DebugWindow subclasses the MainWindow class allowing for debugging."""

  __debug_flag__ = True
  debug1: QAction
  debug2: QAction
  debug3: QAction
  debug4: QAction
  debug5: QAction
  debug6: QAction
  debug7: QAction
  debug8: QAction
  debug9: QAction

  debug: DebugMenu

  def initSignalSlot(self) -> None:
    """Initialize the actions."""
    MainWindow.initSignalSlot(self)
    self.debug1.triggered.connect(self.debug1Func)
    self.debug2.triggered.connect(self.debug2Func)
    self.debug3.triggered.connect(self.debug3Func)
    self.debug4.triggered.connect(self.debug4Func)
    self.debug5.triggered.connect(self.debug5Func)
    self.debug6.triggered.connect(self.debug6Func)
    self.debug7.triggered.connect(self.debug7Func)
    self.debug8.triggered.connect(self.debug8Func)
    self.debug9.triggered.connect(self.debug9Func)

  def debug1Func(self, ) -> None:
    """Debug1 function."""
    self.liveView.addPoint()
    note = 'Debug1 function called, add data to chart view'
    self.statusBar().showMessage(note)
    if self.__paused_time__ is None:
      self.pulseClock.start()
    else:
      self.__resume_clock__.start(self.__paused_time__)

  def debug2Func(self, ) -> None:
    """Debug2 function."""
    note = 'Debug2 function called'
    print(note)
    self.__paused_time__ = self.pulseClock.remainingTime()
    self.pulseClock.stop()

  def debug3Func(self, ) -> None:
    """Debug3 function."""
    note = 'Debug3 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug4Func(self, ) -> None:
    """Debug4 function."""
    note = 'Debug4 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug5Func(self, ) -> None:
    """Debug5 function."""
    note = 'Debug5 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug6Func(self, ) -> None:
    """Debug6 function."""
    note = 'Debug6 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug7Func(self, ) -> None:
    """Debug7 function."""
    note = 'Debug7 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug8Func(self, ) -> None:
    """Debug8 function."""
    note = 'Debug8 function called'
    print(note)
    self.statusBar().showMessage(note)

  def debug9Func(self, ) -> None:
    """Debug9 function."""
    note = 'Debug9 function called'
    print(note)
    self.statusBar().showMessage(note)
