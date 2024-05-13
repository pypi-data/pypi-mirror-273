"""GraffitiVandal provides a subclass of QPainter that allows for
sequential painting functions to react to the same QPaintEvent."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRect, QPoint
from PySide6.QtGui import QPainter


class GraffitiVandal(QPainter):
  """GraffitiVandal provides a subclass of QPainter that allows for
  sequential painting functions to react to the same QPaintEvent."""

  __inner_rect__ = None

  def begin(self, *args) -> None:
    """Begins the painting"""
    QPainter.begin(self, *args)
    QPainter.setRenderHint(self, QPainter.RenderHint.Antialiasing)

  def viewport(self) -> QRect:
    """Returns the viewport"""
    if self.__inner_rect__ is None:
      return QPainter.viewport(self)
    return self.__inner_rect__

  def setInnerViewport(self, rect: QRect) -> None:
    """Sets the viewport"""
    # QPainter.setViewport(self, rect)
    self.translate(rect.topLeft())
    self.__inner_rect__ = QRect(QPoint(0, 0), rect.size())

  def end(self) -> None:
    """Ends the painting"""
    self.__inner_rect__ = None
    QPainter.end(self)