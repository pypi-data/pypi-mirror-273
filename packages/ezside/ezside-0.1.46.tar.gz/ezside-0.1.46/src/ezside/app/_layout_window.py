"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QVBoxLayout
from icecream import ic

from ezside.app import BaseWindow
from ezside.core import AlignTop, AlignLeft
from ezside.widgets import Label, BaseWidget, DigitalClock

ic.configureOutput(includeContext=True, )


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and implements the layout of
  widgets."""

  def __init__(self, *args, **kwargs) -> None:
    """The constructor of the LayoutWindow class."""
    BaseWindow.__init__(self, *args, **kwargs)
    self.baseLayout = QVBoxLayout()
    self.welcomeLabel = Label('LMAO')
    self.clock = DigitalClock()
    self.baseWidget = BaseWidget()

  def initStyle(self) -> None:
    """The initStyle method initializes the style of the window and the
    widgets on it, before 'initUi' sets up the layout. """

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(QSize(640, 480))
    self.baseWidget.__debug_flag__ = True
    self.baseLayout.setAlignment(AlignTop | AlignLeft)
    self.welcomeLabel.initUi()
    self.baseLayout.addWidget(self.welcomeLabel)
    self.clock.initUi()
    self.baseLayout.addWidget(self.clock)
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)

  @abstractmethod  # MainWindow
  def initSignalSlot(self) -> None:
    """The initActions method initializes the actions of the window."""

  def testPauseButton(self) -> None:
    """Test the pause button."""
    self.mainStatusBar.showMessage('Pause button clicked.', 5000)

  def testResumeButton(self) -> None:
    """Test the resume button."""
    self.mainStatusBar.showMessage('Resume button clicked.', 5000)
