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
from qtpy.QtWidgets import QTreeView, QSizePolicy
from qtpy.QtCore import QAbstractItemModel, QModelIndex, Qt
from DMT.gui import OptimizationWidget, MCardWidget, PlotsWidget  # , OpDefinitionWidget


class XtractionTreeView(QTreeView):
    def __init__(self, data):
        # pylint: disable = unused-argument
        super().__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.extraction = None

    def loadXtraction(self, extraction):
        self.extraction = extraction
        self.setModel(TreeModel(extraction))

    def getIndex(self, item):
        return self.model().getIndex(item)


class StepItem(object):
    def __init__(self, step, parent=None, xtraction=None):
        self.parentItem = parent
        self.itemData = [step.__class__.__name__, step.name]
        self.step = step
        self.childItems = []
        self.childItems.append(OptimizationItem(step, parent=self, xtraction=xtraction))
        self.widget = self.childItems[
            -1
        ].widget  # Step Items widget is the OptimizationItems' widget!
        self.childItems.append(PlotsItem(step, parent=self))
        self.childItems.append(MCardItem(step, parent=self))
        # self.childItems.append(OpDefinitionItem(step, parent=self)) # TODO

    def refresh(self):
        pass

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class HeaderItem(object):
    def __init__(self, name, dut_type, parent=None):
        self.parentItem = parent
        self.itemData = [name, dut_type]
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class PlotsItem(object):
    def __init__(self, step, parent=None):
        self.parentItem = parent
        self.itemData = ["Plots"]
        self.widget = PlotsWidget(step)

    def childCount(self):
        return 0

    def columnCount(self):
        return 1

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class MCardItem(object):
    def __init__(self, step, parent=None):
        self.parentItem = parent
        self.itemData = ["MCard"]
        self.widget = MCardWidget()
        self.widget.set_mcard(step)

    def childCount(self):
        return 0

    def columnCount(self):
        return 1

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class OpDefinitionItem(object):
    def __init__(self, step, parent=None):
        self.parentItem = parent
        self.itemData = ["OpDefinition"]
        # self.widget     = OpDefinitionWidget
        # self.widget.set_data(step)

    def childCount(self):
        return 0

    def columnCount(self):
        return 1

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class OptimizationItem(object):
    def __init__(self, step, parent=None, xtraction=None):
        self.parentItem = parent
        self.itemData = ["Optimization"]
        self.widget = OptimizationWidget(step, xtraction=xtraction)

    def childCount(self):
        return 0

    def columnCount(self):
        return 1

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0


class TreeModel(QAbstractItemModel):
    def __init__(self, extraction, parent=None):
        super(TreeModel, self).__init__(parent)
        self.extraction = extraction
        self.rootItem = HeaderItem("XStepClass", "Name")
        self.steps = self.extraction.available_xsteps
        self.setupModelData(self.rootItem, xtraction=self.extraction)

    def getIndex(self, item):
        for row in range(0, self.rowCount(QModelIndex())):
            index = self.index(row, 0, QModelIndex())
            item_at_index = index.internalPointer()
            if item_at_index == item:
                return index

        raise IOError("DMT->GUI->XtractionTreeView->getIndex: Could not find index of item.")

        # for row in range(0, item_at_index.rowCount(index)):
        #     index = self.index(row, 0, )

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)
        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def setupModelData(self, parent, xtraction=None):
        parents = [parent]
        for step in self.steps:
            parents[-1].appendChild(StepItem(step, parent=parents[-1], xtraction=xtraction))
