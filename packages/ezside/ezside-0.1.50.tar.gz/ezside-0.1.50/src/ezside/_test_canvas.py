"""TestCanvas provides a testing widget"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import Slot, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QColorDialog
from icecream import ic

from ezside.core import parseBrush, SolidFill
from ezside.dialogs import ColorSelection
from ezside.widgets import CanvasWidget, GraffitiVandal

ic.configureOutput(includeContext=True)


class TestCanvas(CanvasWidget):
  """LMAO"""

  yolo = Signal()

  def __init__(self, *args) -> None:
    """Initializes the TestCanvas"""
    CanvasWidget.__init__(self, *args)
    self._colorDialog = QColorDialog(self)

  def lmao(self) -> None:
    """YOLO"""
    ic('lmao')
    color = QColorDialog.getColor()
    ic(color)

  @Slot(QColor)
  def selectBackground(self, color: QColor) -> None:
    """Selects the background color"""
    self.forceStyle('backgroundBrush', parseBrush(color, SolidFill))
    self.update()

  def initUi(self) -> None:
    """Initializes the user interface"""
    self.initSignalSlot()

  def customPaint(self, painter: GraffitiVandal) -> None:
    """Subclasses must reimplement this method to define the painting
    action. The painter is already set up and will be ended by the parent
    class. """
    painter.setBrush(self.getStyle('backgroundBrush'))
    viewRect = painter.viewport()
    painter.drawRect(viewRect)

  def setBackgroundColor(self, color: QColor) -> None:
    """Sets the background color."""
    brush = parseBrush(color, SolidFill)
    self.forceStyle('backgroundBrush', brush)
    self.update()
