# DMT
# Copyright (C) from 2022  SemiMod
# Copyright (C) until 2021  Markus Müller, Mario Krattenmacher and Pascal Kuthe
# <https://gitlab.com/dmt-development/dmt-extraction>
#
# This file is part of DMT-extraction.
#
# DMT-extraction is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# DMT-extraction is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along with DMT-extraction.
# If not, see <https://www.gnu.org/licenses/>.
import os
from pathlib import Path
from qtpy.QtWidgets import QFileDialog, QDialog
from qtpy.QtCore import QDir


def file_dialog(directory="", forOpen=True, fmt="", isFolder=False):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.DontUseCustomDirectoryIcons
    dialog = QFileDialog()
    dialog.setOptions(options)

    dialog.setFilter(dialog.filter() | QDir.Hidden)

    # are we talking about files or folders
    if isFolder:
        dialog.setFileMode(QFileDialog.Directory)
    else:
        dialog.setFileMode(QFileDialog.AnyFile)
    # opening or saving
    if forOpen:
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
    else:
        dialog.setAcceptMode(QFileDialog.AcceptSave)

    # set format, if specified
    if fmt != "" and isFolder is False:
        if isinstance(fmt, str):
            dialog.setDefaultSuffix(fmt)
            dialog.setNameFilters(["{0:s} (*.{0:s})".format(fmt), "all (*)"])
        else:
            dialog.setDefaultSuffix(fmt[0])
            if "*" not in fmt:
                fmt.append("*")

            dialog.setNameFilters(["{0:s} (*.{0:s})".format(fmt_a) for fmt_a in fmt])

    # set the starting directory
    if directory:
        dialog.setDirectory(str(directory))
    else:
        dialog.setDirectory(str(os.getcwd()))

    if dialog.exec_() == QDialog.Accepted:
        return Path(dialog.selectedFiles()[0])  # returns a list

    return None
