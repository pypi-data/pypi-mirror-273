"""AbstractUserInput provides an abstract baseclass for descriptors
creating user input dialog boxes.  """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Self

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QDialog
from attribox import AbstractDescriptor
from icecream import ic
from vistutils.waitaminute import typeMsg

if TYPE_CHECKING:
  from ezside.app import BaseWindow
Shiboken = type(QObject)


class AbstractUserInput(QObject, AbstractDescriptor):
  """UserInput provides a descriptor class for user input dialog boxes. """

  def __set_name__(self, owner: Shiboken, name: str) -> None:
    """Expands the parent method by setting a signal on the owner."""
    ic('AbstractUserInput.__set_name__')
    AbstractDescriptor.__set_name__(self, owner, name)
    setattr(owner, self._getSignalName(), self._getSignal())

  @abstractmethod
  def _getSignalName(self, ) -> str:
    """Getter-function for the name the signal attribute should appear in
    the BaseWindow class. Subclasses must implement this method."""

  @abstractmethod
  def _getSignal(self, ) -> Signal:
    """Getter-function for the signal instance that will be owned by the
    BaseWindow class. Subclasses must implement this method to define the
    signal that will emit the user input data."""

  @abstractmethod
  def _createInstance(self, instance: BaseWindow, owner: Shiboken) -> None:
    """Creates the dialog instance. Subclass must implement this method to
    define the dialog window and how the return value should be emitted. """

  def __instance_get__(self,
                       instance: BaseWindow,
                       owner: Shiboken,
                       **kwargs) -> QDialog | Self:
    """Explicit getter-function for the dialog."""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createInstance(instance, owner)
      return self.__instance_get__(instance, owner, _recursion=True)
    dialog = getattr(instance, pvtName)
    if isinstance(dialog, QDialog):
      return dialog
    e = typeMsg('dialog', dialog, QDialog)
    raise TypeError(e)
