"""RealTimeView provides a widget displaying real time data using the
QChart framework."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCharts import QChartView, QChart
from PySide6.QtGui import QPainter
from vistutils.parse import maybe

from ezside.core import AlignBottom, AlignLeft, AlignFlag
from ezside.widgets.charts import DataChart


class RealTimeView(QChartView):
  """RealTimeView provides a widget displaying real time data using the
  QChart framework."""

  __inner_chart__ = None
  __align_flags__ = None
  __fallback_align__ = AlignBottom | AlignLeft
  __chart_theme__ = None
  __fallback_theme__ = QChart.ChartTheme.ChartThemeBrownSand

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the RealTimeView."""
    fallbackAlign, chartTheme = None, None
    for arg in args:
      if isinstance(arg, AlignFlag):
        if fallbackAlign is None:
          fallbackAlign = arg
        else:
          fallbackAlign |= arg
      elif isinstance(arg, QChart.ChartTheme):
        chartTheme = arg
    self.__align_flags__ = maybe(fallbackAlign, self.__fallback_align__)
    self.__chart_theme__ = maybe(chartTheme, self.__fallback_theme__)
    self.__inner_chart__ = DataChart(*args, **kwargs)
    self.__inner_chart__.initChart()

    QChartView.__init__(self, self.__inner_chart__)

  def initUi(self) -> None:
    """Initializes the user interface."""
    self.setRenderHint(QPainter.RenderHint.Antialiasing)
    self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    self.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    self.__inner_chart__.legend().setVisible(True)
    self.__inner_chart__.legend().setAlignment(self.__align_flags__)
    self.__inner_chart__.legend().setShowToolTips(True)
    self.__inner_chart__.setTheme(self.__chart_theme__)

  def append(self, value: float) -> None:
    """Append a value to the chart."""
    self.__inner_chart__.append(value)
