"""WindowBox provides a descriptor class for the main application window."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Never

from PySide6.QtWidgets import QMainWindow as QMain
from attribox import AbstractDescriptor
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

if TYPE_CHECKING:
  from PySide6.QtCore import QObject
  from ezside.app import App

  Shiboken = type(QObject)  # QObject is a class from PySide
  QApp = App | AbstractDescriptor
  QMain = QMain | AbstractDescriptor


class WindowBox(AbstractDescriptor):
  """WindowBox provides a descriptor class for the main application
  window."""

  def _getPrivateName(self, ) -> str:
    """Return the private name of the window field."""
    return '_%s' % self._getFieldName()

  def _createWindow(self, app: App) -> None:
    """Create the main application window."""
    pvtName = self._getPrivateName()
    cls = app.getWindowClass()
    window = cls()
    setattr(app, pvtName, window)

  def __instance_get__(self, app: App, owner: Shiboken, **kwargs) -> QMain:
    """Return the main application window."""
    pvtName = self._getPrivateName()
    if getattr(app, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createWindow(app)
      return self.__instance_get__(app, owner, _recursion=True)
    window = getattr(app, pvtName)
    if isinstance(window, QMain):
      return window
    e = typeMsg('window', window, QMain)
    raise TypeError(monoSpace(e))

  def __set__(self, *_) -> Never:
    """Raise an error if the window is set."""
    e = """Attribute '%s' is read-only! """
    raise AttributeError(monoSpace(e % self._getFieldName()))

  def __delete__(self, *_) -> Never:
    """Raise an error if the window is deleted."""
    e = """Attribute '%s' is read-only! """
    raise AttributeError(monoSpace(e % self._getFieldName()))
