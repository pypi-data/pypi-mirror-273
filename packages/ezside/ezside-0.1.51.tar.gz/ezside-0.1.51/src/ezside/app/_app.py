"""App subclasses the QApplication class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, Signal, Slot, QRect
from PySide6.QtWidgets import QApplication, QMainWindow
from icecream import ic
from vistutils.text import monoSpace

from ezside.app import AppSettings, WindowBox, ThreadBox
from ezside.app import AppThread

ic.configureOutput(includeContext=True, )

MenuFlag = Qt.ApplicationAttribute.AA_DontUseNativeMenuBar

if TYPE_CHECKING:
  pass


class App(QApplication):
  """App is a subclass of QApplication."""

  __window_class__ = None
  __registered_threads__ = None

  mainWindow = WindowBox()
  pulseThread = ThreadBox(AppThread, 250)

  stopThreads = Signal()
  threadsExited = Signal()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the App instance."""
    strArgs = [arg for arg in args if isinstance(arg, str)]
    QApplication.__init__(self, strArgs)
    self.setStyle('Fusion')
    for arg in args:
      if isinstance(arg, type):
        if issubclass(arg, QMainWindow):
          self._setWindowClass(arg)
          ic(arg.__name__)
          break
    else:
      self._setWindowClass(QMainWindow)
    self.setApplicationName('EZSide')
    self.setOrganizationName('EZ')
    self.setAttribute(MenuFlag, True)

  @Slot()
  def callbackError(self, error: Exception) -> None:
    """Callback error."""
    ic(error)

  def _setWindowClass(self, windowClass: type) -> None:
    """Set the window class."""
    if self.__window_class__ is not None:
      e = """Window class already set to %s"""
      raise AttributeError(monoSpace(e % self.__window_class__))
    if isinstance(windowClass, type):
      if issubclass(windowClass, QMainWindow):
        self.__window_class__ = windowClass

  def getWindowClass(self, ) -> type:
    """Getter-function for the window class. """
    if self.__window_class__ is None:
      e = """Window class not set! """
      raise AttributeError(monoSpace(e))
    if isinstance(self.__window_class__, type):
      if issubclass(self.__window_class__, QMainWindow):
        return self.__window_class__

  @staticmethod
  def getSettings() -> AppSettings:
    """Get the application settings."""
    return AppSettings()

  @Slot()
  def initiateQuit(self) -> None:
    """Initialize the quit signal."""
    winGeometry = self.mainWindow.geometry()
    self.getSettings().setValue('/window/geometry', winGeometry)
    if not self.maybeQuit():
      self.stopThreads.emit()

  @Slot()
  def maybeQuit(self, ) -> bool:
    """Checks if any running threads are still running"""
    for thread in self._getRunningThreads():
      if thread.isRunning():
        return False
    else:
      self.threadsExited.emit()
      return True

  def _getRegisteredThreads(self, ) -> list:
    """Get the registered threads."""
    if self.__registered_threads__ is None:
      self.__registered_threads__ = []
    return self.__registered_threads__

  def registerThread(self, thread: AppThread) -> None:
    """Register a thread."""
    self._getRegisteredThreads().append(thread)
    thread.finished.connect(self.maybeQuit)
    self.stopThreads.connect(thread.requestQuit)

  def _getRunningThreads(self, ) -> list[AppThread]:
    """Get the running threads."""
    registeredThreads = self._getRegisteredThreads()
    return [thread for thread in registeredThreads if thread.isRunning()]

  @pulseThread.LOOP
  def pulse(self) -> None:
    """Pulse the application."""
    self.mainWindow.pulse.emit()

  def exec(self) -> int:
    """Executes the application."""
    winGeometry = self.getSettings().value('/window/geometry')
    if isinstance(winGeometry, QRect):
      winGeometry = QRect(winGeometry)
      self.mainWindow.setGeometry(winGeometry)
    else:
      ic(winGeometry)
    self.mainWindow.show()
    self.mainWindow.requestQuit.connect(self.initiateQuit)
    self.mainWindow.setWindowIcon(self.getSettings().value('icon/pogchamp'))
    self.pulseThread.start()
    retCode = super().exec()
    if not retCode:
      AppSettings().setValue('/window/geometry', self.mainWindow.geometry())
    return retCode
