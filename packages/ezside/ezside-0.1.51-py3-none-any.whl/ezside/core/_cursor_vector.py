"""CursorVector encapsulates the movement of a single point cursor,
typically the mouse cursor. It provides positional properties defined by
the horizontal and vertical movements of the cursor during the time given
by the time property. Since the movement of the cursor is relative to
itself, the coordinates are not bound to a particular viewport, but is
scaled according to the widget emitting it.

  t: float movement duration in seconds
  x: float horizontal movement in pixels
  y: float vertical movement in pixels

Based on the above, the following properties are inferred:

  vx: float horizontal velocity in pixels per second
  vy: float vertical velocity in pixels per second
  v: float total velocity in pixels per second
  ax: float horizontal acceleration in pixels per second squared
  ay: float vertical acceleration in pixels per second squared
  a: float total acceleration in pixels per second squared"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from PySide6.QtCore import QPointF, QPoint, QTimer
from PySide6.QtGui import QMouseEvent
from attribox import AttriBox
from vistutils.fields import EmptyField
from vistutils.parse import maybe


class CursorVector:
  """CursorVector encapsulates the movement of a single point cursor,
  typically the mouse cursor. It provides positional properties defined by
  the horizontal and vertical movements of the cursor during the time given
  by the time property. Since the movement of the cursor is relative to
  itself, the coordinates are not bound to a particular viewport, but is
  scaled according to the widget emitting it.

    t: float movement duration in seconds
    x: float horizontal movement in pixels
    y: float vertical movement in pixels

  Based on the above, the following properties are inferred:

    vx: float horizontal velocity in pixels per second
    vy: float vertical velocity in pixels per second
    v: float total velocity in pixels per second
    ax: float horizontal acceleration in pixels per second squared
    ay: float vertical acceleration in pixels per second squared
    a: float total acceleration in pixels per second squared"""

  __fallback_values__ = dict(x=0, y=0, t=1000)
  __inner_horizontal__ = None
  __inner_vertical__ = None
  __inner_time__ = None

  x = AttriBox[int](0)
  y = AttriBox[int](0)
  t = AttriBox[int](1000)

  vx = EmptyField()
  vy = EmptyField()
  v = EmptyField()
  ax = EmptyField()
  ay = EmptyField()
  a = EmptyField()

  @staticmethod
  def _parseInt(*args) -> dict[str, int]:
    """Parse the integer object into a dictionary."""
    intArgs = []
    for arg in args:
      if isinstance(arg, float):
        if arg.is_integer():
          intArgs.append(int(arg))
      elif isinstance(arg, int):
        intArgs.append(arg)
    if len(intArgs) == 1:
      return dict(t=intArgs[0])
    if len(intArgs) == 2:
      return dict(x=intArgs[0], y=intArgs[1])
    if len(intArgs) > 3:
      return dict(x=intArgs[0], y=intArgs[1], t=intArgs[2])

  @staticmethod
  def _parseQTimer(*args) -> dict[str, int]:
    """Parse the QTimer object into a dictionary."""
    for arg in args:
      if isinstance(arg, QTimer):
        return dict(t=arg.interval() - arg.remainingTime())

  @staticmethod
  def _parsePoint(*args) -> dict[str, int]:
    """Parse the QPointF object into a dictionary."""
    pointArgs = []
    for arg in args:
      if isinstance(arg, QPointF):
        arg = arg.toPoint()
      if isinstance(arg, QPoint):
        pointArgs.append(arg)
    if len(pointArgs) == 2:
      dx = pointArgs[1].x() - pointArgs[0].x()
      dy = pointArgs[1].y() - pointArgs[0].y()
      return dict(x=dx, y=dy)

  @classmethod
  def _parseMouseEvent(cls, *args) -> dict[str, int]:
    """Parse the QMouseEvent object into a dictionary."""
    eventArgs = []
    for arg in args:
      if isinstance(arg, QMouseEvent):
        eventArgs.append(arg)
    if len(eventArgs) == 2:
      return cls._parsePoint(eventArgs[0].pos(), eventArgs[1].pos())

  @classmethod
  def _getParsers(cls, ) -> list[Callable]:
    """Getter-function for the parsers."""
    return [cls._parseInt,
            cls._parseQTimer,
            cls._parsePoint,
            cls._parseMouseEvent]

  def __init__(self, *args) -> None:
    """Initialize the CursorVector instance."""
    eventData = self._parseMouseEvent(*args) or {}
    pointData = self._parsePoint(*args) or {}
    intData = self._parseInt(*args) or {}
    timerData = self._parseQTimer(*args) or {}
    fallbackData = self.__fallback_values__
    self.t = timerData.get('t', (intData.get('t', fallbackData.get('t'))))
    spaceData = maybe(eventData, pointData, intData, )
    self.x = spaceData.get('x', fallbackData.get('x'))
    self.y = spaceData.get('y', fallbackData.get('y'))

  @vx.GET
  def _getHorizontalVelocity(self) -> float:
    """Get the horizontal velocity."""
    if self.t:
      return self.x / self.t * 1000
    return 1e06

  @vy.GET
  def _getVerticalVelocity(self) -> float:
    """Get the vertical velocity."""
    if self.t:
      return self.y / self.t * 1000
    return 1e06

  @v.GET
  def _getTotalVelocity(self) -> float:
    """Get the total velocity."""
    if isinstance(self.vx, float) and isinstance(self.vy, float):
      return (self.vx ** 2 + self.vy ** 2) ** 0.5

  @ax.GET
  def _getHorizontalAcceleration(self) -> float:
    """Get the horizontal acceleration."""
    if self.t and isinstance(self.vx, float):
      return self.vx / self.t * 1000
    return 1e06

  @ay.GET
  def _getVerticalAcceleration(self) -> float:
    """Get the vertical acceleration."""
    if self.t and isinstance(self.vy, float):
      return self.vy / self.t * 1000
    return 1e06

  @a.GET
  def _getTotalAcceleration(self) -> float:
    """Get the total acceleration."""
    if isinstance(self.ax, float) and isinstance(self.ay, float):
      return (self.ax ** 2 + self.ay ** 2) ** 0.5

  def __str__(self, ) -> str:
    """Return the string representation of the CursorVector."""
    if isinstance(self.vx, float) and isinstance(self.vy, float):
      return """V(%.3f, %.3f)""" % (self.vx, self.vy)

  def __repr__(self) -> str:
    """Return the code representation of the CursorVector."""
    clsName = self.__class__.__name__
    x, y, t = self.x, self.y, self.t
    return """%s(%d, %d, %d)""" % (clsName, self.x, self.y, self.t)

  def __abs__(self, ) -> float:
    """Return the absolute value of the CursorVector."""
    if isinstance(self.v, float):
      return self.v
