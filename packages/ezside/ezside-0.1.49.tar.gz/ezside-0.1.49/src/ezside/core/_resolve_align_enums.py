"""This module provides functions that resolve alignment enum names."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.core import AlignFlag


def resolveAlign(*args) -> AlignFlag:
  """This module provides functions that resolve alignment enum names."""
  name, value = None, None
  for arg in args:
    if isinstance(arg, str) and name is None:
      name = arg
    elif isinstance(arg, int) and value is None:
      value = arg

  if name is None and value is None:
    e = ValueError('No alignment name or value provided.')

  for key, val in AlignFlag:
    if name is not None and key.lower() == name.lower():
      return val
    if value is not None and val == value:
      return val
