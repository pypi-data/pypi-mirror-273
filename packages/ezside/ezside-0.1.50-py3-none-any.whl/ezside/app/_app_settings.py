"""AppSettings subclasses the QSettings class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING, Any, Union, Dict, Callable

from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon, QKeySequence
from icecream import ic
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import AlignHCenter, \
  AlignRight, \
  AlignLeft, \
  AlignCenter, \
  AlignFlag

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True, )

if sys.version_info.minor < 10:
  StrData = Union[Dict[str, str], str]
else:
  StrData = dict[str, str] | str


class AppSettings(QSettings):
  """The 'AppSettings' class provides a convenient interface for
  working with the application's variable settings. """

  __on_missing__ = None

  @classmethod
  def _getShortcuts(cls, key: str = None) -> StrData:
    """Get the keyboard shortcuts."""
    if key is None:
      return {
        'new'      : 'CTRL+N',
        'open'     : 'CTRL+O',
        'save'     : 'CTRL+S',
        'saveAs'   : 'CTRL+SHIFT+S',
        'close'    : 'CTRL+W',
        'undo'     : 'CTRL+Z',
        'redo'     : 'CTRL+Y',
        'cut'      : 'CTRL+X',
        'copy'     : 'CTRL+C',
        'paste'    : 'CTRL+V',
        'selectAll': 'CTRL+A',
        'aboutQt'  : 'F12',
        'exit'     : 'ALT+F4',
        'debug1'   : 'F1',
        'debug2'   : 'F2',
        'debug3'   : 'F3',
        'debug4'   : 'F4',
        'debug5'   : 'F5',
        'debug6'   : 'F6',
        'debug7'   : 'F7',
        'debug8'   : 'F8',
        'debug9'   : 'F9',
        '__empty__': '',
      }
    if isinstance(key, str):
      shortcuts = cls._getShortcuts()
      if key in shortcuts:
        return shortcuts[key]
      return shortcuts['__empty__']
    e = typeMsg('key', key, str)
    raise TypeError(e)

  @classmethod
  def _getIconPath(cls, key: str = None) -> StrData:
    """Get the icons."""
    if key is None:
      here = os.path.dirname(__file__)
      there = os.path.join(here, 'iconfiles')
      fileNames = {
        'editMenu'    : 'edit_menu',
        'add'         : 'add',
        'debug'       : 'debug',
        'exitImg'     : 'exit_img',
        'microphone'  : 'microphone',
        'aboutPython' : 'about_python',
        'cut'         : 'cut',
        'exit'        : 'exit',
        'unlocked'    : 'unlocked',
        'aboutQt'     : 'about_qt',
        'selectAll'   : 'select_all',
        'paste'       : 'paste',
        'redo'        : 'redo',
        'preferences' : 'preferences',
        'saveAs'      : 'save_as',
        'minescript'  : 'minescript',
        'screenShot'  : 'screen_shot',
        'undo'        : 'undo',
        'new'         : 'new',
        'risitas'     : 'risitas',
        'filesMenu'   : 'files_menu',
        'locked'      : 'locked',
        'aboutConda'  : 'about_conda',
        'files'       : 'files',
        'open'        : 'open',
        'save'        : 'save',
        'help'        : 'help',
        'copy'        : 'copy',
        'workside'    : 'workside',
        'aboutPySide6': 'about_py_side6',
        'aboutPySide' : 'about_py_side6',
        'helpMenu'    : 'help_menu',
        'pogchamp'    : 'pogchamp',
        '__empty__'   : 'risitas',
      }
      filePaths = {}
      for name, fileName in fileNames.items():
        filePath = os.path.join(there, '%s.png' % fileName)
        filePaths[name] = filePath
      return filePaths
    iconPaths = cls._getIconPath()
    if key in iconPaths:
      return iconPaths[key]
    return iconPaths['__empty__']

  @staticmethod
  def _parseInt(val: str) -> int | None:
    """Convert a string to an integer."""
    if all([c in '0123456789_' for c in val]):
      return int(val)
    return None

  @staticmethod
  def _parseFloat(val: str) -> float | None:
    """Convert a string to a float."""
    if all([c in '0123456789_.' for c in val]):
      if len(val) - len(val.replace('.', '')) > 1:
        return None
      return float(val)
    return None

  @staticmethod
  def _parseAlignment(val: str, key: str = None) -> int | None:
    """Parse the alignment."""
    if 'align' in key.lower():
      if 'horizontal' in key.lower():
        if 'center' in val.lower():
          return AlignHCenter
        if 'left' in val.lower():
          return AlignLeft
        if 'right' in val.lower():
          return AlignRight
      if 'vertical' in key.lower():
        if 'center' in val.lower():
          return AlignHCenter
        if 'top' in val.lower():
          return AlignLeft
        if 'bottom' in val.lower():
          return AlignRight
      if 'center' in val.lower():
        return AlignCenter
    return None

  def value(self, *args) -> Any:
    """Get the value of the key."""
    val = self._wrapValue(*args)
    key = args[0]
    if not isinstance(val, str):
      return val
    intVal = self._parseInt(val)
    if isinstance(intVal, int):
      return intVal
    floatVal = self._parseFloat(val)
    if isinstance(floatVal, float):
      return floatVal
    alignVal = self._parseAlignment(val, key)
    if isinstance(alignVal, AlignFlag):
      return alignVal

  def _wrapValue(self, *args) -> Any:
    """Get the value of the key."""
    key, fb, type_ = [*args, None, None, None][:3]
    if key is None:
      e = """At least a key must be provided!"""
      raise ValueError(monoSpace(e))
    keyWords = [w for w in key.split('/') if w]
    if keyWords[0] == 'icon':
      return QIcon(self._getIconPath(keyWords[1]))
    if keyWords[0] == 'shortcut':
      return QKeySequence(self._getShortcuts(keyWords[1]))
    value = QSettings.value(self, key)
    if value is None:
      self._onMissing(key, fb)
      return fb
    if fb is None:
      return value
    if type_ is None:
      return QSettings.value(self, key, fb)
    return QSettings.value(self, key, fb, type_)

  def __init__(self, onMissing: Callable = None) -> None:
    """Initialize the AppSettings object."""
    QSettings.__init__(self, )
    if onMissing is not None:
      if callable(onMissing):
        self.__on_missing__ = onMissing

  def _onMissing(self, key: str, fb: Any = None) -> Any:
    """Record missing value"""
    if self.__on_missing__ is None:
      return
    return self.__on_missing__(key, fb)

  def toStringFactory(self, cls: type) -> Callable:
    """Because QSettings is a scam pretending to save python objects,
    but instead saving text we here provide a factory for creating
    converters from the given type to a string. """
