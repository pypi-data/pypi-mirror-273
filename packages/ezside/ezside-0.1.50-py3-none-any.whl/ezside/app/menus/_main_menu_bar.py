"""MainMenuBar subclasses QMenuBar and brings common menus with common
actions. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu
from icecream import ic

from ezside.app.menus import FileMenu, EditMenu, HelpMenu, \
  DebugMenu, AbstractMenu

if TYPE_CHECKING:
  pass
ic.configureOutput(includeContext=True, )


class MainMenuBar(QMenuBar):
  """MainMenuBar subclasses QMenuBar and brings common menus with common
  actions. """

  __iter_contents__ = None
  __added_menus__ = None

  file: FileMenu
  fileAction: QAction
  edit: EditMenu
  editAction: QAction
  help: HelpMenu
  helpAction: QAction
  debug: DebugMenu
  debugAction: QAction

  hoverText = Signal(str)

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the MainMenuBar."""
    QMenuBar.__init__(self, *args, **kwargs)
    self.initUi()
    self.initDebug()
    self.initSignalSlot()

  def initUi(self, ) -> None:
    """Initializes the user interface for the widget. Required for subclasses
    to implement. """
    self.file = FileMenu(self, 'File')
    self.fileAction = self.addMenu(self.file)
    self.edit = EditMenu(self, 'Edit')
    self.editAction = self.addMenu(self.edit)
    self.help = HelpMenu(self, 'Help')
    self.helpAction = self.addMenu(self.help)

  def initDebug(self) -> None:
    """Initializes the debug menu. Optional for subclasses to implement."""
    self.debug = DebugMenu(self, 'Debug')
    self.addMenu(self.debug)

  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the widget. Optional for
    subclasses to implement."""

  def _getMenuList(self) -> list[AbstractMenu]:
    """Return a list of menus."""
    if self.__added_menus__ is None:
      self.__added_menus__ = []
    return self.__added_menus__

  def addMenu(self, *args) -> QAction:
    """Add a menu to the menu bar. """
    for arg in args:
      if isinstance(arg, AbstractMenu):
        self._getMenuList().append(arg)
        return QMenuBar.addMenu(self, arg)
    else:
      return QMenuBar.addMenu(self, *args)

  def hoverFactory(self, menu: AbstractMenu) -> Callable:
    """Factory for hover handling"""

    def hoverMenu(text: str) -> None:
      """Handle hover action."""
      clsName = menu.__class__.__name__
      self.hoverText.emit('%s/%s' % (clsName, text))

    return hoverMenu

  def __iter__(self) -> MainMenuBar:
    """Iterate over the contents of the menu bar."""
    self.__iter_contents__ = self._getMenuList()
    return self

  def __next__(self, ) -> AbstractMenu:
    """Implementation of iteration protocol"""
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __len__(self) -> int:
    """Return the number of menus in the menu bar."""
    return len(self._getMenuList())

  def __contains__(self, other: QMenu) -> bool:
    """Check if a menu is in the menu bar."""
    for menu in self:
      if menu is other:
        return True
    else:
      return False
