"""The resolveFontWeight function finds the enum in QFont Weight which
matches the given name. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont
from PySide6.QtGui import QFontDatabase


def resolveFontWeight(weight: str) -> QFont.Weight:
  """Resolves the font weight name"""
  for name, value in QFont.Weight:
    if name.lower() == weight.lower():
      return value


def resolveFontCase(fontCase: str) -> QFont.Capitalization:
  """Resolves the font case name"""
  for name, value in QFont.Capitalization:
    if name.lower() == fontCase.lower():
      return value


def resolveFontFamily(family: str) -> str:
  """Resolves the font family name"""
  font_families = QFontDatabase().families()

  if family in font_families:
    return family
  elif family == 'monospace':
    return 'Courier'
  elif family == 'serif':
    return 'Times'
  elif family == 'sans-serif':
    return 'Helvetica'
  else:
    return 'Helvetica'  # default font family
