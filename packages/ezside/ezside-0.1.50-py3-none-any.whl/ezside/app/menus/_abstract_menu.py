"""Menu provides a simplified menu implementation"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar
from icecream import ic
from vistutils.text import monoSpace

if TYPE_CHECKING:
  pass
ic.configureOutput(includeContext=True, )


class AbstractMenu(QMenu):
  """A class for managing menus in the application."""

  __iter_contents__ = None
  __added_actions__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the menu."""
    parent, title = None, None
    for arg in args:
      if isinstance(arg, QMenuBar) and parent is None:
        parent = arg
      elif isinstance(arg, str) and title is None:
        title = arg
      if parent is not None and title is not None:
        break
    else:
      e = """AbstractMenu requires a parent QMenuBar and a title str as 
      arguments to the constructor, but found only parent: '%s' and title: 
      '%s'! """ % (parent, title)
      raise ValueError(monoSpace(e))
    QMenu.__init__(self, title)
    self.initStyle()
    self.initUi()
    self.initSignalSlot()

  def initStyle(self, ) -> None:
    """Initialize the style of the menu. Subclasses may implement this
    method to customize the style of the menu. """

  @abstractmethod
  def initUi(self, ) -> None:
    """Initialize the UI of the menu. Subclasses are required to implement
    this method. The method is expected to instantiate the actions. """

  def initSignalSlot(self, ) -> None:
    """Initialize the signal-slot connections. Subclasses may implement this
    method, but generally the menu class is not responsible for handling
    actions just for presenting them. """

  def _getActionList(self) -> list[QAction]:
    """Get the list of actions."""
    if self.__added_actions__ is None:
      self.__added_actions__ = []
    return self.__added_actions__

  def addAction(self, *args) -> QAction:
    """Add an action to the menu."""
    strArgs = [arg for arg in args if isinstance(arg, str)]
    title, name = [*strArgs, None, None][:2]
    app = QCoreApplication.instance()
    settings = getattr(app, 'getSettings', )()
    icon = settings.value('icon/%s' % name, None)
    shortcut = settings.value('shortcut/%s' % name, None)
    action = QMenu.addAction(self, icon, title, shortcut)
    self._getActionList().append(action)
    main = getattr(app, 'mainWindow', )
    setattr(main, name, action)
    return action

  def __iter__(self) -> AbstractMenu:
    """Iterate over the contents of the menu bar."""
    self.__iter_contents__ = [*self._getActionList(), ]
    return self

  def __next__(self, ) -> QAction:
    """Implementation of iteration protocol"""
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __len__(self) -> int:
    """Return the number of menus in the menu bar."""
    return len(self._getActionList())

  def __contains__(self, other: QAction) -> bool:
    """Check if a menu is in the menu bar."""
    for action in self:
      if action is other:
        return True
    else:
      return False
