"""BaseWidget provides a common base class for all widgets in the
application."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QWidget
from icecream import ic

if TYPE_CHECKING:
  from ezside.app import AppSettings, App

ic.configureOutput(includeContext=True)


class BaseWidget(QWidget):
  """BaseWidget provides a common base class for all widgets in the
  application."""

  __style_id__ = None
  __forced_styles__ = None

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
    self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

  def _getForcedStyle(self, name: str) -> Any:
    """Getter-function for forced styles."""
    return (self.__forced_styles__ or {}).get(name, None)

  def __setitem__(self, name: str, styleVal: Any) -> None:
    """Alias for forceStyle"""
    self.__forced_styles__ = {**(self.__forced_styles__ or {}),
                              name: styleVal}

  def initUi(self, ) -> None:
    """Initializes the user interface for the widget. This is where
    subclasses should organize nested widgets and layouts. Standalone
    widgets may return an empty reimplementation. """

  def initSignalSlot(self) -> None:
    """Initializes the signal/slot connections for the widget. Subclasses
    with nested widgets and internal signal and slot logic, should
    implement this method to organize these. This method is invoked only
    after initUi, so the reimplementation may rely on widgets instantiated
    during initUi to be available. All external signals and slots, must be
    ready before this method returns. If not needed, implement an empty
    method."""

  @classmethod
  def typeGuard(cls, name: str, value: Any) -> Any:
    """Subclasses can reimplement this method to provide fine control of
    the allowable types for the style values. If the name is not
    recognized, this method should return 'None'. In this case, the type
    check compares against the type of the fallback style. If the name is
    recognized and the given value is not of acceptable type, this method
    must raise a TypeError. This method is ignored unless it raises an
    error. """

  @classmethod
  def fallbackStyles(cls, name: str) -> Any:
    """Subclasses are required to implement this method for every style
    name. It should provide the single fallback value that is insensitive
    to instance state and id. """

  def defaultStyles(self, name: str) -> Any:
    """Subclasses may implement this method to provide id and state based
    styles at the given name. This method is attempted if the AppSettings
    class does not provide a value. If a name is not recognized,
    this method should return 'None'. """

  def getState(self) -> str:
    """Getter-function for the state of the widget. Classes should
    implement this method to implement state awareness. """
    return 'base'

  def getId(self, ) -> str:
    """Returns the styleId given to this widget at instantiation time.
    Subclasses may use this value in the 'dynStyles' method to let some
    styles depend on the styleId. By default, the styleId is 'normal'. """
    return self.__style_id__

  def forceStyle(self, name: str, value: Any) -> None:
    """Forces the style value for the given style name. This method takes
    precedence."""
    self.__forced_styles__[name] = value

  def _getStylePrefix(self) -> str:
    """Getter-function for style prefix. This is defined by the name of
    the class, the style-id of the widget, the state of the widget and the
    name of the style. THis method returns only the prefix."""
    clsName = self.__class__.__name__
    styleId = self.getId()
    state = self.getState()
    partKeys = [str(i) for i in [clsName, styleId, state] if i]
    return '/%s/' % '/'.join(partKeys)

  def getStyle(self, name: str) -> Any:
    """Returns the style value for the given style name. """
    forcedStyle = self._getForcedStyle(name)
    if forcedStyle is not None:
      return forcedStyle
    defaultKey = name
    styleKey = '%s%s' % (self._getStylePrefix(), name)
    app = QCoreApplication.instance()
    if TYPE_CHECKING:
      assert isinstance(app, App)
    settings = app.getSettings()
    if TYPE_CHECKING:
      assert isinstance(settings, AppSettings)
    settingsValue = settings.value(styleKey)
    if settingsValue is not None:
      self.typeGuard(name, settingsValue)
      return settingsValue
    defaultStyle = self.defaultStyles(name)
    if defaultStyle is not None:
      self.typeGuard(name, defaultStyle)
      return defaultStyle
    return self.fallbackStyles(name)
