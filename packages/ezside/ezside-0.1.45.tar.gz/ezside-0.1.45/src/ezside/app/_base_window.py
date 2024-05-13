"""BaseWindow provides the base class for the main application window. It
implements menus and actions for the application, leaving widgets for the
LayoutWindow class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable

from PySide6.QtCore import Signal, QUrl, Slot
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMainWindow, QApplication
from icecream import ic

from ezside.app.menus import MainMenuBar, MainStatusBar

ic.configureOutput(includeContext=True, )


class BaseWindow(QMainWindow):
  """BaseWindow class provides menus and actions for the application."""

  mainMenuBar: MainMenuBar
  mainStatusBar: MainStatusBar

  __allow_close__ = False
  __debug_flag__ = None
  __paused_time__ = None

  __is_initialized__ = None
  __is_closing__ = False

  requestQuit = Signal()
  confirmQuit = Signal()
  requestHelp = Signal()
  pulse = Signal()

  @staticmethod
  def link(url: Any) -> Callable:
    """Link to a URL."""
    if isinstance(url, str):
      url = QUrl(url)

    def go() -> bool:
      """Opens link in external browser."""
      return QDesktopServices.openUrl(url)

    return go

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the BaseWindow."""
    self.__debug_flag__ = kwargs.get('_debug', None)
    QMainWindow.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)

  def show(self) -> None:
    """Show the window."""
    if self.__is_initialized__ is None:  # Initialize the menu bar
      self.mainMenuBar = MainMenuBar(self)
      self.mainStatusBar = MainStatusBar(self)
      self.setMenuBar(self.mainMenuBar)
      self.setStatusBar(self.mainStatusBar)
      self.initUi()
      self._initCoreConnections()
      self.initSignalSlot()
      self.__is_initialized__ = True
    QMainWindow.show(self)

  def _initCoreConnections(self) -> None:
    """Initialize the core actions for the main window."""
    self.statusBar()
    self.statusBar().showMessage('Initiating core connections...')
    self.pulse.connect(self.mainStatusBar.updateTime)
    self.mainMenuBar.file.exit.triggered.connect(self.requestQuit)
    self.mainMenuBar.help.help.triggered.connect(self.requestHelp)
    self.mainMenuBar.help.aboutQt.triggered.connect(QApplication.aboutQt)
    condaLink = self.link('https://conda.io')
    pythonLink = self.link('https://python.org')
    pysideLink = self.link('https://doc.qt.io/qtforpython/')
    helpLink = self.link('https://www.youtube.com/watch?v=l60MnDJklnM')
    self.mainMenuBar.help.aboutConda.triggered.connect(condaLink)
    self.mainMenuBar.help.aboutPython.triggered.connect(pythonLink)
    self.mainMenuBar.help.aboutPySide6.triggered.connect(pysideLink)
    self.mainMenuBar.help.help.triggered.connect(helpLink)

  @Slot(str)
  def _announceHover(self, message) -> None:
    """Announce hover text."""
    self.statusBar().showMessage(message)

  @abstractmethod  # LayoutWindow
  def initUi(self, ) -> None:
    """Initializes the user interface for the main window."""

  @abstractmethod  # MainWindow
  def initSignalSlot(self, ) -> None:
    """Initializes the signal slot for the main window."""

  def showEvent(self, *args) -> None:
    """Show the window."""
    QMainWindow.showEvent(self, *args)
    self.statusBar().showMessage('Ready')

  def closeEvent(self, *args, **kwargs) -> None:
    """Close the window."""
    if self.__is_closing__:
      self.confirmQuit.emit()
      return QMainWindow.closeEvent(self, *args, **kwargs)
    self.__is_closing__ = True
    self.requestQuit.emit()
