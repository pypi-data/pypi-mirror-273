"""BaseWindow provides the base class for the main application window. It
implements menus and actions for the application, leaving widgets for the
LayoutWindow class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable

from PySide6.QtCore import Signal, QUrl, Slot
from PySide6.QtGui import QDesktopServices, QColor
from PySide6.QtWidgets import QMainWindow, QApplication
from icecream import ic

from ezside.app.menus import MainMenuBar, MainStatusBar
from ezside.dialogs import ColorSelection, \
  FontSelection, \
  OpenFile, \
  FolderSelection, SaveFile, UserInt

ic.configureOutput(includeContext=True, )


class BaseWindow(QMainWindow):
  """BaseWindow class provides menus and actions for the application."""

  mainMenuBar: MainMenuBar
  mainStatusBar: MainStatusBar
  colorSelected: Signal
  fontSelected: Signal
  openFileSelected: Signal
  saveFileSelected: Signal
  folderSelected: Signal

  intSelected: Signal

  colorDialog = ColorSelection()
  fontDialog = FontSelection()
  openFileDialog = OpenFile()
  saveFileDialog = SaveFile()
  folderDialog = FolderSelection()
  cunt = UserInt()

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
    ic('Initializing core connections')
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting File Menu Actions
    self.new = self.mainMenuBar.file.new
    self.open = self.mainMenuBar.file.open
    self.save = self.mainMenuBar.file.save
    self.saveAs = self.mainMenuBar.file.saveAs
    self.preferences = self.mainMenuBar.file.preferences
    self.exit = self.mainMenuBar.file.exit
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting Edit Menu Actions
    self.selectAll = self.mainMenuBar.edit.selectAll
    self.copy = self.mainMenuBar.edit.copy
    self.cut = self.mainMenuBar.edit.cut
    self.paste = self.mainMenuBar.edit.paste
    self.undo = self.mainMenuBar.edit.undo
    self.redo = self.mainMenuBar.edit.redo
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting Help Menu Actions
    self.aboutQt = self.mainMenuBar.help.aboutQt
    self.aboutConda = self.mainMenuBar.help.aboutConda
    self.aboutPython = self.mainMenuBar.help.aboutPython
    self.aboutPySide6 = self.mainMenuBar.help.aboutPySide6
    self.help = self.mainMenuBar.help.help
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting dialogs
    self.colorSelected.connect(lambda color: print(color))
    self.fontSelected.connect(lambda font: print(font))
    self.openFileSelected.connect(lambda file: print(file))
    self.saveFileSelected.connect(lambda file: print(file))
    self.folderSelected.connect(lambda folder: print(folder))
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting pulse signal
    self.pulse.connect(self.mainStatusBar.updateTime)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting general signals
    self.exit.triggered.connect(self.requestQuit)
    self.exit.triggered.connect(self.close)
    self.help.triggered.connect(self.requestHelp)
    self.aboutQt.triggered.connect(QApplication.aboutQt)
    condaLink = self.link('https://conda.io')
    pythonLink = self.link('https://python.org')
    pysideLink = self.link('https://doc.qt.io/qtforpython/')
    helpLink = self.link('https://www.youtube.com/watch?v=l60MnDJklnM')
    self.aboutConda.triggered.connect(condaLink)
    self.aboutPython.triggered.connect(pythonLink)
    self.aboutPySide6.triggered.connect(pysideLink)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #  Connecting debug signals

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
