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
import copy
import logging
import numpy as np
import datetime
from qtpy.QtGui import QFont
from qtpy.QtCore import Signal, QAbstractTableModel, Qt, Slot
from qtpy.QtWidgets import QWidget, QTableView, QVBoxLayout, QSizePolicy, QMenu, QAction
from DMT.gui import format_float, undo_stack
from DMT.gui.commands import SetMcard
from DMT.extraction import Xtraction


class MCardWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.mcard = None
        self.source = None
        self.table_model = None
        self.table_view = QTableView()
        font = QFont("Times", 14)
        self.table_view.setFont(font)
        self.init_size = True

        # add right click context menu to header
        self.table_view.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.horizontalHeader().customContextMenuRequested.connect(self.popup_header)

        # add right click context menu to body
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.popup_body)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)
        self.setLayout(layout)

    @Slot(Xtraction)
    def set_mcard(self, source):
        self.source = source
        self.mcard = source.mcard
        try:
            self.table_model = MCardModel(  # used for Xtractions -> Global MCard
                copy.deepcopy(self.mcard),
                dir_mcards=source.dirs["mcard_dir"],
            )
        except AttributeError:  # XStep has no MCard
            self.table_model = MCardModel(copy.deepcopy(self.mcard))
        self.table_model.mcardChanged.connect(self.refresh)
        self.table_view.setModel(self.table_model)

        if self.init_size:
            self.table_view.resizeColumnsToContents()
            self.init_size = False  # do this only once, since it is VERY slow

        self.update()
        self.source.mcardChanged.connect(self.refresh)

    def update(self):
        self.table_view.horizontalHeader().stretchLastSection()
        # self.table_view.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        # self.table_view.resizeColumnsToContents()
        self.repaint()

    def refresh(self):
        self.mcard = self.source.mcard
        self.table_model.refresh(self.mcard)
        self.table_model.layoutChanged.emit()
        self.update()

    def sizeHint(self):
        return self.table_view.sizeHint()

    def minimumSizeHint(self):
        return self.table_view.minimumSizeHint()

    def modify_mcard(self):
        undo_stack.push(SetMcard(self.step, self.table_model.mcard))  # write the new modelcard

    def popup_body(self, pos):
        selection = self.table_view.selectionModel().selection()

        menu = QMenu()
        if len(selection.indexes()) == 1:
            push_action = QAction("Push value to current MCard")
            copy_action = QAction("Copy value to current MCard")
        else:
            push_action = QAction("Push values to current MCard")
            copy_action = QAction("Copy values to current MCard")

        if any([i.column() < 4 for i in selection.indexes()]):
            print("Column < 4")
            push_action.setEnabled(False)
            copy_action.setEnabled(False)
        elif any([i.column() != selection.indexes()[0].column() for i in selection.indexes()]):
            print("Column differs")
            push_action.setEnabled(False)
            copy_action.setEnabled(False)

        # menu.addAction(push_action)
        menu.addAction(copy_action)

        action = menu.exec_(self.mapToGlobal(pos))
        if action == copy_action:
            # do it
            values_to_set = {}
            for index in selection.indexes():
                row_index = index.siblingAtColumn(0)
                try:
                    values_to_set[self.table_model.data(row_index, Qt.DisplayRole)] = float(
                        self.table_model.data(index, Qt.DisplayRole)
                    )
                except ValueError:
                    # in empty cells: float(''):
                    pass
            if values_to_set:
                self.table_model.mcard.set_values(values_to_set)
                self.table_model.mcardChanged.emit()
                logging.info("MCardWidget emitted mcardChanged Signal.")

        elif action == push_action:
            # difference push - copy:
            # with push the mcard is also saved accoring to the xtraction autosave policy
            # strange thing to implement here in the GUI...
            # do not offer it for now! (bot added to the menu)
            raise NotImplementedError()

    def popup_header(self, point):
        push_action = QAction("Push all values to current MCard")
        copy_action = QAction("Copy all values to current MCard")
        column = self.table_view.columnAt(point.x())
        if column < 4:
            print("Column < 4")
            push_action.setEnabled(False)
            copy_action.setEnabled(False)

        menu = QMenu()
        # menu.addAction(push_action)
        menu.addAction(copy_action)
        action = menu.exec_(self.mapToGlobal(point))
        if action == copy_action:
            # do it
            values_to_set = {}
            for row in range(self.table_model.rowCount(None)):
                index = self.table_model.index(row, column)
                row_index = index.siblingAtColumn(0)
                try:
                    values_to_set[self.table_model.data(row_index, Qt.DisplayRole)] = float(
                        self.table_model.data(index, Qt.DisplayRole)
                    )
                except ValueError:
                    # in empty cells: float(''):
                    pass

            if values_to_set:
                self.table_model.mcard.set_values(values_to_set)
                self.table_model.mcardChanged.emit()
                logging.info("MCardWidget emitted mcardChanged Signal.")
        elif action == push_action:
            # difference push - copy:
            # with push the mcard is also saved accoring to the xtraction autosave policy
            # strange thing to implement here in the GUI...
            # do not offer it for now! (bot added to the menu)
            raise NotImplementedError()


