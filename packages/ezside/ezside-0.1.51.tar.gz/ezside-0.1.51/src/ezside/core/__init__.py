"""The 'ezside.core' package provides a limited selection from the Qt
namespace in much shorter named versions.

"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._cursor_vector import CursorVector
from ._qt_names import *
from ._ez_timer import EZTimer
from ._resolve_font_enums import resolveFontFamily
from ._resolve_font_enums import resolveFontWeight, resolveFontCase
from ._resolve_align_enums import resolveAlign
from ._resolve_enum import resolveEnum
from ._parse_font import parseFont
from ._parse_pen import parsePen, emptyPen
from ._parse_brush import parseBrush, emptyBrush

from ._colors import *

from ._parse_parent import parseParent
