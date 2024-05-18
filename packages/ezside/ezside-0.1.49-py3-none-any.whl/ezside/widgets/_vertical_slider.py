"""VerticalSlider provides a vertical slider widget. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRectF, QPointF, QSizeF, Qt
from PySide6.QtGui import QMouseEvent, QColor, QKeyEvent
from vistutils.waitaminute import typeMsg

from ezside.core import SolidFill, parseBrush, parsePen, SolidLine
from ezside.widgets import HorizontalSlider, GraffitiVandal


class VerticalSlider(HorizontalSlider):
  """VerticalSlider provides a vertical slider widget. """

  __handle_height__ = 16

  def _setHandleAbsolutePosition(self, event: QMouseEvent = None) -> None:
    """Setter-function for the handle absolute position"""
    if event is None:
      mouse = self._getGrabbedPoint()
    elif isinstance(event, QMouseEvent):
      mouse = event.pos().toPointF()
    else:
      e = typeMsg('event', event, QMouseEvent)
      raise TypeError(e)
    y = mouse.y() - self.__top_left__.y() - self.__handle_height__ / 2
    viewHeight = self.__view_rect__.height() - self.__handle_height__
    absP = max(y, 0)
    absP = min(absP, viewHeight)
    self._setHandlePosition(1 - absP / viewHeight)

  def _getHandleRect(self, viewRect: QRectF, ) -> QRectF:
    """Getter-function for the handle rectangle"""
    handleWidth = viewRect.width()
    handleHeight = self.__handle_height__
    rangeStart = handleHeight / 2
    rangeEnd = viewRect.height() - handleHeight / 2
    rangeLength = rangeEnd - rangeStart
    handleVCenter = rangeEnd - rangeLength * self._getHandlePosition()
    handleHCenter = viewRect.width() / 2
    handleSize = QSizeF(viewRect.width(), handleHeight)
    handleRect = QRectF(QPointF(0, 0), handleSize)
    handleRect.moveCenter(QPointF(handleHCenter, handleVCenter))
    return handleRect

  def customPaint(self, painter: GraffitiVandal) -> None:
    """Custom painting function"""
    viewRect = painter.viewport().toRectF()
    self.__view_rect__ = viewRect
    self.__top_left__ = painter.getTopLeft()
    self.__bottom_right__ = painter.getBottomRight()
    handleRect = self._getHandleRect(viewRect)
    grooveHeight = viewRect.height()
    grooveWidth = 3
    grooveRect = QRectF(QPointF(0, 0), QSizeF(grooveWidth, grooveHeight))
    grooveRect.moveCenter(viewRect.center())
    #  Paint background
    painter.setBrush(self.getStyle('backgroundBrush'))
    painter.drawRect(painter.viewport())
    #  Paint groove
    grooveBrush = parseBrush(QColor(0, 0, 0, 255), SolidFill)
    painter.setBrush(grooveBrush)
    painter.drawRect(grooveRect)
    #  Paint handle
    handleBrush = parseBrush(QColor(144, 255, 47, 255), SolidFill)
    handlePen = parsePen(QColor(0, 0, 0, 255), 1, SolidLine)
    painter.setBrush(handleBrush)
    painter.setPen(handlePen)
    painter.drawRect(handleRect)

  def keyPressEvent(self, event: QKeyEvent) -> None:
    """Key press event"""
    if event.key() == Qt.Key.Key_Escape:
      self.cancelHandle()
      self.update()
    elif event.key() == Qt.Key.Key_Left:
      self.stepDown(0.2)
    elif event.key() == Qt.Key.Key_Right:
      self.stepUp(0.2)
    elif event.key() == Qt.Key.Key_Up:
      self.stepUp()
    elif event.key() == Qt.Key.Key_Down:
      self.stepDown()
    elif event.key() == Qt.Key.Key_PageDown:
      self.stepDown(0.5)
    elif event.key() == Qt.Key.Key_PageUp:
      self.stepUp(0.5)
    elif event.key() == Qt.Key.Key_End:
      self._setHandlePosition(1)
      self.update()
    elif event.key() == Qt.Key.Key_Home:
      self._setHandlePosition(0)
      self.update()
