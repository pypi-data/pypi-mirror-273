"""IntDialogWindow provides a dialog window received integer values from
the user. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSpinBox
from attribox import AttriBox
from icecream import ic

from ezside.core import Tight, parseFont, Expand
from ezside.dialogs import AbstractDialogWindow
from ezside.widgets import Label

ic.configureOutput(includeContext=True)


class IntDialogWindow(AbstractDialogWindow):
  """IntDialogWindow provides a dialog window received integer values from
  the user. """

  def __init__(self, ) -> None:
    """Initializes the dialog window. """
    self.__is_initialized__ = None
    AbstractDialogWindow.__init__(self)

  spinBox = AttriBox[QSpinBox]()
  label = AttriBox[Label](id='info')

  valueSelected = Signal(int)

  def initContent(self) -> None:
    """Initializes the user interface for the widget. """
    self.setSizePolicy(Expand, Tight)
    self.spinBox.setFont(parseFont('Courier', 16))
    self.spinBox.setSizePolicy(Expand, Tight)
    self.spinBox.setRange(-999999, 999999)
    self.spinBox.setSingleStep(1)
    self.label.initUi()
    self.label.text = """Please provide integer in the spinbox: """
    self.label.setSizePolicy(Tight, Tight)
    self.contentLayout.addWidget(self.label)
    self.contentLayout.addWidget(self.spinBox)
    self.spinBox.adjustSize()

  def connectContent(self) -> None:
    """This method runs after the remaining dialog is initialized. """
    self.accepted.connect(self.emitSpinboxValue)

  def emitSpinboxValue(self) -> None:
    """Emits the spinbox value on the valueSelected signal. """
    self.valueSelected.emit(self.spinBox.value())
