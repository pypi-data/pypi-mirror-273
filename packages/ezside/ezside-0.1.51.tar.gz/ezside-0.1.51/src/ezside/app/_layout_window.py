"""LayoutWindow subclasses BaseWindow and implements the layout of
widgets."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QVBoxLayout, QWidget
from attribox import AttriBox
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
from ezside.widgets.charts import RealTimeView

ic.configureOutput(includeContext=True, )


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and implements the layout of
  widgets."""

  confirmBox = ConfirmBox()

  baseLayout = AttriBox[QVBoxLayout]()
  baseWidget = AttriBox[BaseWidget]()
  titleWidget = AttriBox[Label]('EZSide title', id='title')
  liveChart = AttriBox[RealTimeView]()

  def initStyle(self) -> None:
    """The initStyle method initializes the style of the window and the
    widgets on it, before 'initUi' sets up the layout. """

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.baseLayout.setSpacing(2)
    self.baseLayout.setContentsMargins(0, 0, 0, 0)
    self.titleWidget.initUi()
    self.baseLayout.addWidget(self.titleWidget)
    self.liveChart.initUi()
    self.baseLayout.addWidget(self.liveChart)
    self.baseWidget.initUi()
    self.baseWidget.setLayout(self.baseLayout)
    self.setCentralWidget(self.baseWidget)

  @abstractmethod  # MainWindow
  def initSignalSlot(self) -> None:
    """The initActions method initializes the actions of the window."""
