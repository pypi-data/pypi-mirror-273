"""AbstractDialogWindow provides a base class for user input dialog windows
that inherit from CanvasWidget. Descriptor classes should create instances of
this class or subclasses of it. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING
from PySide6.QtCore import Signal, QCoreApplication
from PySide6.QtWidgets import QVBoxLayout, QDialog, QHBoxLayout
from attribox import AttriBox
from icecream import ic
from vistutils.parse import maybe

from ezside.core import Tight, AlignTop
from ezside.dialogs import DialogButtons
from ezside.widgets import CanvasWidget, Label, BaseWidget

if TYPE_CHECKING:
  from ezside.app import App, AppSettings

ic.configureOutput(includeContext=True)


class AbstractDialogWindow(QDialog, ):
  """AbstractDialogWindow provides a base class for user input dialog
  windows that inherit from CanvasWidget. Descriptor classes should create
  instances of this class or subclasses of it. """

  valueSelected: Signal

  __is_initialized__ = None

  __fallback_title__ = 'Integer Input Dialog'
  titleText = AttriBox[str]()
  windowText = AttriBox[str]()
  baseLayout = AttriBox[QVBoxLayout]()
  titleBanner = AttriBox[Label](id='title')
  dialogButtons = AttriBox[DialogButtons]()
  contentLayout = AttriBox[QHBoxLayout]()
  contentWidget = AttriBox[BaseWidget]()

  resetRequested = Signal()
  applyRequested = Signal()
  helpRequested = Signal()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the dialog window. """
    QDialog.__init__(self)
    title, windowTitle, icon = None, None, None
    for arg in args:
      if isinstance(arg, str):
        if '/icon/' in arg and icon is None:
          icon = arg
        elif title is None:
          title = arg
        elif windowTitle is None:
          windowTitle = arg
    self.titleText = maybe(title, self.__fallback_title__)
    self.windowText = maybe(windowTitle, self.__fallback_title__)
    icon = maybe(icon, '/icon/lmao')
    app = QCoreApplication.instance()
    if TYPE_CHECKING:
      assert isinstance(app, App)
    settings = app.getSettings()
    if TYPE_CHECKING:
      assert isinstance(settings, AppSettings)
    icon = settings.value(icon)
    self.setWindowIcon(icon)
    self.setWindowTitle(self.windowText)

  @abstractmethod
  def initContent(self) -> None:
    """Subclasses should implement this method and place the necessary
    widgets in the 'contentsLayout'. """

  @abstractmethod
  def connectContent(self) -> None:
    """This method runs after the remaining dialog is initialized.
    Subclasses should implement this method to provide the internal logic."""

  def initUi(self, ) -> None:
    """Initializes the user interface for the widget. """
    self.titleBanner.text = self.titleText
    self.titleBanner.setSizePolicy(Tight, Tight)
    self.titleBanner.initUi()
    self.baseLayout.addWidget(self.titleBanner)
    self.baseLayout.setSpacing(0)
    self.baseLayout.setContentsMargins(1, 1, 1, 1, )
    self.baseLayout.setAlignment(AlignTop)
    self.contentWidget.initUi()
    self.initContent()
    self.contentWidget.setLayout(self.contentLayout)
    self.baseLayout.addWidget(self.contentWidget)
    self.dialogButtons.initUi()
    self.dialogButtons.initSignalSlot()
    self.baseLayout.addWidget(self.dialogButtons)
    self.setLayout(self.baseLayout)
    self.setSizePolicy(Tight, Tight)
    self.adjustSize()

  def initSignalSlot(self) -> None:
    """Initializes the signal-slot connections for the widget. """
    if self.__is_initialized__:
      return
    self.__is_initialized__ = True
    self.dialogButtons.accepted.connect(self.accept)
    self.dialogButtons.rejected.connect(self.reject)
    self.dialogButtons.resetRequested.connect(self.resetRequested)
    self.dialogButtons.applyRequested.connect(self.applyRequested)
    self.dialogButtons.helpRequested.connect(self.helpRequested)
    self.connectContent()

  def show(self) -> None:
    """LMAO"""
    self.initUi()
    self.initSignalSlot()
    QDialog.show(self)
