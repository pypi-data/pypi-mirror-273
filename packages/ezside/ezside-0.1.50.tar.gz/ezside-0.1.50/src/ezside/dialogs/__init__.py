"""The 'ezside.dialogs' package provides dialog windows for short term
user interaction such as confirmation boxes, file dialogs, and message
boxes."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._confirm_box import ConfirmBox
from ._color_selection import ColorSelection
from ._font_selection import FontSelection
from ._open_file import OpenFile
from ._save_file import SaveFile
from ._folder_selection import FolderSelection
from ._abstract_user_input import AbstractUserInput
from ._dialog_buttons import DialogButtons
from ._abstract_dialog_window import AbstractDialogWindow
from ._int_dialog_window import IntDialogWindow
from ._user_int import UserInt
