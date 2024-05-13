"""The parseEnum function parses the name or value of a Qt Enum. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from enum import EnumType
from typing import Any


def resolveEnum(enumType: EnumType, name: str) -> Any:
  """The parseEnum function parses the name or value of a Qt Enum. """
  for key, val in enumType:
    if name.lower() == key.lower():
      return val
    if name.lower() == val.name.lower():
      return val
