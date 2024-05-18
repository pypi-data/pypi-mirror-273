"""EZTimer provides a descriptor class for QTimer."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, Any

from PySide6.QtCore import QTimer
from attribox import AbstractDescriptor, AttriBox
from vistutils.fields import EmptyField
from vistutils.parse import maybe
from vistutils.text import monoSpace, stringList
from vistutils.waitaminute import typeMsg

from ezside.core import Precise, TimerType


class EZTimer(AbstractDescriptor):
  """EZTimer provides a descriptor class for QTimer."""

  __is_initialised__ = None

  __single_shot__ = None
  __interval_time__ = None
  __timer_type__ = None
  __fallback_single__ = False
  __fallback_time__ = 1000
  __fallback_timer_type__ = Precise

  singleShot = EmptyField()
  timerType = EmptyField()
  intervalTime = AttriBox[int]()

  @singleShot.GET
  def _getSingleShot(self) -> bool:
    """Getter-function for single shot flag"""
    flag = maybe(self.__single_shot__, self.__fallback_single__)
    return True if flag else False

  @singleShot.SET
  def _setSingleShot(self, val: Any) -> None:
    """Setter-function for single shot flag"""
    self.__single_shot__ = True if val else False

  @singleShot.DEL
  def _delSingleShot(self) -> Never:
    """Deleter-function for single shot flag"""
    e = """Attribute 'singleShot' is read-only! """
    raise AttributeError(monoSpace(e))

  @timerType.GET
  def _getTimerType(self) -> TimerType:
    """Getter-function for timer type"""
    return maybe(self.__timer_type__, self.__fallback_timer_type__)

  @timerType.SET
  def _setTimerType(self, val: TimerType) -> None:
    """Setter-function for timer type"""
    if isinstance(val, TimerType):
      self.__timer_type__ = val
    elif isinstance(val, str):
      val = val.lower()
      for timerType in TimerType:
        name = timerType.name.lower()
        if name == val or name in val or val in name:
          self.__timer_type__ = timerType
          break
    else:
      e = typeMsg('timerType', val, TimerType)
      raise TypeError(monoSpace(e))

  @timerType.DEL
  def _delTimerType(self) -> Never:
    """Deleter-function for timer type"""
    e = """Attribute 'timerType' is read-only! """
    raise AttributeError(monoSpace(e))

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the EZTimer instance."""
    single, interval, timer = None, None, None
    singleKeys = stringList("""single, single_shot, singleShot""")
    intervalKeys = stringList("""interval, interval_time, intervalTime, 
      timeLimit, time, limit""")
    precisionKeys = stringList("""precision, timeType, timer_type""")
    KEYS = [singleKeys, intervalKeys, precisionKeys]
    types = dict(single=bool, interval=int, timer=TimerType)
    values = {}
    for ((name, type_), keys) in zip(types.items(), KEYS):
      for key in keys:
        if key in kwargs:
          val = kwargs[key]
          if isinstance(val, type_):
            values[name] = val
            break
          e = typeMsg(key, val, type_)
          raise TypeError(monoSpace(e))
      else:
        for arg in args:
          if isinstance(arg, type_):
            values[name] = arg
            break
    if 'single' in values:
      self.singleShot = values['single']
    if 'interval' in values:
      self.intervalTime = values['interval']
    if 'timer' in values:
      self.timerType = values['timer']
    self.__is_initialised__ = True

  def _createTimer(self, instance: object) -> None:
    """Creator-function for the QTimer instance."""
    timer = QTimer()
    timer.setSingleShot(self.singleShot)
    timer.setInterval(self.intervalTime)
    timer.setTimerType(self.timerType)
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
    if not isinstance(timer, QTimer):
      e = typeMsg('timer', timer, QTimer)
      raise TypeError(monoSpace(e))
    if timer.isActive():
      return timer
    if timer.isSingleShot() != self.singleShot:
      timer.setSingleShot(self.singleShot)
    if timer.interval() != self.intervalTime:
      timer.setInterval(self.intervalTime)
    if timer.timerType() != self.timerType:
      timer.setTimerType(self.timerType)
    return timer

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
