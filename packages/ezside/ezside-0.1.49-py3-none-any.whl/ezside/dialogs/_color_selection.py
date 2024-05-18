"""ColorSelection provides a dialog window for selecting a color."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QColorDialog, QWidget
from attribox import AbstractDescriptor
from icecream import ic
from vistutils.waitaminute import typeMsg

from ezside.core import QtRGB

if TYPE_CHECKING:
  from ezside.app import BaseWindow
Shiboken = type(QObject)

ic.configureOutput(includeContext=True)


class ColorSelection(QObject, AbstractDescriptor):
  """_ColorDialog provides a dialog window for selecting a color."""

  def __set_name__(self, owner: Shiboken, name: str) -> None:
    """Expands the parent method by setting a signal on the owner."""
    AbstractDescriptor.__set_name__(self, owner, name)
    setattr(owner, 'colorSelected', Signal(QColor))

  def _createInstance(self, instance: BaseWindow, owner: Shiboken) -> None:
    """Create the instance."""
    dialog = QColorDialog(instance)
    dialog.setOption(QtRGB, )
    dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel)
    dialog.colorSelected.connect(instance.colorSelected)
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, dialog)

  def __instance_get__(self,
                       instance: BaseWindow,
                       owner: Shiboken,
                       **kwargs) -> Any:
    """Get the instance."""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createInstance(instance, owner)
      return self.__instance_get__(instance, owner, _recursion=True)
    dialog = getattr(instance, pvtName)
    if isinstance(dialog, QColorDialog):
      return dialog
    e = typeMsg('dialog', dialog, QColorDialog)
    raise TypeError(e)
