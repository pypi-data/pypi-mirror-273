"""EZTimer provides a descriptor class for QTimer."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from PySide6.QtCore import QTimer
from attribox import AbstractDescriptor
from vistutils.parse import maybe
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import Precise


class EZTimer(AbstractDescriptor):
  """EZTimer provides a descriptor class for QTimer."""

  __single_shot__ = None
  __interval_time__ = None
  __timer_type__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the EZTimer instance."""
    single, interval, timer = None, None, None
    for arg in args:
      if isinstance(arg, bool) and self.__single_shot__ is None:
        self.__single_shot__ = arg
      elif isinstance(arg, int) and self.__interval_time__ is None:
        self.__interval_time__ = arg
      elif isinstance(arg, int) and self.__timer_type__ is None:
        self.__timer_type__ = arg

  def _createTimer(self, instance: object) -> None:
    """Creator-function for the QTimer instance."""
    timer = QTimer()
    timer.setSingleShot(maybe(self.__single_shot__, False))
    timer.setInterval(maybe(self.__interval_time__, 1000))
    timer.setTimerType(maybe(self.__timer_type__, Precise))
    setattr(instance, self._getPrivateName(), timer)

  def __instance_get__(self,
                       instance: object,
                       owner: type,
                       **kwargs) -> QTimer:
    """The __instance_get__ method is called when the descriptor is accessed
    via the owning instance. """
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createTimer(instance)
      return self.__instance_get__(instance, owner, _recursion=True)
    timer = getattr(instance, pvtName)
    if isinstance(timer, QTimer):
      return timer
    e = typeMsg('timer', timer, QTimer)
    raise TypeError(monoSpace(e))

  def _getPrivateName(self, ) -> str:
    """Get the private name."""
    return '_%s' % self.__field_name__

  def __set__(self, *_) -> Never:
    """Raise an error if the window is set."""
    e = """Attribute '%s' is read-only! """
    raise AttributeError(monoSpace(e % self._getFieldName()))

  def __delete__(self, *_) -> Never:
    """Raise an error if the window is deleted."""
    e = """Attribute '%s' is read-only! """
    raise AttributeError(monoSpace(e % self._getFieldName()))
