"""PushButton is a subclass of CanvasWidget providing push button
functionality. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import Any

from PySide6.QtCore import QEvent, QMargins, Signal, Slot
from PySide6.QtGui import QMouseEvent, QEnterEvent, QColor, QFontMetrics
from PySide6.QtWidgets import QWidget
from icecream import ic

from ezside.core import EZTimer, \
  Precise, \
  SolidLine, \
  parseBrush, \
  SolidFill, Tight
from ezside.core import LeftClick, Click
from ezside.widgets import Label, BaseWidget

ic.configureOutput(includeContext=True)


class StaticState(Enum):
  """StaticState describes the possible states of a widget that can change
  at runtime, but which are not dependent on user interaction. """
  DISABLED = -1
  NORMAL = 0
  CHECKED = 1


class DynamicState(Enum):
  """DynamicState describes the possible states of a widget relative to
  immediate user input, such as hover or pressed. """
  NORMAL = 0
  HOVER = 1
  PRESSED = 2
  MOVING = 3


class PushButton(Label):
  """PushButton is a subclass of CanvasWidget providing push button
  functionality. """

  _moveTimer = EZTimer(100, Precise, singleShot=True)
  _releaseTimer = EZTimer(125, Precise, singleShot=True)

  __is_enabled__ = True
  __is_checked__ = None
  __is_hovered__ = None
  __is_pressed__ = None
  __click_press__ = None
  __is_moving__ = None
  __cursor_x__ = None
  __cursor_y__ = None
  __press_x__ = None
  __press_y__ = None
  __active_button__ = None

  singleClick = Signal()

  def setEnabled(self, enabled: bool) -> None:
    """This method sets the enabled state of the button. """
    self.__is_enabled__ = True if enabled else False
    self.update()

  def initUi(self, ) -> None:
    """Initialize the user interface."""
    self.setSizePolicy(Tight, Tight)
    textRect = QFontMetrics(self.getStyle('font')).boundingRect(self.text)
    outerRect = textRect + self.getStyle('paddings')
    outerRect += self.getStyle('borders')
    outerRect += self.getStyle('margins')
    self.setMouseTracking(True)

  def initSignalSlot(self, ) -> None:
    """Initialize the signal slot."""

  def _movingStop(self) -> None:
    """If a mouse move event has not occurred for the time set in the
    moving timer, this method is called to stop the moving state. Please
    note, that the 'mouseMoveEvent' is responsible for starting and
    stopping the timer. """
    self.__is_moving__ = False

  @classmethod
  def styleTypes(cls) -> dict[str, type]:
    """The styleTypes method provides the type expected at each name. """
    return {**Label.styleTypes(), **{
      'driftLimit': int,
    }}

  @classmethod
  def staticStyles(cls, ) -> dict[str, Any]:
    """This method returns the current static state of the button. """
    borderBrush = parseBrush(QColor(0, 0, 63, 255), SolidLine)
    buttonStyles = {
      'driftLimit': 4,
    }
    return {**Label.staticStyles(), **buttonStyles}

  def getState(self, ) -> tuple[StaticState, DynamicState]:
    """This method returns the current state of the button. """
    staticState = StaticState.NORMAL
    if not self.__is_enabled__:
      staticState = StaticState.DISABLED
    elif self.__is_checked__:
      staticState = StaticState.CHECKED
    dynamicState = DynamicState.NORMAL
    if self.__is_hovered__:
      dynamicState = DynamicState.HOVER
    if self.__is_pressed__:
      dynamicState = DynamicState.PRESSED
    elif self.__is_moving__:
      dynamicState = DynamicState.MOVING
    return staticState, dynamicState

  def dynStyles(self, ) -> dict[str, Any]:
    """This implementation defines how the button is rendered depending
    on its current state. The BaseWidget class does not provide state
    awareness on the instance level at runtime, so this method returns the
    dictionary that matches the current state. """
    state = self.getState()
    borderBrush = parseBrush(QColor(223, 223, 223, 255), SolidFill)
    normalNormal = (StaticState.NORMAL, DynamicState.NORMAL)
    normalHover = (StaticState.NORMAL, DynamicState.HOVER)
    normalPressed = (StaticState.NORMAL, DynamicState.PRESSED)
    normalMoving = (StaticState.NORMAL, DynamicState.MOVING)

    if state == normalNormal:
      return {
        'padding'        : QMargins(2, 2, 2, 2),
        'borders'        : QMargins(2, 2, 2, 2),
        'borderBrush'    : parseBrush(QColor(0, 0, 0, 144), SolidFill),
        'backgroundBrush': parseBrush(QColor(223, 223, 223, 255), SolidFill),
      }
    if state in [normalHover, normalMoving]:
      return {
        'padding'        : QMargins(2, 2, 2, 2),
        'borders'        : QMargins(2, 2, 2, 2, ),
        'borderBrush'    : parseBrush(QColor(0, 0, 0, 191), SolidFill),
        'backgroundBrush': parseBrush(QColor(191, 191, 191, 255), SolidFill),
      }
    if state in [normalPressed, ]:
      return {
        'padding'        : QMargins(2, 4, 2, 0),
        'borders'        : QMargins(2, 0, 2, 4, ),
        'borderBrush'    : parseBrush(QColor(0, 0, 0, 255), SolidFill),
        'backgroundBrush': parseBrush(QColor(169, 169, 169, 255), SolidFill),
      }

  def enterEvent(self, event: QEnterEvent) -> None:
    """This method is called when the mouse enters the button. """
    self._updateCursor(event)
    self.__is_hovered__ = True
    self.update()

  def leaveEvent(self, event: QEvent) -> None:
    """This method is called when the mouse leaves the button. """
    self._updateCursor(event)
    self.__is_hovered__ = False
    self.__is_pressed__ = False
    self.__is_moving__ = False
    self.update()

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """This method is called when the mouse is pressed on the button. """
    self.__is_pressed__ = True
    self.__is_hovered__ = True
    self.update()
    self.__press_x__, self.__press_y__ = event.pos().x(), event.pos().y()

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """This method is called when the mouse is released on the button. """
    self.__is_pressed__ = False
    self.__is_hovered__ = True
    self.update()
    x, y = event.pos().x(), event.pos().y()
    x0, y0 = self.__press_x__, self.__press_y__
    if (x - x0) ** 2 + (y - y0) ** 2 < self.getStyle('driftLimit') ** 2:
      self.singleClick.emit()

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """This method is called when the mouse is moved over the button. """
    if self._cursorDrift(event) < self.getStyle('driftLimit') ** 2:
      return  # Ignore small drifts
    self.__is_moving__ = True
    self._moveTimer.stop()
    self._updateCursor(event)
    self._moveTimer.start()

  def _updateCursor(self, event: QEvent) -> None:
    """This method updates the cursor position. """
    if isinstance(event, (QMouseEvent, QEnterEvent)):
      self.__cursor_x__ = event.pos().x()
      self.__cursor_y__ = event.pos().y()
    elif event.type() == QEvent.Type.Leave:
      self.__cursor_x__ = None
      self.__cursor_y__ = None

  def _cursorDrift(self, event: QMouseEvent) -> float:
    """This method calculates the distance between the cursor position in
    the event and the most recent cursor position stored in the widget.
    Please note, that the squared value is returned."""
    if self.__cursor_x__ is None or self.__cursor_y__ is None:
      return 99999.
    x0, y0 = self.__cursor_x__, self.__cursor_y__
    ex, ey = event.pos().x(), event.pos().y()
    return (ex - x0) ** 2 + (ey - y0) ** 2