class MCardModel(QAbstractTableModel):
    mcardChanged = Signal()

    def __init__(self, mcard, dir_mcards=None):
        QAbstractTableModel.__init__(self)
        self.mcard = mcard
        self.header = ["Name", "Value", "Boundary low", "Boundary up"]
        self.dir_mcards = dir_mcards
        self.mcard_history = {}
        self.mcard_history_keys = []
        if self.dir_mcards is not None:
            self.read_mcard_history()

    def rowCount(self, parent):
        return len(self.mcard)

    def columnCount(self, parent):
        if self.dir_mcards is None:
            return 4

        return 4 + len(
            [child for child in self.dir_mcards.iterdir()]
        )  # 4 for the MCard itself and then the number of saved files in the directory

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role == Qt.BackgroundRole:
            return None
        elif role != Qt.DisplayRole:
            return None

        para = self.mcard.paras[index.row()]

        if index.column() == 0:
            return para.name
        elif index.column() == 1:
            return format_float(para.value)
        elif index.column() == 2:
            return format_float(para.min)
        elif index.column() == 3:
            return format_float(para.max)

        if len(self.mcard_history) != len([child for child in self.dir_mcards.iterdir()]):
            self.read_mcard_history()

        try:
            key = self.mcard_history_keys[index.column() - 4]
            value_history = self.mcard_history[key].get(para).value

            if para.value != 0 and np.abs(para.value) < 1e-8:
                # for saturation currents, zero-bias capacitances and charges...
                atol = 1e-35
            else:
                atol = 1e-8

            if np.isclose(value_history, para.value, atol=atol):
                return ""
        except KeyError:
            return "Not available"

        return format_float(value_history)

    def setData(self, index, value, role):
        para = self.mcard.paras[index.row()]
        if index.column() == 1:
            para.value = para.val_type(value)
        elif index.column() == 2:
            para.min = para.val_type(value)
        elif index.column() == 3:
            para.max = para.val_type(value)

        self.mcard.set(para)
        self.mcardChanged.emit()
        logging.info("MCardWidget emitted mcardChanged Signal.")

        return self.dataChanged.emit(index, index)

    def flags(self, index):
        if not index.isValid():
            return None
        else:
            if index.column() in [1, 2, 3]:
                return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            elif index.column() == 0:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable
            elif index.column() >= 4:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]

        return None

    def refresh(self, mcard):
        self.mcard = mcard
        if self.dir_mcards is not None and len(self.mcard_history) != len(
            [child for child in self.dir_mcards.iterdir()]
        ):
            self.read_mcard_history()

            # for i_row, param in enumerate(self.mcard):
            #     for i_column, mcard_old in enumerate(self.mcard_history):
            #         para_old = mcard_old.get(param)
            #         if not np.isclose(para_old.value, param.value):
            #             self.colors[(i_row, i_column + 4)] = QBrush(Qt.red)

    def read_mcard_history(self):
        self.mcard_history_keys = []
        self.header = ["Name", "Value", "Boundary low", "Boundary up"]

        time_now = datetime.datetime.now()
        mcardclass = self.mcard.__class__
        for path in sorted([child for child in self.dir_mcards.iterdir()], reverse=True):
            time_history = datetime.datetime.strptime(path.stem, "%Y-%m-%d_%H-%M-%S")
            time_delta = time_now - time_history

            if time_delta.days > 1:
                header_col = time_history.strftime("%Y/%m/%d %H:%M:%S")
            elif time_delta.days == 1:
                header_col = time_history.strftime("yesterday %H:%M:%S")
            elif time_delta.seconds > 3600:
                header_col = time_history.strftime("%H:%M:%S")
            else:
                minutes, seconds = divmod(time_delta.seconds, 60)
                if minutes > 0:
                    header_col = f"{minutes:d}:{seconds:2d}min before"
                else:
                    header_col = f"{seconds:d}s before"

            self.header.append(header_col)
            self.mcard_history_keys.append(time_history)
            if time_history not in self.mcard_history:
                self.mcard_history[time_history] = mcardclass.load_json(path)
