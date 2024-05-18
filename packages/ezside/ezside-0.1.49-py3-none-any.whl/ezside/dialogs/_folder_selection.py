"""FolderSelection provides a descriptor class for creating file dialogs
for selecting folders. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Self

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog
from attribox import AbstractDescriptor
from vistutils.waitaminute import typeMsg

if TYPE_CHECKING:
  from ezside.app import BaseWindow
Shiboken = type(QObject)


class FolderSelection(QObject, AbstractDescriptor):
  """FolderSelection provides a descriptor class for creating file dialogs
  for selecting folders. """

  def __set_name__(self, owner: type, name: str) -> None:
    """The __set_name__ method is called when the descriptor is assigned to
    a class attribute. """
    AbstractDescriptor.__set_name__(self, owner, name)
    setattr(owner, 'folderSelected', Signal(str))

  def _createInstance(self, instance: BaseWindow, owner: Shiboken) -> None:
    """Creates the FileDialog instance. """
    dialog = QFileDialog()
    dialog.setViewMode(QFileDialog.ViewMode.Detail)
    dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
    dialog.setOption(QFileDialog.Option.ShowDirsOnly)
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
    dialog.fileSelected.connect(instance.folderSelected)
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, dialog)

  def __instance_get__(self,
                       instance: BaseWindow,
                       owner: Shiboken,
                       **kwargs) -> QFileDialog | Self:
    """The __instance_get__ method is called when the descriptor is accessed
    via the owning instance. """
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      self._createInstance(instance, owner)
    dialog = getattr(instance, pvtName)
    if isinstance(dialog, QFileDialog):
      return dialog
    e = typeMsg('dialog', dialog, QFileDialog)
    raise TypeError(e)
