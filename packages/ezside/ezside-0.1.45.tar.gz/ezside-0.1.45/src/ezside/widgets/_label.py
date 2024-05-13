"""Label provides the general class for widgets whose primary function is
to display text. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QMargins, QPoint, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QFontMetrics, QPen, QFont, QBrush
from attribox import AttriBox
from icecream import ic

from ezside.core import SolidLine, \
  parseFont, \
  parsePen, \
  AlignLeft, \
  Center, \
  Normal, parseBrush, SolidFill
from ezside.core import AlignVCenter
from ezside.core import Bold, MixCase
from ezside.widgets import CanvasWidget

ic.configureOutput(includeContext=True, )


class Label(CanvasWidget):
  """Label provides the   general class for widgets"""
  __fallback_text__ = 'Label'

  text = AttriBox[str]('lmao')

  def __init__(self, *args, **kwargs) -> None:
    posArgs = []
    iniText = None
    for arg in args:
      if isinstance(arg, str) and iniText is None:
        self.text = arg
      else:
        posArgs.append(arg)
    super().__init__(*posArgs, **kwargs)
    self.fitText()
    self.fitText('blabla ')

  def fitText(self, sampleText: str = None) -> None:
    """Fits the text to the widget."""
    metrics = QFontMetrics(self.getStyle('font'))
    paddings = self.getStyle('paddings')
    borders = self.getStyle('borders')
    margins = self.getStyle('margins')
    innerRect = metrics.boundingRect(self.text)
    if sampleText is not None:
      sampleRect = metrics.boundingRect(sampleText)
      sampleWidth, sampleHeight = sampleRect.width(), sampleRect.height()
      innerWidth, innerHeight = innerRect.width(), innerRect.height()
      width = max(sampleWidth, innerWidth)
      height = max(sampleHeight, innerHeight)
      innerRect = QRect(innerRect.topLeft(), QSize(width, height))
    viewRect = innerRect + paddings + borders + margins
    self.setMinimumSize(viewRect.size())

  def initUi(self) -> None:
    """Initializes the user interface."""

  def initSignalSlot(self) -> None:
    """Connects signals and slots"""

  @classmethod
  def styleTypes(cls) -> dict[str, type]:
    """Registers the field types for Label."""
    return {**CanvasWidget.styleTypes(), **{
      'font'           : QFont,
      'textPen'        : QPen,
      'backgroundBrush': QBrush,
      'borderBrush'    : QBrush,
      'margins'        : QMargins,
      'borders'        : QMargins,
      'paddings'       : QMargins,
      'radius'         : QPoint,
      'vAlign'         : int,
      'hAlign'         : int,
    }, }

  @classmethod
  def registerStyleIds(cls) -> list[str]:
    """Registers the supported style IDs for Label."""
    return ['title', 'warning', 'normal']

  @classmethod
  def registerStates(cls) -> list[str]:
    """Registers the supported states for Label."""
    return ['base', 'focus']

  @classmethod
  def staticStyles(cls) -> dict[str, Any]:
    """Registers default field values for Label, providing a foundation
    for customization across different styleIds and states."""
    backgroundBrush = parseBrush(QColor(223, 223, 223, 255), SolidFill)
    borderBrush = parseBrush(QColor(223, 223, 223, 255), SolidFill)
    return {**CanvasWidget.staticStyles(), **{
      'font'           : parseFont('Montserrat', 12, Normal, MixCase),
      'textPen'        : parsePen(QColor(0, 0, 0, 255), 1, SolidLine),
      'backgroundBrush': backgroundBrush,
      'borderBrush'    : borderBrush,
      'margins'        : QMargins(2, 2, 2, 2, ),
      'borders'        : QMargins(2, 2, 2, 2),
      'paddings'       : QMargins(4, 4, 4, 4, ),
      'radius'         : QPoint(4, 4),
      'vAlign'         : AlignVCenter,
      'hAlign'         : AlignLeft,
    }}

  def dynStyles(self) -> dict[str, Any]:
    """Defines dynamic fields based on styleId and state. These settings
    override the base field values in specific styles and states."""
    if self.getId() == 'title':
      return {
        'font': parseFont('Montserrat', 16, Bold, MixCase),
      }
    if self.getId() == 'warning':
      return {
        'font': parseFont('Montserrat', 12, Bold, MixCase),
      }

  def customPaint(self, painter: QPainter) -> None:
    """Custom paint method for Label."""
    viewRect = painter.viewport()
    painter.setFont(self.getStyle('font'))
    painter.setPen(self.getStyle('textPen'))
    textSize = painter.boundingRect(viewRect, Center, self.text).size()
    textRect = self.alignRect(viewRect, textSize)
    painter.drawText(textRect, Center, self.text)
