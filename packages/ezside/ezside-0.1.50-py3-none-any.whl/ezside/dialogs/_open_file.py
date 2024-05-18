"""OpenFile provide a descriptor class for creating an open file dialog. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Self

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog
from attribox import AbstractDescriptor
from vistutils.parse import maybe
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

if TYPE_CHECKING:
  from ezside.app import BaseWindow
Shiboken = type(QObject)


class OpenFile(QObject, AbstractDescriptor):
  """OpenFile provide a descriptor class for creating an open file dialog.
  """

  __name_filter__ = None
  __fallback_filter__ = 'All Files (*)'

  def __init__(self, *args, **kwargs) -> None:
    QObject.__init__(self)
    filterKeys = stringList("""filter, filters, name_filter""")
    for key in filterKeys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, str):
          self._setNameFilter(val)
          break
    else:
      for arg in args:
        if isinstance(arg, str):
          self._setNameFilter(arg)
          break

  def _setNameFilter(self, nameFilter: str) -> None:
    """Set the name filter for the file dialog. """
    self.__name_filter__ = nameFilter

  def _getNameFilter(self, ) -> str:
    """Getter-function for the name filter"""
    return maybe(self.__name_filter__, self.__fallback_filter__)

  def __set_name__(self, owner: type, name: str) -> None:
    """The __set_name__ method is called when the descriptor is assigned to
    a class attribute. """
    AbstractDescriptor.__set_name__(self, owner, name)
    setattr(owner, 'openFileSelected', Signal(str))

  def _createInstance(self, instance: BaseWindow, owner: Shiboken) -> None:
    """Creates the FileDialog instance. """
    dialog = QFileDialog()
    dialog.setViewMode(QFileDialog.ViewMode.Detail)
    dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    dialog.setNameFilter(self._getNameFilter())
    dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
    dialog.fileSelected.connect(instance.openFileSelected)
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
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createInstance(instance, owner)
      return self.__instance_get__(instance, owner, _recursion=True)
    dialog = getattr(instance, pvtName)
    if isinstance(dialog, QFileDialog):
      return dialog
    e = typeMsg('dialog', dialog, QFileDialog)
    raise TypeError(e)
