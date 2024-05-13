"""RealTimeView provides a widget displaying real time data using the
QChart framework."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCharts import QChartView, QChart
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from ezside.core import AlignBottom, AlignLeft
from ezside.widgets.charts import DataChart


class RealTimeView(QChartView):
  """RealTimeView provides a widget displaying real time data using the
  QChart framework."""

  __inner_chart__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the RealTimeView."""
    self.__inner_chart__ = DataChart(*args, **kwargs)
    self.__inner_chart__.initChart()
    QChartView.__init__(self, self.__inner_chart__)

  def initUi(self) -> None:
    """Initializes the user interface."""
    self.setRenderHint(QPainter.RenderHint.Antialiasing)
    self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    self.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    self.__inner_chart__.legend().setVisible(True)
    self.__inner_chart__.legend().setAlignment(AlignBottom | AlignLeft)
    self.__inner_chart__.legend().setShowToolTips(True)
    self.__inner_chart__.setTheme(QChart.ChartTheme.ChartThemeBrownSand)

  def append(self, value: float) -> None:
    """Append a value to the chart."""
    self.__inner_chart__.append(value)
