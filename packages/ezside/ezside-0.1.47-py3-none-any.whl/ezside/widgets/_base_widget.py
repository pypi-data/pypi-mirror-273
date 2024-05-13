"""BaseWidget provides a common base class for all widgets in the
application."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from PySide6.QtWidgets import QWidget
from icecream import ic
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class BaseWidget(QWidget):
  """BaseWidget provides a common base class for all widgets in the
  application."""

  __style_id__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the BaseWidget.
    Please note that BaseWidget will look for keyword arguments to set the
    styleId, at the following names:
      - 'styleId'
      - 'style'
      - 'id'
    The default styleId is 'normal'. """
    for arg in args:
      if isinstance(arg, QWidget):
        QWidget.__init__(self, arg)
    else:
      QWidget.__init__(self)
    styleKeys = ['styleId', 'style', 'id', ]
    for key in styleKeys:
      if key in kwargs:
        self.__style_id__ = kwargs[key]
        break
    else:
      self.__style_id__ = 'normal'

  @abstractmethod
  def initUi(self, ) -> None:
    """Initializes the user interface for the widget. This is where
    subclasses should organize nested widgets and layouts. Standalone
    widgets may return an empty reimplementation. """

  @abstractmethod
  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the widget. Subclasses
    with nested widgets and internal signal and slot logic, should
    implement this method to organize these. This method is invoked only
    after initUi, so the reimplementation may rely on widgets instantiated
    during initUi to be available. All external signals and slots, must be
    ready before this method returns. If not needed, implement an empty
    method."""

  @classmethod
  @abstractmethod
  def styleTypes(cls) -> dict[str, type]:
    """Subclasses are required to implement this method,
    the 'staticStyles' method and the 'dynStyles' method. This method
    should provide the type expected at each name. The 'staticStyles'
    method should return fallback values for the styles. Please note that
    these are defined on the class level, meaning that these are not
    sensitive to the instance state. Finally, the 'dynStyles' provides
    the styles that are sensitive to the instance state. Styles not
    sensitive to the instance state, should be defined in the
    'staticStyles' method."""

  @classmethod
  @abstractmethod
  def staticStyles(cls, ) -> dict[str, Any]:
    """Returns the static styles for the widget. """

  @abstractmethod
  def dynStyles(self, ) -> dict[str, Any]:
    """Returns the dynamic styles for the widget."""

  def getId(self, ) -> str:
    """Returns the styleId given to this widget at instantiation time.
    Subclasses may use this value in the 'dynStyles' method to let some
    styles depend on the styleId. By default, the styleId is 'normal'. """
    return self.__style_id__ or 'normal'

  def getStyle(self, name: str) -> Any:
    """Returns the style value for the given style name. """
    try:
      styleType = (self.styleTypes() or {}).get(name, None)
      staticValue = (self.staticStyles() or {}).get(name, None)
      dynamicValue = (self.dynStyles() or {}).get(name, None)
    except Exception as exception:
      print(self.__class__.__name__)
      print(self.staticStyles)
      print(exception)
      raise SystemExit from exception
    if styleType is None:
      e = """The styleType at key: '%s' is not defined by the current 
      class: '%s'!""" % (name, self.__class__.__name__)
      raise ValueError(monoSpace(e))
    if not isinstance(staticValue, styleType):
      e = typeMsg('staticValue', staticValue, styleType)
      e2 = """When attempting to retrieve style at key: '%s' from widget 
      class: '%s', the following error was encountered: \n'%s'!"""
      raise TypeError(monoSpace(e2 % (name, self.__class__.__name__, e)))
    if dynamicValue is None:
      return staticValue
    if isinstance(dynamicValue, styleType):
      if isinstance(dynamicValue, styleType):
        return dynamicValue
    e = typeMsg('dynamicValue', dynamicValue, styleType)
    raise TypeError(e)
