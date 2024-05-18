"""Chart provides a base class for the real-time chart widgets."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCharts import QChart, QValueAxis

from ezside.core import AlignBottom, AlignLeft
from ezside.widgets.charts import RollSeries


class DataChart(QChart):
  """Chart provides a base class for the real-time chart widgets."""

  __roll_series__ = None
  __horizontal_axis__ = None
  __vertical_axis__ = None
  __chart_title__ = None
  __fallback_title__ = 'Data Chart'

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the Chart instance."""
    intArgs, posArgs = [], []
    for arg in args:
      if isinstance(arg, int) and len(intArgs) < 2:
        intArgs.append(arg)
      elif isinstance(arg, str) and self.__chart_title__ is None:
        self.__chart_title__ = arg
      else:
        posArgs.append(arg)
    self.__roll_series__ = RollSeries(*intArgs, )
    QChart.__init__(self, *posArgs, **kwargs)
    self.initChart()
    self.initAxis()

  def initChart(self, ) -> None:
    """Initializes the chart."""
    self.__roll_series__.setPointLabelsVisible(False)
    self.addSeries(self.__roll_series__)
    self.setTitle(self.__chart_title__ or self.__fallback_title__)

  def initAxis(self, ) -> None:
    """Initializes the axis."""
    self.__horizontal_axis__ = QValueAxis()
    self.__horizontal_axis__.setRange(-10, 0)  # the most recent 10 seconds
    self.addAxis(self.__horizontal_axis__, AlignBottom)
    self.__vertical_axis__ = QValueAxis()
    self.__vertical_axis__.setRange(-10, 10)  # may require dynamic scaling
    self.addAxis(self.__vertical_axis__, AlignLeft)
    self.__roll_series__.attachAxis(self.__horizontal_axis__)
    self.__roll_series__.attachAxis(self.__vertical_axis__)

  def append(self, value: float) -> None:
    """Append a value to the chart."""
    self.__roll_series__.addValue(value)
