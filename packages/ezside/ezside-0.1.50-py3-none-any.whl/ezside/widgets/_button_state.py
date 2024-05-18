"""ButtonStates instances enumerate different states of a button."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TYPE_CHECKING, Self

from attribox import AbstractDescriptor
from icecream import ic
from vistutils.waitaminute import typeMsg

from ezside.widgets import Label
from moreattribox import Flag

ic.configureOutput(includeContext=True)

if TYPE_CHECKING:
  pass


class ButtonState:
  """ButtonState describes the possible states of a button."""

  __iter_contents__ = None

  enabled = Flag(True)
  checked = Flag(False)
  hovered = Flag(False)
  pressed = Flag(False)
  moving = Flag(False)

  @classmethod
  def null(cls) -> Self:
    """Creates an instance with all flags deactivated."""
    return cls(enabled=False, checked=False, hovered=False, pressed=False,
               moving=False)

  @staticmethod
  def _parseStr(*args) -> dict[str, bool]:
    """Parses strings"""
    out = {}
    for arg in args:
      if isinstance(arg, str):
        if arg in ['enabled', 'checked', 'hovered', 'pressed', 'moving']:
          out[arg] = True
    return out

  @staticmethod
  def _parseButton(*args) -> dict[str, bool]:
    """Parse the button object into a dictionary."""
    if not args:
      return {}
    for arg in args:
      if isinstance(arg, Label):
        return dict(enabled=getattr(arg, '__is_enabled__', False),
                    checked=getattr(arg, '__is_checked__', False),
                    hovered=getattr(arg, '__is_hovered__', False),
                    pressed=getattr(arg, '__is_pressed__', False),
                    moving=getattr(arg, '__is_moving__', False)
                    )
    return {}

  @staticmethod
  def _parseKwargs(**kwargs) -> dict[str, bool]:
    """Parse the keyword arguments into a dictionary."""
    out = {}
    names = ['enabled', 'checked', 'hovered', 'pressed', 'moving']
    for name in names:
      if name in kwargs:
        out[name] = kwargs[name]
    return out

  def __init__(self, *args, **kwargs) -> None:
    data = {}
    parsedButton = self._parseButton(*args)
    parsedKwargs = self._parseKwargs(**kwargs)
    parsedStr = self._parseStr(*args)
    if parsedButton:
      data = parsedButton
    else:
      data = parsedKwargs
      if parsedStr:
        data |= parsedStr
    self.enabled = True if data.get('enabled', False) else False
    self.checked = True if data.get('checked', False) else False
    self.hovered = True if data.get('hovered', False) else False
    self.pressed = True if data.get('pressed', False) else False
    self.moving = True if data.get('moving', False) else False

  def __iter__(self) -> Self:
    """Iterates over the flags"""
    self.__iter_contents__ = [self.enabled, self.checked, self.hovered,
                              self.pressed, self.moving]
    return self

  def __next__(self, ) -> Self:
    """Returns the next flag"""
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __int__(self, ) -> int:
    """The integer representation includes prime factors with each flag
    represented by a prime number:
    - enabled: 2
    - checked: 3
    - hovered: 5
    - pressed: 7
    - moving: 11
    """
    out = 1
    for (prime, flag) in zip([2, 3, 5, 7, 11], self):
      out *= (prime if flag else 1)
    return out

  def __getitem__(self, key: str) -> bool:
    """Returns the value of the flag"""
    cls = self.__class__
    if getattr(cls, key, None) is None:
      raise KeyError(key)
    if not isinstance(getattr(cls, key), AbstractDescriptor):
      e = typeMsg(key, getattr(cls, key), AbstractDescriptor)
      raise TypeError
    return True if getattr(self, key) else False

  def __contains__(self, item: Any) -> bool:
    """Checks if the item is in the flags"""
    if isinstance(item, int):
      return False if item % int(self) else True
    if isinstance(item, str):
      return self[item]

  def __eq__(self, other: Any) -> bool:
    """Equality check"""
    if isinstance(other, Label):
      return self == ButtonState(other)
    if isinstance(other, ButtonState):
      return False if int(self) - int(other) else True
    if isinstance(other, int):
      return False if int(self) - other else True

  def __hash__(self, ) -> int:
    """Hash representation"""
    return int(self)

  @staticmethod
  def _getNames() -> list[str]:
    """Get the names of the flags"""
    return ['enabled', 'checked', 'hovered', 'pressed', 'moving']

  def __str__(self, ) -> str:
    """String representation"""
    out = []
    for (name, flag) in zip(self._getNames(), self):
      if flag:
        out.append(name)
    clsName = self.__class__.__name__
    return '%s(%s)' % (clsName, ', '.join(out))

  def __repr__(self, ) -> str:
    """Code representation"""
    return self.__str__()
