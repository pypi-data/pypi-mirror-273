"""AbstractSlider provides a custom baseclass for value input widgets
allowing the user to input values by moving a visual element with the
mouse or other input device. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRectF, QSizeF, Signal, QEvent, Qt, Slot
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QColor, QMouseEvent, QKeyEvent
from icecream import ic
from vistutils.parse import maybe
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import parseBrush, \
  SolidFill, \
  parsePen, \
  SolidLine
from ezside.widgets import CanvasWidget, GraffitiVandal
from moreattribox import Flag

if TYPE_CHECKING:
  from ezside.app import AppSettings, App

ic.configureOutput(includeContext=True)


class HorizontalSlider(CanvasWidget):
  """AbstractSlider provides a custom baseclass for value input widgets
  allowing the user to input values by moving a visual element with the
  mouse or other input device. """

  __handle_width__ = 16
  __handle_position__ = None  # in unit scale
  __grabbed_point__ = None
  __view_rect__ = None
  __top_left__ = None
  __bottom_right__ = None

  grabbed = Flag(False)

  handleGrabbed = Signal()
  handleMoved = Signal(float)
  handleReleased = Signal()
  handleCancelled = Signal()
  positionChanged = Signal(float)

  def initUi(self) -> None:
    """Initializes the user interface"""
    self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    app = QCoreApplication.instance()
    if TYPE_CHECKING:
      assert isinstance(app, App)
    settings = app.getSettings()
    if TYPE_CHECKING:
      assert isinstance(settings, AppSettings)
    clsName = self.__class__.__name__
    objName = self.objectName()
    key = '/%s/%s/%s' % (clsName, objName, 'handle')
    self._setHandlePosition(settings.value(key, 0.0))
    self.initSignalSlot()

  def initSignalSlot(self) -> None:
    """Initializes the signal-slot connections"""
    self.handleReleased.connect(self._saveHandlePosition)

  @Slot()
  def _saveHandlePosition(self, *_) -> None:
    """Save the handle position"""
    app = QCoreApplication.instance()
    if TYPE_CHECKING:
      assert isinstance(app, App)
    settings = app.getSettings()
    if TYPE_CHECKING:
      assert isinstance(settings, AppSettings)
    clsName = self.__class__.__name__
    objName = self.objectName()
    key = '/%s/%s/%s' % (clsName, objName, 'handle')
    settings.setValue(key, self._getHandlePosition())

  def _getHandlePosition(self) -> float:
    """Getter-function for the handle position"""
    return maybe(self.__handle_position__, 0.0)

  def _setHandlePosition(self, val: float) -> None:
    """Setter-function for the handle position"""
    if 0 > val or val > 1:
      e = """Handle position must be in unit range, but received: '%.3f'!"""
      raise ValueError(monoSpace(e % val))
    self.__handle_position__ = val
    self.positionChanged.emit(val)

  def _setHandleAbsolutePosition(self, event: QMouseEvent = None) -> None:
    """Setter-function for the handle absolute position"""
    if event is None:
      mouse = self._getGrabbedPoint()
    elif isinstance(event, QMouseEvent):
      mouse = event.pos().toPointF()
    else:
      e = typeMsg('event', event, QMouseEvent)
      raise TypeError(e)
    x = mouse.x() - self.__top_left__.x() - self.__handle_width__ / 2
    viewRect = self.__view_rect__
    viewWidth = self.__view_rect__.width() - self.__handle_width__
    absP = max(x, 0)
    absP = min(absP, viewWidth)
    self._setHandlePosition(absP / viewWidth)

  def _getGrabbedPoint(self) -> QPointF:
    """Getter-function for the grabbed point"""
    return self.__grabbed_point__

  def _setGrabbedPoint(self, grabbedPoint: QPointF) -> None:
    """Setter-function for the grabbed point"""
    self.__grabbed_point__ = grabbedPoint

  def _getHandleRect(self, viewRect: QRectF, ) -> QRectF:
    """Getter-function for the handle rectangle"""
    handleWidth = self.__handle_width__
    handleHeight = viewRect.height()
    rangeStart = handleWidth / 2
    rangeEnd = viewRect.width() - handleWidth / 2
    rangeLength = rangeEnd - rangeStart
    handleHCenter = rangeStart + rangeLength * self._getHandlePosition()
    handleVCenter = viewRect.height() / 2
    handleSize = QSizeF(handleWidth, viewRect.height() - 8)
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
    grooveHeight = 3
    grooveWidth = viewRect.width()
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

  def grabHandle(self, event: QMouseEvent) -> None:
    """Grabs the handle"""
    self.grabbed = True
    self.setFocus(Qt.FocusReason.MouseFocusReason)
    self._setGrabbedPoint(event.pos().toPointF())
    self.handleGrabbed.emit()

  def releaseHandle(self, event: QMouseEvent) -> None:
    """Releases the handle"""
    self.grabbed = False
    self.clearFocus()
    self.handleReleased.emit()
    self.handleMoved.emit(self._getHandlePosition())

  def cancelHandle(self) -> None:
    """Cancels the handle. This is called if the handle is released outside
    the widget or if the escape key is pressed. """
    self.grabbed = False
    self.handleCancelled.emit()
    self._setHandleAbsolutePosition()
    self.clearFocus()

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Mouse press event"""
    self.setFocus()
    viewRect = self.geometry()
    handleRect = self._getHandleRect(viewRect.toRectF())
    if handleRect.contains(event.pos()):
      self.grabHandle(event)
    elif handleRect.left() > event.pos().x():
      self.__handle_position__ *= 0.9
      self.update()
    elif handleRect.right() < event.pos().x():
      self.__handle_position__ *= 1.1
      self.update()

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Mouse move event"""
    if self.grabbed:
      self._setHandleAbsolutePosition(event)
      self.update()

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Mouse release event"""
    self.setFocus()
    if self.grabbed:
      self.releaseHandle(event)

  def leaveEvent(self, event: QEvent) -> None:
    """Leave event"""
    if self.grabbed:
      self.cancelHandle()
      self.update()

  def keyPressEvent(self, event: QKeyEvent) -> None:
    """Key press event"""
    if event.key() == Qt.Key.Key_Escape:
      self.cancelHandle()
      self.update()
    elif event.key() == Qt.Key.Key_Left:
      self.stepDown()
    elif event.key() == Qt.Key.Key_Right:
      self.stepUp()
    elif event.key() == Qt.Key.Key_Up:
      self.stepUp(0.2)
    elif event.key() == Qt.Key.Key_Down:
      self.stepDown(0.2)
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

  def stepDown(self, f: float = None) -> None:
    """Step down"""
    self.__handle_position__ *= (1 - maybe(f, 0.1))
    self.update()

  def stepUp(self, f: float = None) -> None:
    """Step Up"""
    top = (1 - self.__handle_position__) * maybe(f, 0.1)
    self.__handle_position__ += top
    self.update()
