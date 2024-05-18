"""Parses a QPen from given arguments."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor

from ezside.core import SolidLine


def parsePen(*args) -> QPen:
  """Parses a QPen from given arguments."""
  pen = QPen()
  width, color, style, capStyle, joinStyle = None, None, None, None, None
  for arg in args:
    if isinstance(arg, QPen):
      return arg
    if isinstance(arg, QColor) and color is None:
      color = arg
    elif isinstance(arg, Qt.PenStyle) and style is None:
      style = arg
    elif isinstance(arg, Qt.PenCapStyle) and capStyle is None:
      capStyle = arg
    elif isinstance(arg, Qt.PenJoinStyle) and joinStyle is None:
      joinStyle = arg
    elif isinstance(arg, int) and width is None:
      width = arg
  width = 1 if width is None else width
  color = QColor(0, 0, 0, ) if color is None else color
  style = SolidLine if style is None else style
  capStyle = Qt.PenCapStyle.FlatCap if capStyle is None else capStyle
  joinStyle = Qt.PenJoinStyle.MiterJoin if joinStyle is None else joinStyle
  pen.setWidth(width)
  pen.setColor(color)
  pen.setStyle(style)
  pen.setCapStyle(capStyle)
  pen.setJoinStyle(joinStyle)
  return pen


def emptyPen() -> QPen:
  """Returns an empty pen."""
  pen = QPen()
  pen.setStyle(Qt.PenStyle.NoPen)
  pen.setColor(QColor(0, 0, 0, 0, ))
  return pen
