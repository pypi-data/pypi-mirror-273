"""Flag provides a boolean descriptor class by subclassing the
AbstractDescriptor from the AttriBox package. This class has been improved
since AttriBox was developed. It now provides a general baseclass for
descriptor classes."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from attribox import AbstractDescriptor


class Flag(AbstractDescriptor):
  """Flag provides a boolean valued descriptor class"""

  __default_value__ = None

  def __init__(self, *args) -> None:
    if args:
      self.__default_value__ = True if args[0] else False
    else:
      self.__default_value__ = False

  def __instance_get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Implementation of getter function"""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      setattr(instance, pvtName, self.__default_value__)
      return self.__instance_get__(instance, owner, _recursion=True)
    return True if getattr(instance, pvtName) else False

  def __set__(self, instance: object, value: Any) -> None:
    """Implementation of setter function"""
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, True if value else False)

  def activate(self) -> None:
    """Activates the flag"""
    self.__default_value__ = True

  def deactivate(self, ) -> None:
    """Deactivates the flag"""
    self.__default_value__ = False
