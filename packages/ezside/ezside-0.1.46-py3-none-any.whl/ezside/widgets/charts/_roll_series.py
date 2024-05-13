"""RollSeries subclasses the QXYSeries class and provides a FIFO buffered
data series. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import time

from PySide6.QtCharts import QScatterSeries
from PySide6.QtCore import QPointF
import numpy as np
from vistutils.parse import maybe


class RollSeries(QScatterSeries):
  """RollSeries subclasses the QXYSeries class and provides a FIFO buffered
  data series. """

  __num_points__ = None
  __fallback_num__ = 1024
  __max_age__ = None
  __fallback_age__ = 120

  __inner_array__ = None
  __current_index__ = 0

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the RollSeries instance."""
    num, age = None, None
    for arg in args:
      if isinstance(arg, int):
        if num is None:
          num = arg
        elif age is None:
          age = arg
          break
    else:
      self.__num_points__ = maybe(num, self.__fallback_num__)
      self.__max_age__ = maybe(age, self.__fallback_age__)
    QScatterSeries.__init__(self)
    self.__inner_array__ = np.empty((self.__num_points__, 1),
                                    dtype=np.complex64)
    self.__inner_array__.fill(np.nan)

  def append(self, *args) -> None:
    """Reimplementation of the append method accepts only single floating
    point values. """
    value = time.time() + float([*args, None][0]) * 1j
    self.__inner_array__[self.__current_index__] = value
    self.__current_index__ += 1
    self.__current_index__ %= self.__num_points__

  def points(self, ) -> list[QPointF]:
    """Returns the points in the series."""
    data = [c for c in self.__inner_array__ if c == c]
    now = time.time()
    return [QPointF(c.real - now, c.imag) for c in data]
