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
import sys
import os
import logging
from qtpy.QtGui import QFont
from qtpy.QtWidgets import (
    QMainWindow,
    QApplication,
    QAction,
    QWidget,
    QStyle,
    QLabel,
    QSizePolicy,
    QHBoxLayout,
    QTabBar,
    QStackedWidget,
    QVBoxLayout,
    QSpacerItem,
    QTabWidget,
)
from qtpy.QtCore import QObject, Signal, QThread, Slot, Qt
from DMT.gui import OptimizationWidget
from DMT.gui.commands import ReplotCommand, StartExtraction, PullCommand, PushCommand
from DMT.extraction import Xtraction
from DMT.gui import PlotsWidget, undo_stack


class XStepGui(QMainWindow):
    # https://stackoverflow.com/questions/11643221/are-there-default-icons-in-pyqt-pyside
    """This class can be used to display and control a single XStep.

    For details look into the XtractionGui class, the documentation can also be applied here.
    """

    def __init__(self, xstep):
        self.app = QApplication(sys.argv)
        self.xstep = xstep
        self.extraction_widget = None
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_widget = QTabWidget()
        self.status_bar = self.statusBar()

        # add actions
        # icons for current xstep ----------------------------------------------------
        undo_icon = self.main_widget.style().standardIcon(getattr(QStyle, "SP_ArrowLeft"))
        self.undo_action = QAction(undo_icon, "Undo", self)

        redo_icon = self.main_widget.style().standardIcon(getattr(QStyle, "SP_ArrowRight"))
        self.redo_action = QAction(redo_icon, "Redo", self)

        extract_icon = self.main_widget.style().standardIcon(getattr(QStyle, "SP_MediaPlay"))
        extract_action = QAction(extract_icon, "Start XStep", self)
        extract_action.triggered.connect(self.extract)

        apply_icon = self.main_widget.style().standardIcon(getattr(QStyle, "SP_DialogOkButton"))
        apply_action = QAction(apply_icon, "Apply Changes", self)
        apply_action.triggered.connect(self.replot)

        self.toolbar = self.addToolBar("bar")
        self.toolbar.setStyleSheet("QToolBar{spacing:5px;}")

        self.toolbar.addAction(self.undo_action)
        self.toolbar.addAction(self.redo_action)
        self.toolbar.addAction(extract_action)
        self.toolbar.addAction(apply_action)

        self.toolbar.addSeparator()

        self.curr_lbl = QLabel("current xstep: None")

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)
        self.toolbar.addWidget(self.curr_lbl)

        self.undo_action.triggered.connect(undo_stack.undo)
        self.redo_action.triggered.connect(undo_stack.redo)

        self.curr_lbl.setText("current xstep: " + self.xstep.name)

        # init the extraction widget and place it as central widget
        self.extraction_widget = OptimizationWidget(self.xstep, xtraction=None)
        self.main_widget.addTab(self.extraction_widget, "optimization widget")
        self.plots_widget = PlotsWidget(self.xstep)
        self.main_widget.addTab(self.plots_widget, "others plots")

        # self.worker_thread = QThread()
        # self.worker_thread.start()

        self.x_step_worker = XWorker(self.xstep)
        self.x_step_worker.start.connect(self.x_step_worker.run)

        # connect everything AFTER creating the thread
        self.xstep.process.connect(self.extraction_widget.process)
        self.xstep.finished.connect(self.extraction_widget.refresh)
        self.xstep.mcardChanged.connect(self.extraction_widget.refresh)
        self.setCentralWidget(self.main_widget)

        # self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("DMT XStep - Alpha Version")

    def start(self):
        self.show()  # Show the form
        self.app.exec_()

    def replot(self):
        """This method invokes a recalculation and replot of the plots using the currently displayed ParaEditBox values."""
        self.status_bar.showMessage("replotting...", 1000)  # update status bar
        undo_stack.push(ReplotCommand(self.xstep))

    def extract(self):
        """This method starts the extraction of the XStep object."""
        self.status_bar.showMessage("extraction in progress")  # set the status bar
        try:
            self.extraction_widget.para_editor.update()  # take over new parameters from the para editor widget
            inactive_paras = self.extraction_widget.para_editor.get_inactive_paras()
        except AttributeError:  # some Xsteps dont have a para editor
            pass
        undo_stack.push(StartExtraction(self.xstep))
        self.status_bar.showMessage("")  # set the status bar


class XWorker(QObject):
    """This is a wrapper for an XStep's extract method. Instances of this class can be moved into new QThreads."""

    start = Signal()
    finished = Signal()

    def __init__(self, xstep):
        QObject.__init__(self)
        self.xstep = xstep  # the wrapped XStep

    @Slot()
    def run(self):  # should be called upon emitting the XWorker.start Signal.
        print("running")
        self.xstep.extract()
