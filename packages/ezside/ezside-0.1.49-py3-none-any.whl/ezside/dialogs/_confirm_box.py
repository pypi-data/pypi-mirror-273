"""ConfirmBox provides a confirmation dialog box that may be placed
between a slot and a signal requiring confirmation. For example:

  source.connect.self.confirmBox(target)

When the source signals the target, an instance of ConfirmBox will open,
and its accepted signal will be connected to the target. User interaction
is then required to invoke target slot. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Callable, Never, TYPE_CHECKING

from PySide6.QtCore import QCoreApplication, QObject
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QDialog, QWidget, QGridLayout
from attribox import AttriBox
from icecream import ic
from vistutils.parse import maybe
from vistutils.waitaminute import typeMsg

from ezside.core import parseFont, Normal, AlignHCenter
from ezside.widgets import BaseWidget, PushButton, Label

if TYPE_CHECKING:
  from ezside.app import App, AppSettings


class _ConfirmDialog(QDialog):
  """_ConfirmDialog provides a dialog box for ConfirmBox instances."""

  __user_question__ = None
  __fallback_question__ = """Please confirm!"""
  __target_slot__ = None

  windowTitle = AttriBox[str]()

  def __init__(self, callMeMaybe: Callable, parent: QWidget, *args) -> None:
    """Initialize the _ConfirmDialog."""
    QDialog.__init__(self, parent)
    self.__target_slot__ = callMeMaybe
    for arg in args:
      if isinstance(arg, str):
        self._setUserQuestion(arg)
        break
    else:
      self._setUserQuestion(self.__fallback_question__)
    self.baseLayout = QGridLayout()
    self.baseWidget = BaseWidget()
    self.questionLabel = Label()
    self.acceptButton = PushButton('Accept')
    self.rejectButton = PushButton('Reject')

  def _setUserQuestion(self, question: str) -> None:
    """Set the user question."""
    if self.__user_question__ is not None:
      e = """User question is already set!"""
      raise AttributeError(e)
    if not isinstance(question, str):
      e = typeMsg('question', question, str)
      raise TypeError(e)
    self.__user_question__ = question

  def _getUserQuestion(self) -> str:
    """Get the user question."""
    return self.__user_question__

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.setWindowTitle(self.windowTitle)
    app = QCoreApplication.instance()
    if TYPE_CHECKING:
      assert isinstance(app, App)
    settings = app.getSettings()
    if TYPE_CHECKING:
      assert isinstance(app, AppSettings)
    self.setWindowIcon(settings.value('/icon/confirm'))
    metrics = QFontMetrics(parseFont('Montserrat', 12, Normal))
    titleWidth = metrics.boundingRect(self.windowTitle).width()
    self.setMinimumWidth(titleWidth + 96)
    self.questionLabel.text = self._getUserQuestion()
    self.questionLabel['hAlign'] = AlignHCenter
    self.questionLabel.initUi()
    self.baseLayout.addWidget(self.questionLabel, 0, 0, 1, 2)
    self.acceptButton.text = 'Confirm'
    self.acceptButton.initUi()
    self.baseLayout.addWidget(self.acceptButton, 1, 0)
    self.rejectButton.text = 'Reject'
    self.rejectButton.initUi()
    self.baseLayout.addWidget(self.rejectButton, 1, 1)
    self.setLayout(self.baseLayout)

  def initSignalSlot(self) -> None:
    """Initialize the signal slot connections."""
    self.acceptButton.singleClick.connect(self.accept)
    self.rejectButton.singleClick.connect(self.reject)
    self.accepted.connect(self.__target_slot__)

  def show(self) -> None:
    """Show the dialog."""
    self.initUi()
    self.initSignalSlot()
    QDialog.show(self)
    ic('_ConfirmDialog.show')


class ConfirmBox(QObject):
  """ConfirmBox provides a confirmation dialog box that may be placed
  between a slot and a signal requiring confirmation. For example:

    source.connect.self.confirmBox(target)

  When the source signals the target, an instance of ConfirmBox will open,
  and its accepted signal will be connected to the target. User interaction
  is then required to invoke target slot. """

  __target_slot__ = None
  __field_name__ = None
  __field_owner__ = None
  __pos_args__ = None

  def __get__(self, instance: QWidget, owner: type) -> Any:
    """Get the instance of ConfirmBox."""
    if instance is None:
      return self
    ic('__get__')

    args = maybe(self.__pos_args__, [])

    def callMeMaybe(targetSlot) -> Callable:
      """Factory function returning the creator function for the dialog"""

      def createDialog() -> None:
        """Create the dialog."""
        ic('createDialog')
        dialog = _ConfirmDialog(targetSlot, instance, *args)
        clsName = self.getFieldOwner().__name__
        field = self.getFieldName()
        dialog.windowTitle = 'Please Confirm!  %s.%s' % (clsName, field)
        dialog.show()

      return createDialog

    return callMeMaybe

  def __set__(self, *_) -> Never:
    """Illegal setter function"""
    e = """ConfirmBox instances are read-only!"""
    raise TypeError(e)

  def __delete__(self, *_) -> Never:
    """Illegal deleter function"""
    e = """ConfirmBox instances are read-only!"""
    raise TypeError(e)

  def __set_name__(self, owner: type, name: str):
    """Set the name of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def getFieldName(self) -> str:
    """Get the field name."""
    return self.__field_name__

  def getFieldOwner(self) -> type:
    """Get the field owner."""
    return self.__field_owner__
