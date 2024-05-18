"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QVBoxLayout, QWidget
from icecream import ic

from ezside import TestCanvas
from ezside.app import BaseWindow
from ezside.core import AlignTop, AlignLeft
from ezside.dialogs import ConfirmBox
from ezside.widgets import BaseWidget, \
  Label, \
  PushButton, \
  CheckButton, \
  VerticalSlider
from ezside.widgets import HorizontalSlider

ic.configureOutput(includeContext=True, )


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and implements the layout of
  widgets."""

  confirmBox = ConfirmBox()

  def __init__(self, *args, **kwargs) -> None:
    """The constructor of the LayoutWindow class."""
    BaseWindow.__init__(self, *args, **kwargs)
    self.baseLayout = QVBoxLayout()
    self.baseWidget = BaseWidget()
    self.titleWidget = Label('Title', id='title')
    self.headerWidget = Label('Header', id='header')
    self.buttonWidget = PushButton('Click Me', )
    self.slider = VerticalSlider()
    self.positionIndicator = Label('Position', id='info')
    self.tester = TestCanvas()

  def initStyle(self) -> None:
    """The initStyle method initializes the style of the window and the
    widgets on it, before 'initUi' sets up the layout. """

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.baseWidget.__debug_flag__ = True
    self.baseLayout.setAlignment(AlignTop | AlignLeft)
    self.baseLayout.addWidget(self.titleWidget)
    self.baseLayout.addWidget(self.headerWidget)
    self.buttonWidget.initUi()
    self.baseLayout.addWidget(self.buttonWidget)
    self.slider.setFixedSize(QSize(48, 256))
    self.slider.initUi()
    self.baseLayout.addWidget(self.slider)
    self.positionIndicator.initUi()
    self.baseLayout.addWidget(self.positionIndicator)
    self.slider.positionChanged.connect(self.positionIndicator.echo)
    self.tester.setMinimumSize(64, 64)
    self.tester.initUi()
    self.baseLayout.addWidget(self.tester)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)
    QWidget.setTabOrder(self.slider, self.buttonWidget, )

  @abstractmethod  # MainWindow
  def initSignalSlot(self) -> None:
    """The initActions method initializes the actions of the window."""
