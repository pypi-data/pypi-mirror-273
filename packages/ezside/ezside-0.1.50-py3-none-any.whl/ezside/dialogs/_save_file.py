"""SaveFile provides a descriptor class for creating a file dialog for
save files. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog
from attribox import AbstractDescriptor

from ezside.dialogs import OpenFile

if TYPE_CHECKING:
  from ezside.app import BaseWindow
Shiboken = type(QObject)


class SaveFile(OpenFile):
  """SaveFile provides a descriptor class for creating a file dialog for
  save files. """

  __name_filter__ = None
  __fallback_filter__ = 'All Files (*)'

  def __set_name__(self, owner: type, name: str) -> None:
    """The __set_name__ method is called when the descriptor is assigned to
    a class attribute. """
    AbstractDescriptor.__set_name__(self, owner, name)
    setattr(owner, 'saveFileSelected', Signal(str))

  def _createInstance(self, instance: BaseWindow, owner: Shiboken) -> None:
    """Creates the FileDialog instance. """
    dialog = QFileDialog()
    dialog.setViewMode(QFileDialog.ViewMode.Detail)
    dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
    dialog.setFileMode(QFileDialog.FileMode.AnyFile)
    dialog.setNameFilter(self._getNameFilter())
    dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    dialog.fileSelected.connect(instance.saveFileSelected)
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, dialog)
