"""DigitalClock widget uses the SevenSegmentDigit class to display the
current time in a digital clock format. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from datetime import datetime
from typing import Any

from PySide6.QtGui import QColor, QBrush, QPen
from icecream import ic
from PySide6.QtCore import Slot, QPoint, QMargins
from PySide6.QtWidgets import QHBoxLayout

from ezside.core import AlignTop, \
  AlignLeft, \
  AlignFlag, \
  AlignVCenter, \
  parseBrush, SolidFill
from ezside.core import AlignHCenter
from ezside.widgets import BaseWidget, SevenSegmentDigit, CanvasWidget
from ezside.widgets import ColonDisplay

ic.configureOutput(includeContext=True)


class DigitalClock(CanvasWidget):
  """DigitalClock widget uses the SevenSegmentDigit class to display the
  current time in a digital clock format. """

  @classmethod
  def staticStyles(cls) -> dict[str, Any]:
    """The registerFields method registers the fields of the widget.
    Please note, that subclasses can reimplement this method, but must
    provide these same fields. """
    backgroundBrush = parseBrush(QColor(223, 223, 223, 255), SolidFill)
    borderBrush = parseBrush(QColor(223, 223, 223, 255), SolidFill)
    return {
      'margins'        : QMargins(0, 0, 0, 0, ),
      'borders'        : QMargins(2, 2, 2, 2, ),
      'paddings'       : QMargins(0, 0, 0, 0, ),
      'borderBrush'    : borderBrush,
      'backgroundBrush': backgroundBrush,
      'radius'         : QPoint(2, 2, ),
      'vAlign'         : AlignVCenter,
      'hAlign'         : AlignHCenter,
    }

  @classmethod
  def styleTypes(cls) -> dict[str, type]:
    """The styleTypes method provides the type expected at each name. """
    canvasWidgetStyles = CanvasWidget.styleTypes()
    digitalClockStyles = {
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
      'vAlign'         : int,
      'hAlign'         : int,
      'aspect'         : float,
      'spacing'        : int,
    }
    return {**canvasWidgetStyles, **digitalClockStyles}

  def dynStyles(self) -> list[str]:
    """The dynStyles method provides the dynamic styles of the widget."""

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the DigitalClock widget."""
    super().__init__(*args, **kwargs)
    self.baseLayout = QHBoxLayout()
    self.baseLayout.setContentsMargins(1, 0, 1, 0, )
    self.baseLayout.setSpacing(0)
    styleId = self.getId()
    self.hoursTens = SevenSegmentDigit(id=styleId)
    self.hours = SevenSegmentDigit(id=styleId)
    self.colon1 = ColonDisplay(id=styleId)
    self.minutesTens = SevenSegmentDigit(id=styleId)
    self.minutes = SevenSegmentDigit(id=styleId)
    self.colon2 = ColonDisplay(id=styleId)
    self.secondsTens = SevenSegmentDigit(id=styleId)
    self.seconds = SevenSegmentDigit(id=styleId)
    self.initUi()

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the widget."""
    # self.setSizePolicy(Tight, Prefer)
    self.baseLayout.setAlignment(AlignTop | AlignLeft)
    self.baseLayout.addWidget(self.hoursTens, )
    self.hoursTens.initUi()
    self.baseLayout.addWidget(self.hours, )
    self.hours.initUi()
    self.baseLayout.addWidget(self.colon1, )
    self.colon1.initUi()
    self.baseLayout.addWidget(self.minutesTens, )
    self.minutesTens.initUi()
    self.baseLayout.addWidget(self.minutes, )
    self.minutes.initUi()
    self.baseLayout.addWidget(self.colon2, )
    self.colon2.initUi()
    self.baseLayout.addWidget(self.secondsTens, )
    self.secondsTens.initUi()
    self.baseLayout.addWidget(self.seconds, )
    self.seconds.initUi()
    self.setLayout(self.baseLayout)

  def initSignalSlot(self) -> None:
    """The initSignalSlot method initializes the signal and slot connections
    of the widget."""

  @Slot()
  def refresh(self) -> None:
    """The refresh method refreshes the widget."""
    self.update()

  def update(self) -> None:
    """Checks if the inner value of the widget is different from the
    displayed value and changes before applying parent update."""
    rightNow = datetime.now()
    s, S = int(rightNow.second % 10), int(rightNow.second // 10)
    m, M = int(rightNow.minute % 10), int(rightNow.minute // 10)
    h, H = int(rightNow.hour % 10), int(rightNow.hour // 10)
    self.hoursTens.setInnerValue(H)
    self.hours.setInnerValue(h)
    self.minutesTens.setInnerValue(M)
    self.minutes.setInnerValue(m)
    self.secondsTens.setInnerValue(S)
    self.seconds.setInnerValue(s)
    BaseWidget.update(self)
