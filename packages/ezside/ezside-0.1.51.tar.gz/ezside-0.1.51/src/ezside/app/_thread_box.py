"""ThreadBox provides a descriptor class for the AppThread class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Never
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication as QApp
from PySide6.QtWidgets import QMainWindow as QMain
from PySide6.QtCore import QObject, QThread
from attribox import AbstractDescriptor
from vistutils.parse import maybe
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

if TYPE_CHECKING:
  from ezside.app import App, AppThread

  Shiboken = type(QObject)  # QObject is a class from PySide
  QApp = App | AbstractDescriptor
  QMain = QMain | AbstractDescriptor
  QThread = QThread | AbstractDescriptor
  AppThread = AppThread | AbstractDescriptor


class ThreadBox(AbstractDescriptor):
  """ThreadBox provides a descriptor class for the AppThread class. """

  __loop_time__ = None
  __fallback_time__ = 250  # Default pause at end of loop
  __thread_class__ = None
  __fallback_thread__ = QThread

  __callback_functions__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the ThreadBox instance."""
    time_, cls = None, None
    for arg in args:
      if isinstance(arg, int) and time_ is None:
        time_ = arg
      elif isinstance(arg, type) and cls is None:
        if issubclass(arg, QThread):
          cls = arg
    self.setTime(maybe(time_, self.__fallback_time__))
    self.setThreadClass(maybe(cls, self.__fallback_thread__))

  def setTime(self, *args) -> None:
    """Set the loop time."""
    if isinstance(self, ThreadBox):
      self.__loop_time__ = args[0]
    elif isinstance(self, int):
      self.__loop_time__ = self
    else:
      e = """Unexpected arguments! %s"""
      argMsg = ', '.join(['%s' % arg for arg in [self, *args]])
      raise TypeError(e % argMsg)

  def getTime(self: ThreadBox = None) -> int:
    """Get the loop time."""
    if isinstance(self, ThreadBox):
      return self.__loop_time__
    return ThreadBox.__loop_time__ or ThreadBox.__fallback_time__

  def setThreadClass(self, cls: type, ) -> None:
    """Set the thread class."""
    if self.__thread_class__ is not None:
      e = """Thread class already set to %s"""
      raise AttributeError(monoSpace(e % self.__thread_class__))
    if isinstance(cls, type):
      if issubclass(cls, QThread):
        self.__thread_class__ = cls

  def getThreadClass(self, ) -> type:
    """Get the thread class."""
    if self.__thread_class__ is None:
      e = """Thread class not set! """
      raise AttributeError(monoSpace(e))
    if isinstance(self.__thread_class__, type):
      if issubclass(self.__thread_class__, QThread):
        return self.__thread_class__

  def _getPrivateName(self, ) -> str:
    """Get the private name."""
    return '_%s' % self.__field_name__

  def appendCallback(self, callMeMaybe: Callable) -> Callable:
    """Append the callback."""
    if not callable(callMeMaybe):
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)
    existing = self.__callback_functions__ or []

    def wrap() -> None:
      """Wraps the callback. Passes the running app to the callable."""
      app = QApp.instance()
      return callMeMaybe(app)

    self.__callback_functions__ = [*existing, wrap, ]
    return callMeMaybe

  def _getCallbacks(self, ) -> list[Callable]:
    """Get the callbacks."""
    return self.__callback_functions__ or []

  def _setCallbacks(self, *callMeMaybe: Callable) -> None:
    """Set the callbacks."""
    self.__callback_functions__ = [*callMeMaybe, ]

  def LOOP(self, callMeMaybe: Callable) -> Callable:
    """Alias for appendCallback. Use as decorator."""
    return self.appendCallback(callMeMaybe)

  def _createThread(self, instance: QApp) -> AppThread:
    """Create the thread."""
    cls = self.getThreadClass()
    thread = cls()
    thread.setTime(self.getTime())
    thread.setCallbacks(*self._getCallbacks())
    thread.callbackError.connect(instance.callbackError)
    instance.registerThread(thread)
    return thread

  def __instance_get__(self,
                       instance: App,
                       owner: Shiboken,
                       **kwargs) -> QThread:
    """Return the thread."""
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      setattr(instance, pvtName, self._createThread(instance))
    thread = getattr(instance, pvtName)
    if isinstance(thread, QThread):
      return thread
    e = typeMsg('thread', thread, QThread)
    raise TypeError(e)

  def __set__(self, *_) -> Never:
    """Raise an error if the window is set."""
    e = """Attribute '%s' is read-only! """
    raise AttributeError(monoSpace(e % self._getFieldName()))

  def __delete__(self, *_) -> Never:
    """Raise an error if the window is deleted."""
    e = """Attribute '%s' is read-only! """
    raise AttributeError(monoSpace(e % self._getFieldName()))
