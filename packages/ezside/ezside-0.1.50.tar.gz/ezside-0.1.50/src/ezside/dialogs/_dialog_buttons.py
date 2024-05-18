"""DialogButtons class providing a single widget containing the common
button types for dialogs. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout
from attribox import AttriBox

from ezside.core import AlignLeft, Tight
from ezside.widgets import PushButton, CanvasWidget
from moreattribox import Flag


class DialogButtons(CanvasWidget):
  """DialogButtons class providing a single widget containing the common
  button types for dialogs. """

  __is_initialized__ = None

  __include_buttons__ = None
  __fallback_buttons__ = ['accept', 'reject', ]
  __init_signals__ = None
  __init_slots__ = None

  acceptFlag = Flag(True)
  cancelFlag = Flag(True)
  resetFlag = Flag(True)
  applyFlag = Flag(True)
  helpFlag = Flag(True)

  baseLayout = AttriBox[QHBoxLayout]()
  acceptButton = AttriBox[PushButton]('OK')
  cancelButton = AttriBox[PushButton]('Cancel')
  resetButton = AttriBox[PushButton]('Clear')
  applyButton = AttriBox[PushButton]('Apply')
  helpButton = AttriBox[PushButton]('Help')

  accepted = Signal()
  rejected = Signal()
  resetRequested = Signal()
  applyRequested = Signal()
  helpRequested = Signal()

  def initUi(self, ) -> None:
    """Initializes the user interface for the widget. """
    self.setSizePolicy(Tight, Tight)
    self.baseLayout.setSpacing(0)
    self.baseLayout.setContentsMargins(1, 1, 1, 1, )
    self.baseLayout.setAlignment(AlignLeft)
    if self.acceptFlag:
      self.acceptButton.initUi()
      self.acceptButton.initSignalSlot()
      self.baseLayout.addWidget(self.acceptButton)
    if self.cancelFlag:
      self.cancelButton.initUi()
      self.cancelButton.initSignalSlot()
      self.baseLayout.addWidget(self.cancelButton)
    if self.resetFlag:
      self.resetButton.initUi()
      self.resetButton.initSignalSlot()
      self.baseLayout.addWidget(self.resetButton)
    if self.applyFlag:
      self.applyButton.initUi()
      self.applyButton.initSignalSlot()
      self.baseLayout.addWidget(self.applyButton)
    if self.helpFlag:
      self.helpButton.initUi()
      self.helpButton.initSignalSlot()
      self.baseLayout.addWidget(self.helpButton)
    self.setLayout(self.baseLayout)

  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the widget. """
    if self.__is_initialized__:
      return
    self.__is_initialized__ = True
    self.acceptButton.singleLeft.connect(self.accepted)
    self.cancelButton.singleLeft.connect(self.rejected)
    self.resetButton.singleLeft.connect(self.resetRequested)
    self.applyButton.singleLeft.connect(self.applyRequested)
    self.helpButton.singleLeft.connect(self.helpRequested)
