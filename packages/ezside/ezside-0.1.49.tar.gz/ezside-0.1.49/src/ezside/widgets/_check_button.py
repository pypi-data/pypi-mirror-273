"""CheckButton provides check button supporting on and off states. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QColor

from ezside.core import parseBrush, SolidFill
from ezside.widgets import PushButton


class CheckButton(PushButton):
  """CheckButton provides check button supporting on and off states. """

  __is_checked__ = None

  def check(self) -> None:
    """Changes the state to checked"""
    if self.__is_checked__ or not self.__is_enabled__:
      return
    self.__is_checked__ = True

  def uncheck(self) -> None:
    """Changes the state to unchecked"""
    if not self.__is_checked__ or not self.__is_enabled__:
      return
    self.__is_checked__ = False

  def initSignalSlot(self, ) -> None:
    """Initialize the signal slot."""
    PushButton.initSignalSlot(self)
    self.pressHoldLeft.connect(self.check)
    self.pressHoldLeft.connect(self.update)
    self.pressHoldRight.connect(self.uncheck)
    self.pressHoldRight.connect(self.update)

  def getDefaultStyles(self, ) -> dict[str, Any]:
    """Get the default styles."""
    base = PushButton.getDefaultStyles(self)
    if self.__is_checked__:
      bgColor = QColor(144, 255, 63, 255)
    else:
      bgColor = QColor(255, 144, 63, 255)
    borderColor = QColor(0, 0, 0, 255)
    f = 100
    f = 125 if self.__is_hovered__ else f
    f = 150 if self.__is_pressed__ else f
    bgBrush = parseBrush(bgColor.darker(f), SolidFill)
    borderBrush = parseBrush(borderColor.darker(f), SolidFill)
    base['backgroundBrush'] = bgBrush
    base['borderBrush'] = borderBrush
    return base
