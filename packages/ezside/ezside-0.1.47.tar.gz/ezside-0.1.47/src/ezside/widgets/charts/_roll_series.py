"""RollSeries subclasses the QXYSeries class and provides a FIFO buffered
data series. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time

from PySide6.QtCharts import QScatterSeries


class RollSeries(QScatterSeries):
  """RollData provides a pythonic data structure for a FIFO buffered data."""

  __num_points__ = None
  __fallback_points__ = 1024

  __inner_data__ = []

  def __init__(self, *args, **kwargs) -> None:
    for arg in args:
      if isinstance(arg, int):
        self.__num_points__ = arg
        break
    else:
      self.__num_points__ = self.__fallback_points__
    QScatterSeries.__init__(self)

  def addValue(self, value: float) -> None:
    """Adds the value with a time stamp"""

    self.__inner_data__.append(time.time() + value * 1j)
    while len(self.__inner_data__) > self.__num_points__:
      self.__inner_data__.pop(0)

    rightNow = time.time()
    self.clear()
    for item in self.__inner_data__:
      self.append(item.real - rightNow, item.imag)
