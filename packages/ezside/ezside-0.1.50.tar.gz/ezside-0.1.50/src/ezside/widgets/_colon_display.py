"""ColonDisplay displays a colon. Used by digital clock widget. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QPointF, QMargins
from PySide6.QtGui import QPainter, QColor
from icecream import ic

from ezside.core import SolidFill, \
  SolidLine, \
  parseBrush, parsePen
from ezside.widgets import SevenSegmentDigit, CanvasWidget

ic.configureOutput(includeContext=True, )


class ColonDisplay(SevenSegmentDigit):
  """PunctuationDisplay widget provides a widget for displaying
  punctuation characters. """

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the widget."""
    super().__init__(*args, **kwargs)
    if self.getId() == 'clock':
      self.setFixedSize(12, 64)
    if self.getId() == 'statusBarClock':
      self.setFixedSize(6, 32)

  @classmethod
  def getFallbackStyles(cls) -> dict[str, Any]:
    """Register the fields."""
    highBrush = parseBrush(QColor(0, 0, 0, 255), SolidFill)
    lowBrush = parseBrush(QColor(215, 215, 215, 255), SolidFill)
    highPen = parsePen(QColor(0, 0, 0, 255), 0, SolidLine)
    lowPen = parsePen(QColor(255, 255, 255, 255), 0, SolidLine)
    backgroundBrush = parseBrush(QColor(223, 223, 223, 255), SolidFill)
    borderBrush = parseBrush(QColor(223, 223, 223, 255), SolidFill)
    SevenSegmentDigitStyles = SevenSegmentDigit.getFallbackStyles()
    colonStyles = {
      'highBrush'      : highBrush,
      'lowBrush'       : lowBrush,
      'highPen'        : highPen,
      'lowPen'         : lowPen,
      'backgroundBrush': backgroundBrush,
      'borderBrush'    : borderBrush,
      'aspect'         : 0.25,
      'spacing'        : 0,
    }
    return {**SevenSegmentDigitStyles, **colonStyles}

  def getDefaultStyles(self) -> dict[str, Any]:
    """Getter-function for the default styles"""
    if self.getId() == 'clock':
      return {'borders': QMargins(0, 0, 0, 0, ), }

  def getStyle(self, name: str) -> Any:
    """Get the style."""
    return super().getStyle(name)

  def customPaint(self, painter: QPainter) -> None:
    """Paint the widget."""
    viewRect = painter.viewport()
    width, height = viewRect.width(), viewRect.height()
    r = height / 16
    yTop = height / 3
    yBottom = height - yTop
    x = width / 2
    painter.setBrush(self.getStyle('highBrush'))
    painter.drawEllipse(QPointF(x, yTop), r, r)
    painter.drawEllipse(QPointF(x, yBottom), r, r)
