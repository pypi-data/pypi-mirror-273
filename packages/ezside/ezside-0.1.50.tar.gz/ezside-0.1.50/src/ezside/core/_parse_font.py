"""The 'parseFont' function creates instances of QFont. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QFont, QFontDatabase


class _FontParser:
  """This class implementation prevents calls to QFontDatabase from
  occurring before the QApplication is initialized. """

  def __init__(self) -> None:
    self.fontDatabase = QFontDatabase()

  def __call__(self, *args, **kwargs) -> QFont:
    """The 'parseFont' function creates instances of QFont. """
    family, fontSize, fontWeight, fontCase = None, None, None, None
    for arg in args:
      if isinstance(arg, str):
        if arg in QFontDatabase.families() and family is None:
          family = arg
      elif isinstance(arg, int) and fontSize is None:
        fontSize = arg
      elif isinstance(arg, QFont.Weight) and fontWeight is None:
        fontWeight = arg
      elif isinstance(arg, QFont.Capitalization) and fontCase is None:
        fontCase = arg
    family = 'Helvetica' if family is None else family
    fontSize = 12 if fontSize is None else fontSize
    fontWeight = QFont.Weight.Normal if fontWeight is None else fontWeight
    fontCase = QFont.Capitalization.MixedCase if fontCase is None else (
      fontCase)
    font = QFont()
    font.setFamily(family)
    font.setPointSize(fontSize)
    font.setWeight(fontWeight)
    font.setCapitalization(fontCase)
    return font


def parseFont(*args, **kwargs) -> QFont:
  """The 'parseFont' function creates instances of QFont. """
  try:
    QCoreApplication.instance()
  except Exception as exception:
    e = """The QApplication instance has not been initialized. """
    raise RuntimeError(e) from exception
  return _FontParser()(*args, **kwargs)
