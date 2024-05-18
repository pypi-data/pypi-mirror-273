"""FontSelection provides a descriptor class for the QFontDialog class. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFontDialog, QColorDialog
from PySide6.QtGui import QFont
from attribox import AbstractDescriptor
from vistutils.waitaminute import typeMsg

if TYPE_CHECKING:
  from ezside.app import BaseWindow
Shiboken = type(QObject)


class FontSelection(QObject, AbstractDescriptor):
  """FontSelection provides a descriptor class for the QFontDialog class. """

  def __set_name__(self, owner: Shiboken, name: str) -> None:
    """Expands the parent method by setting a signal on the owner."""
    AbstractDescriptor.__set_name__(self, owner, name)
    setattr(owner, 'fontSelected', Signal(QFont))

  def _createInstance(self, instance: BaseWindow, owner: Shiboken) -> None:
    """Create the font dialog."""
    dialog = QFontDialog()
    dialog.setOption(QFontDialog.FontDialogOption.DontUseNativeDialog)
    dialog.fontSelected.connect(instance.fontSelected)
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, dialog)

  def __instance_get__(self,
                       instance: BaseWindow,
                       owner: Shiboken,
                       **kwargs) -> QFontDialog | Self:
    """Explicit getter-function for the font dialog."""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createInstance(instance, owner)
      return self.__instance_get__(instance, owner, _recursion=True)
    dialog = getattr(instance, pvtName)
    if isinstance(dialog, QFontDialog):
      return dialog
    e = typeMsg('dialog', dialog, QFontDialog)
    raise TypeError(e)
