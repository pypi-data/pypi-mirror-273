"""RealTimeView provides a widget displaying real time data using the
QChart framework."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCharts import QChartView, QChart, QValueAxis
from PySide6.QtCore import QPointF, \
  Signal, \
  QPoint, \
  QEvent, \
  Qt, \
  QRect, \
  QSize, \
  QSizeF, QRectF
from PySide6.QtGui import QPainter, \
  QColor, \
  QFont, \
  QMouseEvent, \
  QWheelEvent, \
  QBrush
from PySide6.QtWidgets import QGraphicsRectItem
from icecream import ic
from vistutils.parse import maybe
from vistutils.waitaminute import typeMsg

from ezside.core import AlignBottom, \
  AlignLeft, \
  AlignFlag, \
  parseBrush, \
  SolidFill, parseFont, SHIFT, CTRL
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

  def append(self, value: float) -> None:
    """Append a value to the chart."""
    self.__inner_chart__.append(value)

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
    newVMin = vMin + scroll * f * vSpan
    newVMax = vMax + scroll * f * vSpan
    if event.modifiers() == SHIFT:
      self.chart().axes(Qt.Orientation.Horizontal)[0].setRange(newHMin, hMax)
    if event.modifiers() != CTRL:
      return
    if (vMax - vMouse) ** 2 > (vMouse - vMin) ** 2:
      self.chart().axes(Qt.Orientation.Vertical)[0].setRange(newVMin, vMax)
    elif (vMax - vMouse) ** 2 < (vMouse - vMin) ** 2:
      self.chart().axes(Qt.Orientation.Vertical)[0].setRange(vMin, newVMax)
