"""Label provides the general class for widgets whose primary function is
to display text. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from PySide6.QtCore import QMargins, QPoint, QRect, QSize, Slot
from PySide6.QtGui import QColor, QPainter, QFontMetrics, QPen, QFont, QBrush
from attribox import AttriBox
from icecream import ic
from vistutils.fields import EmptyField
from vistutils.parse import maybe

from ezside.core import AlignHCenter
from ezside.core import SolidLine, parseFont, parsePen, AlignLeft, Center
from ezside.core import Normal, parseBrush, SolidFill, AlignVCenter, Bold
from ezside.core import MixCase

from ezside.widgets import CanvasWidget

ic.configureOutput(includeContext=True, )


class Label(CanvasWidget):
  """Label provides the   general class for widgets"""

  __fallback_text__ = 'Label'

  prefix = AttriBox[str]('')
  text = AttriBox[str]('lmao')
  suffix = AttriBox[str]('')

  fullText = EmptyField()

  @Slot(object)
  def echo(self, newText: Any) -> None:
    """Updates the text between prefix and suffix"""
    if isinstance(newText, str):
      self.text = newText
    else:
      self.text = str(newText)
    self.fitText()

  @fullText.GET
  def _getFullText(self) -> str:
    """Getter-function for the text including prefix and suffix."""
    return '%s%s%s' % (self.prefix, self.text, self.suffix)

  def __init__(self, *args, **kwargs) -> None:
    posArgs = []
    iniText = None
    for arg in args:
      if isinstance(arg, str):
        iniText = arg
      else:
        posArgs.append(arg)
    super().__init__(*posArgs, **kwargs)
    self.text = maybe(iniText, self.__fallback_text__)
    self.prefix = kwargs.get('prefix', '')
    self.suffix = kwargs.get('suffix', '')
    self.fitText(self.__fallback_text__)

  @text.ONSET
  def _textSetterHook(self, *args) -> None:
    """Triggered by the hook in the __set__ on the AttriBox instance."""
    self.fitText(floor=True)
    self.update()

  def fitText(self, sampleText: str = None, **kwargs) -> None:
    """Fits the text to the widget."""
    if TYPE_CHECKING:
      assert isinstance(self.fullText, str)
    metrics = QFontMetrics(self.getStyle('font'))
    paddings = self.getStyle('paddings')
    borders = self.getStyle('borders')
    margins = self.getStyle('margins')
    innerRect = metrics.boundingRect(self.fullText)
    if sampleText is not None:
      sampleRect = metrics.boundingRect(sampleText)
      sampleWidth, sampleHeight = sampleRect.width(), sampleRect.height()
      innerWidth, innerHeight = innerRect.width(), innerRect.height()
      width = max(sampleWidth, innerWidth)
      height = max(sampleHeight, innerHeight)
      innerRect = QRect(innerRect.topLeft(), QSize(width, height))
    viewRect = innerRect + paddings + borders + margins
    minW, minH = self.minimumWidth(), self.minimumHeight()
    viewW, viewH = viewRect.width(), viewRect.height()
    if minW < viewW or minH < viewH:
      self.setMinimumSize(viewRect.size())

  def initUi(self) -> None:
    """Initializes the user interface."""

  def initSignalSlot(self) -> None:
    """Connects signals and slots"""

  @staticmethod
  def getStyleTypes() -> dict[str, type]:
    """Getter-function for the style types for Label."""
    parentStyleTypes = CanvasWidget.getStyleTypes()
    LabelStyleTypes = {
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
    }
    return {**parentStyleTypes, **LabelStyleTypes}

  @classmethod
  def getFallbackStyles(cls) -> dict[str, Any]:
    """The fallbackStyles method provides the default values for the
    styles."""
    parentFallbackStyles = CanvasWidget.getFallbackStyles()
    fallbackStyles = {
      'font'           : parseFont('Montserrat', 12, Normal, MixCase),
      'textPen'        : parsePen(QColor(0, 0, 0, 255), 1, SolidLine),
      'backgroundBrush': parseBrush(QColor(223, 223, 223, 255), SolidFill),
      'borderBrush'    : parseBrush(QColor(223, 223, 223, 255), SolidFill),
      'margins'        : QMargins(2, 2, 2, 2, ),
      'borders'        : QMargins(2, 2, 2, 2),
      'paddings'       : QMargins(4, 4, 4, 4, ),
      'radius'         : QPoint(4, 4),
      'vAlign'         : AlignVCenter,
      'hAlign'         : AlignLeft,
    }
    return {**parentFallbackStyles, **fallbackStyles}

  def getDefaultStyles(self) -> dict[str, Any]:
    """Getter-function for the default styles for Label."""
    if self.getId() == 'title':
      return {'font'  : parseFont('Montserrat', 20, Bold, MixCase),
              'hAlign': AlignHCenter, }
    if self.getId() == 'header':
      return {'font': parseFont('Montserrat', 16, Bold, MixCase), }
    if self.getId() == 'normal':
      return {'font': parseFont('Montserrat', 12, Normal, MixCase), }
    if self.getId() == 'info':
      return {'font'       : parseFont('Consolas', 10, Normal, MixCase),
              'textPen'    : parsePen(QColor(63, 0, 0, 255), 1, SolidLine),
              'borderBrush': parseBrush(QColor(255, 0, 0, 255), SolidFill),
              'hAlign'     : AlignHCenter, }

  def defaultStyles(self, name: str) -> Any:
    """Subclasses are free to define this method to provide id and state
    sensitive styling options. Please note that values obtained from the
    AppSettings class will override the values provided here. """
    data = maybe(self.getDefaultStyles(), {})
    return data.get(name, None)

  def customPaint(self, painter: QPainter) -> None:
    """Custom paint method for Label."""
    if TYPE_CHECKING:
      assert isinstance(self.fullText, str)
    viewRect = painter.viewport()
    painter.setFont(self.getStyle('font'))
    painter.setPen(self.getStyle('textPen'))
    textSize = painter.boundingRect(viewRect, Center, self.fullText).size()
    textRect = self.alignRect(viewRect, textSize)
    painter.drawText(textRect, Center, self.fullText)
