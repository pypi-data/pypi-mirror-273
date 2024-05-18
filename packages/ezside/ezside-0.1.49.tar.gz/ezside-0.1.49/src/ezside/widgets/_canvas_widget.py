"""CanvasWidget provides a canvas widget. It supports the box model with
an outer margin, a border and padding. Subclasses should allow the parent
class to paint the background and border before painting the custom
content. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QPoint, QRect, QPointF, QRectF, QSizeF, QSize
from PySide6.QtCore import QMargins
from PySide6.QtGui import QPaintEvent, QColor, QBrush, QFocusEvent, QPainter
from icecream import ic
from vistutils.text import monoSpace

from ezside.widgets import BaseWidget, GraffitiVandal
from ezside.core import parseBrush, SolidFill, emptyPen, AlignTop, AlignFlag
from ezside.core import AlignCenter, AlignBottom, AlignVCenter, AlignLeft
from ezside.core import AlignHCenter, AlignRight

ic.configureOutput(includeContext=True)


class CanvasWidget(BaseWidget):
  """CanvasWidget provides a canvas widget. It supports the box model with
  an outer margin, a border and padding. Subclasses should allow the parent
  class to paint the background and border before painting the custom
  content. """

  __focus_paint__ = False
  __has_focus__ = None
  __forced_styles__ = None

  @staticmethod
  def getStyleTypes() -> dict[str, type]:
    """Getter-function for the style types."""
    return {
      'margins'        : QMargins,
      'borders'        : QMargins,
      'paddings'       : QMargins,
      'borderBrush'    : QBrush,
      'backgroundBrush': QBrush,
      'radius'         : QPoint,
      'vAlign'         : AlignFlag,
      'hAlign'         : AlignFlag,
    }

  @classmethod
  def typeGuard(cls, name: str, value: Any) -> Any:
    """The styleTypes method provides the type expected at each name. """
    data = cls.getStyleTypes()
    styleType = data.get(name, None)
    if styleType is None:
      e = """Unrecognized style name: '%s'"""
      raise KeyError(monoSpace(e % name))
    if isinstance(value, styleType):
      return True
    e = """Expected a value of type '%s' for style '%s'!"""
    raise TypeError(monoSpace(e % (str(styleType), name)))

  @classmethod
  def getFallbackStyles(cls) -> dict[str, Any]:
    """The fallbackStyles method provides the default values for the
    styles."""
    return {
      'margins'        : QMargins(2, 2, 2, 2, ),
      'borders'        : QMargins(2, 2, 2, 2, ),
      'paddings'       : QMargins(2, 2, 2, 2, ),
      'borderBrush'    : parseBrush(QColor(0, 0, 0, 255), SolidFill, ),
      'backgroundBrush': parseBrush(QColor(215, 215, 215), SolidFill, ),
      'radius'         : QPoint(8, 8, ),
      'vAlign'         : AlignVCenter,
      'hAlign'         : AlignHCenter,
    }

  @classmethod
  def fallbackStyles(cls, name: str) -> Any:
    """The registerFields method registers the fields of the widget.
    Please note, that subclasses can reimplement this method, but must
    provide these same fields. """
    fallbackStyles = cls.getFallbackStyles()
    style = fallbackStyles.get(name, None)
    if style is None:
      e = """Unrecognized style name: '%s'"""
      raise KeyError(monoSpace(e % name))
    return style

  def defaultStyles(self, name: str) -> Any:
    """The defaultStyles method provides the default values for the
    styles."""

  def initSignalSlot(self) -> None:
    """The initSignalSlot method connects signals and slots."""

  def initUi(self) -> None:
    """The initUi method initializes the user interface."""

  def alignRect(self, *args) -> QRect:
    """Calculates the aligned rectangle for text"""
    static, moving = None, None
    for arg in args:
      if isinstance(arg, QRectF):
        if static is None:
          static = arg.toRect()
        elif moving is None:
          moving = arg.toRect()
      if isinstance(arg, QRect):
        if static is None:
          static = arg
        elif moving is None:
          moving = arg
      if isinstance(arg, (QSize, QSizeF)):
        if static is None:
          e = """Received a size argument before a rectangle argument!"""
          raise ValueError(monoSpace(e))
        if isinstance(arg, QSizeF):
          moving = arg.toSize()
        else:
          moving = arg
    if static is None or moving is None:
      e = """Missing a rectangle argument!"""
      raise ValueError(monoSpace(e))
    vAlign = self.getStyle('vAlign')
    hAlign = self.getStyle('hAlign')
    staticHeight, movingHeight = static.height(), moving.height()
    staticWidth, movingWidth = static.width(), moving.width()
    if vAlign == AlignTop:
      top = static.top()
    elif vAlign in [AlignCenter, AlignVCenter]:
      top = static.top() + (staticHeight - movingHeight) / 2
    elif vAlign == AlignBottom:
      top = static.bottom() - movingHeight
    else:
      e = """Unrecognized value for vertical alignment: '%s'"""
      raise ValueError(monoSpace(e % str(vAlign)))
    if hAlign == AlignLeft:
      left = static.left()
    elif hAlign in [AlignCenter, AlignHCenter]:
      left = static.left() + (staticWidth - movingWidth) / 2
    elif hAlign == AlignRight:
      left = static.right() - movingWidth
    else:
      e = """Unrecognized value for horizontal alignment: '%s'"""
      raise ValueError(monoSpace(e % str(hAlign)))
    topLeft = QPointF(left, top).toPoint()
    return QRect(topLeft, moving)

  def paintEvent(self, event: QPaintEvent, ) -> None:
    """The paintEvent method paints the widget."""
    margins = self.getStyle('margins')
    borders = self.getStyle('borders')
    paddings = self.getStyle('paddings')
    radius = self.getStyle('radius')
    backgroundBrush = self.getStyle('backgroundBrush')
    borderBrush = self.getStyle('borderBrush')
    painter = GraffitiVandal()
    painter.begin(self)
    viewRect = painter.viewport()
    pen = emptyPen()
    painter.setPen(pen)
    if radius is None:
      rx, ry = 0, 0
    else:
      rx, ry = radius.x(), radius.y()
    borderedRect = viewRect - margins
    paddedRect = borderedRect - borders
    innerRect = paddedRect - paddings
    borderedRect.moveCenter(viewRect.center())
    paddedRect.moveCenter(viewRect.center())
    innerRect.moveCenter(viewRect.center())
    if self.__has_focus__:
      focusBrush = parseBrush(QColor(255, 0, 0, 63), SolidFill)
      painter.setBrush(focusBrush)
      painter.drawRoundedRect(painter.viewport(), 0, 0, )
    painter.setBrush(borderBrush)
    painter.drawRoundedRect(borderedRect, rx, ry)
    painter.setBrush(backgroundBrush)
    painter.drawRoundedRect(paddedRect, rx, ry)
    painter.setInnerViewport(innerRect)
    self.customPaint(painter)
    painter.end()

  def customPaint(self, painter: GraffitiVandal) -> None:
    """Subclasses must reimplement this method to define the painting
    action. The painter is already set up and will be ended by the parent
    class. """

  def focusInEvent(self, event: QFocusEvent) -> None:
    """Handle the widget's focus-in event. """
    self.__has_focus__ = True
    self.update()

  def focusOutEvent(self, event: QFocusEvent) -> None:
    """Handle the widget's focus-out event. """
    self.__has_focus__ = False
    self.update()

  def _getForcedStyle(self, name: str) -> Any:
    """Get the forced style."""
    if self.__forced_styles__ is None:
      self.__forced_styles__ = {}
      return None
    return self.__forced_styles__.get(name, None)

  def forceStyle(self, name: str, value: Any) -> None:
    """Force the style."""
    self.__forced_styles__ = {**(self.__forced_styles__ or {}), name: value}
