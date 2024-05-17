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
# main.py
from qtpy.QtWidgets import QWidget, QStyle
from qtpy.QtCore import QModelIndex, Signal, Slot, QObject, QItemSelectionModel
from DMT.gui import StepItem, undo_stack
from DMT.gui.commands import StartExtraction, PullCommand, PushCommand, StopOptimizationCommand
import logging

# pyside2-uic DMT/gui/xtraction_view_ui.ui -o DMT/gui/xtraction_view_ui.py
from DMT.gui.xtraction_view_ui import Ui_Form


class XtractionView(QWidget, Ui_Form):
    statusMessage = Signal(str)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined
        self.x_step_worker = None
        self.currStepItem = None  # pointer to the currently active StepItem
        self.currWidget = None  # pointer to the currently displayed items widget
        self.extraction = None

        extract_icon = self.style().standardIcon(getattr(QStyle, "SP_MediaPlay"))
        self.extractButton.setIcon(extract_icon)
        self.extractButton.clicked.connect(self.extract)

        pull_icon = self.style().standardIcon(getattr(QStyle, "SP_ArrowDown"))
        self.pullButton.setIcon(pull_icon)
        self.pullButton.clicked.connect(self.pull)

        push_icon = self.style().standardIcon(getattr(QStyle, "SP_ArrowUp"))
        self.pushButton.setIcon(push_icon)
        self.pushButton.clicked.connect(self.push)

        stop_icon = self.style().standardIcon(getattr(QStyle, "SP_BrowserStop"))
        self.stopButton.setIcon(stop_icon)
        self.stopButton.clicked.connect(self.stop)

        # apply_icon = self.style().standardIcon(getattr(QStyle, 'SP_DialogOkButton'))
        # self.applyButton.setIcon(apply_icon)

        undo_icon = self.style().standardIcon(getattr(QStyle, "SP_ArrowLeft"))
        self.undoButton.setIcon(undo_icon)
        self.redoButton.clicked.connect(undo_stack.redo)

        redo_icon = self.style().standardIcon(getattr(QStyle, "SP_ArrowRight"))
        self.redoButton.setIcon(redo_icon)
        self.undoButton.clicked.connect(undo_stack.undo)

    def loadXtraction(self, extraction):
        self.extraction = extraction
        self.treeView.loadXtraction(extraction)  # widgets are inited inside this amazing class
        model = self.treeView.model()
        rows = range(0, model.rowCount(QModelIndex()))
        # step_items = model.index(rows[0], 0, QModelIndex() )
        step_items = [model.index(row, 0, QModelIndex()).internalPointer() for row in rows]

        initial_step_widget = None
        for step_item in step_items:
            for childItem in step_item.childItems:
                widget = childItem.widget
                if widget is not None:  # some widgets not yet implemented
                    self.stackedWidget.addWidget(childItem.widget)

            if step_item.step == extraction.curr_xstep:
                initial_step_widget = step_item.widget
                self.currStepItem = step_item

        self.currWidget = initial_step_widget
        index = self.stackedWidget.indexOf(
            initial_step_widget
        )  # index of main_plot_widget in list of all widgets
        self.stackedWidget.setCurrentIndex(index)

        selection_model = self.treeView.selectionModel()
        index = self.treeView.getIndex(self.currStepItem)
        selection_model.select(index, QItemSelectionModel.ClearAndSelect)
        selection_model.selectionChanged.connect(self.changeCurrentWidget)

        self.stackedWidget.repaint()

        self.step_changed(self.extraction.curr_xstep)

        logging.info("XtractionView loaded xtraction %s!", self.extraction.name)

    def extract(self):
        self.statusMessage.emit("optimizing.")  # set the status bar
        undo_stack.push(StartExtraction(self.extraction))
        self.statusMessage.emit("optimization finished.")  # set the status bar

    def push(self):
        self.statusMessage.emit("pushing local mcard.")  # set the status bar
        undo_stack.push(PushCommand(self.extraction))
        self.statusMessage.emit("pushed local mcard.")  # set the status bar

    def stop(self):
        self.statusMessage.emit("stopping optimization.")  # set the status bar
        undo_stack.push(StopOptimizationCommand(self.extraction))
        self.statusMessage.emit("stopped optimization.")  # set the status bar

    def pull(self):
        self.statusMessage.emit("pulling global mcard.")  # set the status bar
        undo_stack.push(PullCommand(self.extraction))
        self.statusMessage.emit("pulled global mcard.")  # set the status bar

    def changeCurrentWidget(self, current, previous):
        # pylint: disable= unused-argument
        item = current.indexes()[1].internalPointer()
        self.currWidget = item.widget
        self.currWidget.refresh()
        index = self.stackedWidget.indexOf(
            item.widget
        )  # index of main_plot_widget in list of all widgets
        self.stackedWidget.setCurrentIndex(index)
        if isinstance(item, StepItem):
            step = item.step
            self.currStepItem = item
        else:
            step = item.parent().step
            self.currStepItem = item.parent()

        if step != self.extraction.curr_xstep:
            self.step_changed(step)

    def step_changed(self, step):
        # pylint: disable=bare-except
        self.extraction.activate_xstep(step.name)

        # move xstep into worker thread and start the thread
        if not self.x_step_worker:
            self.x_step_worker = XWorker(self.extraction.curr_xstep)
            self.x_step_worker.start.connect(self.x_step_worker.run)  #  <---- Like this instead
            self.x_step_worker.extraction = self.extraction

        self.extractionStatus.setStep(self.extraction.curr_xstep)

        # connect everything AFTER creating the thread
        try:  # make sure it is only connected one time...dirty but works
            self.extraction.curr_xstep.process.disconnect()
            self.extraction.curr_xstep.finished.disconnect()
            self.extraction.curr_xstep.mcardChanged.disconnect()
            self.extraction.mcardChanged.disconnect()
        except:
            pass

        self.extraction.curr_xstep.process.connect(self.extractionStatus.process)
        self.extraction.curr_xstep.finished.connect(self.extractionStatus.reset)
        self.extraction.curr_xstep.mcardChanged.connect(self.refresh)
        self.extraction.mcardChanged.connect(self.refresh)
        self.extraction.curr_xstep.finished.connect(self.refresh)
        # logging.info('Changed current XStep to: ' + self.xtraction_views.tabText(index) )

    def refresh(self):
        self.currWidget.refresh()


class XWorker(QObject):
    """This is a wrapper for an XStep's extract method. Instances of this class can be moved into new QThreads."""

    start = Signal()
    finished = Signal()

    def __init__(self, extraction):
        QObject.__init__(self)
        self.extraction = extraction  # the wrapped XStep

    @Slot()
    def run(self):  # should be called upon emitting the XWorker.start Signal.
        self.extraction.curr_xstep.extract()
