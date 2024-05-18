"""UserInt subclasses AbstractUserInput and provides an input dialog for
received integer values from the user."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

from ezside.dialogs import AbstractUserInput, IntDialogWindow

if TYPE_CHECKING:
  from ezside.app import BaseWindow

Shiboken = type(QObject)


class UserInt(AbstractUserInput):
  """UserInt subclasses AbstractUserInput and provides an input dialog for
  received integer values from the user."""

  def _getSignal(self, ) -> Signal:
    """Getter-function for the signal instance that will be owned by the
    BaseWindow class. """
    return Signal(int)

  def _getSignalName(self, ) -> str:
    """Getter-function for the name the signal attribute should appear in
    the BaseWindow class. """
    return 'intSelected'

  def _createInstance(self, instance: BaseWindow, owner: Shiboken) -> None:
    """Creator-function for the input dialog. """
    dialog = IntDialogWindow()
    signalName = self._getSignalName()
    dialog.valueSelected.connect(getattr(instance, signalName))
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, dialog)
