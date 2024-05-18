"""GraffitiVandal provides a subclass of QPainter that allows for
sequential painting functions to react to the same QPaintEvent."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRect, QPoint, QMargins
from PySide6.QtGui import QPainter


class GraffitiVandal(QPainter):
  """GraffitiVandal provides a subclass of QPainter that allows for
  sequential painting functions to react to the same QPaintEvent."""

  __inner_rect__ = None
  __top_left__ = None
  __bottom_right__ = None

  def begin(self, *args) -> None:
    """Begins the painting"""
    QPainter.begin(self, *args)
    QPainter.setRenderHint(self, QPainter.RenderHint.Antialiasing)

  def getTopLeft(self, ) -> QPoint:
    """Returns the top left corner of the viewport"""
    if self.__top_left__ is None:
      return QPoint(0, 0)
    return self.__top_left__

  def getBottomRight(self, ) -> QPoint:
    """Returns the bottom right corner of the viewport"""
    if self.__bottom_right__ is None:
      return QPoint(self.device().width(), self.device().height())
    return self.__bottom_right__

  def getOuterMargins(self) -> QMargins:
    """Returns the outer margins"""
    return QMargins(self.getTopLeft(), self.getBottomRight())

  def viewport(self) -> QRect:
    """Returns the viewport"""
    if self.__inner_rect__ is None:
      return QPainter.viewport(self)
    return self.__inner_rect__

  def setInnerViewport(self, rect: QRect) -> None:
    """Sets the viewport"""
    # QPainter.setViewport(self, rect)
    self.__top_left__ = rect.topLeft()
    self.__bottom_right__ = rect.bottomRight()
    self.translate(self.__top_left__)
    self.__inner_rect__ = QRect(QPoint(0, 0), rect.size())

  def end(self) -> None:
    """Ends the painting"""
    self.__inner_rect__ = None
    QPainter.end(self)
