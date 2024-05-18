"""RealTimeView provides a widget displaying real time data using the
QChart framework."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCharts import QChartView, QChart, QValueAxis
from PySide6.QtCore import QPointF, \
  Signal, \
  QPoint, \
  QEvent, \
  Qt, \
  QRect, \
  QSize, \
  QSizeF, QRectF, Slot
from PySide6.QtGui import QPainter, \
  QColor, \
  QFont, \
  QMouseEvent, \
  QWheelEvent, \
  QBrush
from PySide6.QtWidgets import QGraphicsRectItem
from icecream import ic
from vistutils.fields import EmptyField
from vistutils.parse import maybe
from vistutils.waitaminute import typeMsg

from ezside.core import AlignBottom, \
  AlignLeft, \
  AlignFlag, \
  parseBrush, \
  SolidFill, parseFont, SHIFT, CTRL, HORIZONTAL, VERTICAL
from ezside.widgets.charts import DataChart

ic.configureOutput(includeContext=True, )


class RealTimeView(QChartView):
  """RealTimeView provides a widget displaying real time data using the
  QChart framework."""

  __scroll_factor__ = 0.2  # 20% of the span

  __inner_chart__ = None
  __align_flags__ = None
  __fallback_align__ = AlignBottom | AlignLeft
  __chart_theme__ = None
  __fallback_theme__ = QChart.ChartTheme.ChartThemeBrownSand
  __mouse_pos__ = None

  cursorPos = Signal(QPoint)

  title = EmptyField()
  hAxis = EmptyField()
  vAxis = EmptyField()
  hMax = EmptyField()
  hMin = EmptyField()
  vMax = EmptyField()
  vMin = EmptyField()

  @title.GET
  def getTitle(self) -> str:
    """Get the title of the chart."""
    return self.__inner_chart__.title()

  @title.SET
  def setTitle(self, title: str) -> None:
    """Set the title of the chart."""
    self.__inner_chart__.setTitle(title)

  @Slot()
  def append(self, value: float) -> None:
    """Append a value to the chart."""
    self.__inner_chart__.append(value)

  @hMax.SET
  def _setHorizontalMax(self, value: float) -> None:
    """Set the maximum value of the horizontal axis."""
    if TYPE_CHECKING:
      assert isinstance(self.hAxis, QValueAxis)
    self.hAxis.setMax(value)

  @hMin.SET
  def _setHorizontalMin(self, value: float) -> None:
    """Set the minimum value of the horizontal axis."""
    if TYPE_CHECKING:
      assert isinstance(self.hAxis, QValueAxis)
    self.hAxis.setMin(value)

  @vMax.SET
  def _setVerticalMax(self, value: float) -> None:
    """Set the maximum value of the vertical axis."""
    if TYPE_CHECKING:
      assert isinstance(self.vAxis, QValueAxis)
    self.vAxis.setMax(value)

  @vMin.SET
  def _setVerticalMin(self, value: float) -> None:
    """Set the minimum value of the vertical axis."""
    if TYPE_CHECKING:
      assert isinstance(self.vAxis, QValueAxis)
    self.vAxis.setMin(value)

  @hMax.GET
  def _getHorizontalMax(self) -> float:
    """Get the maximum value of the horizontal axis."""
    if TYPE_CHECKING:
      assert isinstance(self.hAxis, QValueAxis)
    return self.hAxis.max()

  @hMin.GET
  def _getHorizontalMin(self) -> float:
    """Get the minimum value of the horizontal axis."""
    if TYPE_CHECKING:
      assert isinstance(self.hAxis, QValueAxis)
    return self.hAxis.min()

  @vMax.GET
  def _getVerticalMax(self) -> float:
    """Get the maximum value of the vertical axis."""
    if TYPE_CHECKING:
      assert isinstance(self.vAxis, QValueAxis)
    return self.vAxis.max()

  @vMin.GET
  def _getVerticalMin(self) -> float:
    """Get the minimum value of the vertical axis."""
    if TYPE_CHECKING:
      assert isinstance(self.vAxis, QValueAxis)
    return self.vAxis.min()

  @hAxis.GET
  def _getHorizontalAxis(self) -> QValueAxis:
    """Get the horizontal axis."""
    axis = self.__inner_chart__.axes(Qt.Orientation.Horizontal)[0]
    if isinstance(axis, QValueAxis):
      return axis
    e = typeMsg('axis', axis, QValueAxis)
    raise TypeError(e)

  @vAxis.GET
  def _getVerticalAxis(self) -> QValueAxis:
    """Get the vertical axis."""
    axis = self.__inner_chart__.axes(Qt.Orientation.Vertical)[0]
    if isinstance(axis, QValueAxis):
      return axis
    e = typeMsg('axis', axis, QValueAxis)
    raise TypeError(e)

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the RealTimeView."""
    fallbackAlign, chartTheme, title = None, None, None
    for arg in args:
      if isinstance(arg, AlignFlag):
        if fallbackAlign is None:
          fallbackAlign = arg
        else:
          fallbackAlign |= arg
      elif isinstance(arg, QChart.ChartTheme):
        chartTheme = arg
      elif isinstance(arg, str) and title is None:
        title = arg

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
    self.__inner_chart__.legend().setVisible(False)
    self.__inner_chart__.setTheme(self.__chart_theme__)
    titleBrush = parseBrush(QColor(63, 0, 0), SolidFill)
    titleFont = parseFont(
      'Montserrat', 16, QFont.Capitalization.Capitalize, )
    self.__inner_chart__.setTitleBrush(titleBrush)
    self.__inner_chart__.setTitleFont(titleFont)

  def initSignalSlot(self) -> None:
    """Initializes the signal-slot connections."""

  def overLay(self, rect: QRect, brush: QBrush = None) -> None:
    """Overlay a value to the chart."""
    topLeft = self.chart().mapToPosition(rect.topLeft())
    bottomRight = self.chart().mapToPosition(rect.bottomRight())
    width = bottomRight.x() - topLeft.x()
    height = bottomRight.y() - topLeft.y()
    size = QSizeF(width, height)
    rect = QGraphicsRectItem(QRectF(topLeft, size))
    brush = maybe(brush, parseBrush(QColor(255, 0, 0, 47), SolidFill))
    rect.setBrush(brush)
    self.chart().scene().addItem(rect)

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Mouse press event."""
    QChartView.mousePressEvent(self, event)

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Mouse release event."""
    QChartView.mouseReleaseEvent(self, event)

  def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Mouse move event."""
    QChartView.mouseMoveEvent(self, event)
    self.cursorPos.emit(event.pos())
    self.__mouse_pos__ = event.pos()

  def wheelEvent(self, event: QWheelEvent) -> None:
    """Wheel event."""
    QChartView.wheelEvent(self, event)
    scroll = 1 if event.angleDelta().y() > 0 else -1
    pixelPos = self.chart().mapToValue(self.__mouse_pos__)
    vMouse, hMouse = pixelPos.y(), pixelPos.x()
    vAxis = self.chart().axes(Qt.Orientation.Vertical)[0]
    hAxis = self.chart().axes(Qt.Orientation.Horizontal)[0]
    if not isinstance(vAxis, QValueAxis):
      e = typeMsg('vAxis', vAxis, QValueAxis)
      raise TypeError(e)
    if not isinstance(hAxis, QValueAxis):
      e = typeMsg('hAxis', hAxis, QValueAxis)
      raise TypeError(e)
    vMax, vMin = vAxis.max(), vAxis.min()
    hMax, hMin = hAxis.max(), hAxis.min()
    hSpan, vSpan = hMax - hMin, vMax - vMin
    f = self.__scroll_factor__
    newHMin = hMin + scroll * f * hSpan
    newHMax = hMax + scroll * f * hSpan
    newVMin = vMin + scroll * f * vSpan
    newVMax = vMax + scroll * f * vSpan
    if event.modifiers() == SHIFT:
      if (hMax - hMouse) ** 2 > (hMouse - hMin) ** 2:
        self.chart().axes(HORIZONTAL)[0].setRange(newHMin, hMax)
      if (hMax - hMouse) ** 2 < (hMouse - hMin) ** 2:
        self.chart().axes(HORIZONTAL)[0].setRange(hMin, newHMax)
    if event.modifiers() != CTRL:
      return
    if (vMax - vMouse) ** 2 > (vMouse - vMin) ** 2:
      self.chart().axes(VERTICAL)[0].setRange(newVMin, vMax)
    elif (vMax - vMouse) ** 2 < (vMouse - vMin) ** 2:
      self.chart().axes(VERTICAL)[0].setRange(vMin, newVMax)
