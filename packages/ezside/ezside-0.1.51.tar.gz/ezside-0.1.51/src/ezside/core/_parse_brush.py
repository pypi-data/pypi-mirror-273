"""The parseBrush function creates instances of QBrush from a bunch of
arguments."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor

from ezside.core import SolidFill


def parseBrush(*args, **kwargs) -> QBrush:
  """The parseBrush function creates instances of QBrush from a bunch of
  arguments."""
  fillStyle, color = None, None
  for arg in args:
    if isinstance(arg, QBrush):
      return arg
    if isinstance(arg, Qt.BrushStyle) and fillStyle is None:
      fillStyle = arg
    if isinstance(arg, QColor) and color is None:
      color = arg
  fillStyle = SolidFill if fillStyle is None else fillStyle
  color = QColor(0, 0, 0, 0) if color is None else color
  brush = QBrush()
  brush.setStyle(fillStyle)
  brush.setColor(color)
  return brush


def emptyBrush() -> QBrush:
  """Returns an empty brush."""
  brush = QBrush()
  brush.setStyle(Qt.BrushStyle.NoBrush)
  brush.setColor(QColor(0, 0, 0, 0))
  return brush
