"""SevenSegmentDigit class for displaying numbers on a 7-segment display."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSizeF, QPointF, QRectF, QMargins, QPoint
from PySide6.QtGui import QPainter, QBrush, QColor, QPen
from PySide6.QtWidgets import QWidget
from icecream import ic
from vistutils.parse import maybe
from vistutils.waitaminute import typeMsg

from ezside.core import SolidLine, \
  AlignHCenter, \
  AlignVCenter, \
  parseBrush, \
  AlignFlag
from ezside.core import SolidFill, parsePen
from ezside.widgets import CanvasWidget

ic.configureOutput(includeContext=True, )


class SevenSegmentDigit(CanvasWidget):
  """SevenSegment class for displaying numbers on a 7-segment display."""

  __inner_value__ = None
  __power_scale__ = None
  __inner_scale__ = None
  __is_dot__ = None

  def __init__(self, *args, **kwargs) -> None:
    self.__power_scale__ = kwargs.get('scale', 1)
    parent, scale = None, kwargs.get('scale', None)
    for arg in args:
      if isinstance(arg, QWidget) and parent is None:
        parent = arg
      elif isinstance(arg, int) and scale is None:
        power = arg
      if parent is not None and scale is not None:
        break
    else:
      self.__inner_scale__ = maybe(scale, 1)
    CanvasWidget.__init__(self, *args, **kwargs)
    self.__is_dot__ = kwargs.get('dot', False)
    if self.getId() == 'clock':
      self.setFixedSize(32, 64)
    if self.getId() == 'statusBarClock':
      self.setFixedSize(16, 32)

  def initUi(self, ) -> None:
    """Initialize the user interface."""

  def initSignalSlot(self) -> None:
    """Initialize the signal slot."""

  @staticmethod
  def getStyleTypes() -> dict[str, type]:
    """The styleTypes method provides the type expected at each name."""
    canvasWidgetStyles = CanvasWidget.getStyleTypes()
    sevenSegmentDigitStyles = {
      'highBrush'      : QBrush,
      'lowBrush'       : QBrush,
      'backgroundBrush': QBrush,
      'borderBrush'    : QBrush,
      'highPen'        : QPen,
      'lowPen'         : QPen,
      'margins'        : QMargins,
      'borders'        : QMargins,
      'paddings'       : QMargins,
      'radius'         : QPoint,
      'vAlign'         : AlignFlag,
      'hAlign'         : AlignFlag,
      'aspect'         : float,
      'spacing'        : int,
    }
    return {**canvasWidgetStyles, **sevenSegmentDigitStyles}

  @classmethod
  def getFallbackStyles(cls) -> dict[str, Any]:
    """Register the fields."""
    highBrush = parseBrush(QColor(0, 0, 0, 255), SolidFill)
    lowBrush = parseBrush(QColor(215, 215, 215, 255), SolidFill)
    highPen = parsePen(QColor(0, 0, 0, 255), 0, SolidLine)
    lowPen = parsePen(QColor(255, 255, 255, 255), 0, SolidLine)
    backgroundBrush = parseBrush(QColor(223, 223, 223, 255), SolidFill)
    borderBrush = parseBrush(QColor(223, 223, 223, 255), SolidFill)
    canvasWidgetStyles = CanvasWidget.getFallbackStyles()
    SevenSegmentDigitStyles = {
      'highBrush'      : highBrush,
      'lowBrush'       : lowBrush,
      'highPen'        : highPen,
      'lowPen'         : lowPen,
      'backgroundBrush': backgroundBrush,
      'borderBrush'    : borderBrush,
      'margins'        : QMargins(1, 1, 1, 1, ),
      'borders'        : QMargins(1, 1, 1, 1, ),
      'paddings'       : QMargins(1, 1, 1, 1, ),
      'radius'         : QPoint(1, 1, ),
      'vAlign'         : AlignVCenter,
      'hAlign'         : AlignHCenter,
      'aspect'         : 0.2,
      'spacing'        : 2,
    }
    return {**canvasWidgetStyles, **SevenSegmentDigitStyles}

  def getDefaultStyles(self, ) -> dict[str, Any]:
    """Implementation of dynamic fields"""
    if self.getId() in ['clock', 'statusBarClock']:
      highBrush = parseBrush(QColor(0, 0, 0, 255), SolidFill)
      lowBrush = parseBrush(QColor(191, 191, 191, 255), SolidFill)
      highPen = parsePen(QColor(0, 0, 0, 255), 0, SolidLine)
      lowPen = parsePen(QColor(191, 191, 191, 255), 0, SolidLine)
      backgroundBrush = parseBrush(QColor(207, 207, 207, 255), SolidFill)
      borderBrush = parseBrush(QColor(0, 0, 0, 255), SolidFill)
      return {
        'highBrush'      : highBrush,
        'lowBrush'       : lowBrush,
        'highPen'        : highPen,
        'lowPen'         : lowPen,
        'backgroundBrush': backgroundBrush,
        'borderBrush'    : borderBrush,
        'radius'         : QPoint(0, 0),
        'spacing'        : 1,
        'margins'        : QMargins(0, 0, 0, 0, ),
        'borders'        : QMargins(0, 0, 0, 0, ),
        'paddings'       : QMargins(0, 0, 0, 0, ),
      }

  def defaultStyles(self, name: str) -> Any:
    """Implementation of dynamic fields"""
    data = maybe(self.getDefaultStyles(), {})
    return data.get(name, None)

  def __int__(self, ) -> int:
    """Returns the inner value."""
    return self.getInnerValue() or 0

  def __float__(self) -> float:
    """Returns the inner value multiplied by 10 to the power at power
    scale. Please note that this may be negative. """
    return float(self.getInnerValue() * self.getScale()) or float(0)

  def getInnerValue(self) -> int:
    """Get the inner value."""
    self.update()
    if self.__inner_value__ is None:
      return 0
    if isinstance(self.__inner_value__, int):
      return self.__inner_value__ % 10
    e = typeMsg('inner_value', self.__inner_value__, int)
    raise TypeError(e)

  def setInnerValue(self, value: int) -> None:
    """Set the inner value."""
    self.update()
    if isinstance(value, int):
      self.__inner_value__ = value % 10
    else:
      e = typeMsg('value', value, int)
      raise TypeError(e)

  def increment(self) -> None:
    """Increments the inner value rolling over from 9 to 0"""
    self.update()
    self.__inner_value__ += 1
    self.__inner_value__ %= 10

  def decrement(self) -> None:
    """Decrements the inner value rolling over from 0 to 9"""
    self.update()
    self.__inner_value__ -= 1
    self.__inner_value__ %= 10

  def segState(self, segment: str) -> bool:
    """Get the segment state."""
    return True if segment in self.map7()[int(self)] else False

  @staticmethod
  def map7() -> list[list[str]]:
    """This method returns a list of lists of strings, where at each index
    of the outer list, there is a list of strings representing the segments
    that should be on for the corresponding digit. """
    return [
      ['A', 'B', 'C', 'D', 'E', 'F'],
      ['B', 'C'],
      ['A', 'B', 'G', 'E', 'D'],
      ['A', 'B', 'G', 'C', 'D'],
      ['F', 'G', 'B', 'C'],
      ['A', 'F', 'G', 'C', 'D'],
      ['A', 'F', 'G', 'C', 'D', 'E'],
      ['A', 'B', 'C'],
      ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
      ['A', 'B', 'C', 'D', 'F', 'G'],
    ]

  def map7seg(self) -> list[str]:
    """This method returns a list of strings representing the segments that
    should be on for the corresponding digit. """
    return self.map7()[int(self)]

  def getScale(self) -> int:
    """Public getter for the power scale."""
    return self.__inner_scale__ or 0.

  def customPaint(self, painter: QPainter) -> None:
    """Custom paint method for Label."""
    lowPen = self.getStyle('lowPen')
    lowBrush = self.getStyle('lowBrush')
    highPen = self.getStyle('highPen')
    highBrush = self.getStyle('highBrush')

    viewRect = painter.viewport()
    width, height = viewRect.width(), viewRect.height()
    spacing = self.getStyle('spacing')
    aspect = self.getStyle('aspect')
    segmentWidth = (width - 4 * spacing) / (1 + 2 * aspect)
    segmentHeight = aspect * segmentWidth
    hSize = QSizeF(segmentWidth, segmentHeight)
    vSize = QSizeF(segmentHeight, segmentWidth)
    EFLeft = spacing
    ADGLeft = 2 * spacing + segmentHeight
    BCLeft = ADGLeft + segmentWidth + spacing
    ATop = 0
    BFTop = spacing + segmentHeight
    CETop = BFTop + segmentWidth + 2 * spacing + segmentHeight
    DTop = CETop + segmentWidth + spacing
    GTop = ATop / 2 + DTop / 2
    topSpace = spacing
    bottomSpace = height - GTop + segmentHeight
    avgSpace = 0.5 * (topSpace + bottomSpace) - topSpace
    offSet = (height - DTop - segmentHeight) / 2

    segments = {
      'A': QRectF(QPointF(ADGLeft, ATop + offSet), hSize),
      'B': QRectF(QPointF(BCLeft, BFTop + offSet), vSize),
      'C': QRectF(QPointF(BCLeft, CETop + offSet), vSize),
      'D': QRectF(QPointF(ADGLeft, DTop + offSet), hSize),
      'E': QRectF(QPointF(EFLeft, CETop + offSet), vSize),
      'F': QRectF(QPointF(EFLeft, BFTop + offSet), vSize),
      'G': QRectF(QPointF(ADGLeft, GTop + offSet), hSize),
    }
    highSegments = []
    lowSegments = []
    high7 = self.map7seg()
    for (seg, rect) in segments.items():
      if seg in high7:
        highSegments.append(rect)
      else:
        lowSegments.append(rect)
    painter.setBrush(self.getStyle('lowBrush'))
    painter.setPen(self.getStyle('lowPen'))
    for rect in lowSegments:
      painter.drawRect(rect)
    painter.setBrush(self.getStyle('highBrush'))
    painter.setPen(self.getStyle('highPen'))
    for rect in highSegments:
      painter.drawRect(rect)
