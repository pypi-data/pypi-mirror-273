# DMT
# Copyright (C) 2019  Markus Müller and Mario rattenmacher and the DMT contributors <https://gitlab.hrz.tu-chemnitz.de/CEDIC_Bipolar/DMT/>
#
# This file is part of DMT.
#
# DMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
import copy
import re
import logging

import numpy as np
from pylatexenc.latex2text import LatexNodes2Text
from qtpy.QtCore import QLocale, Qt, Signal, QObject
from qtpy.QtGui import QFont, QValidator, QPalette
from qtpy.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QSizePolicy,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QGroupBox,
    QFrame,
    QScrollArea,
)

from DMT.gui.commands import (
    SetOptimizationMethod,
    SetOptimizationNmax,
    SetOptimizationParaNormalization,
    SetOptimizationTolerance,
    SetPara,
    SetParaPush,
    SetParaActive,
)

# all commands that can be run by the gui
from DMT.exceptions import BoundsError, ValueTooLargeError, ValueTooSmallError
from DMT.extraction import QStep
from DMT.gui import mathTex_to_QPixmap, format_float

# all commands that can be run by the gui
from DMT.gui import XPlot, undo_stack, OpSelectorPlot


QLocale.setDefault(
    QLocale(QLocale.English, QLocale.UnitedStates)
)  # english numbers . instead of german ,


class OptimizationOptionsWidget(QWidget):
    """This Widget displays widgets that can be used to maniupulate to Optimization options.

    Attributes
    ----------
    xstep      : DMT.xstep()
        The xstep whose options are manipulated.
    layout     : QGridLayout()
        The Layout used to display the widgets.
    fit_method : QComboBox()
        A ComboBox widget used to manipulate the fit_method.
    ftol       : QLineEdit
        A LineEdit widget used to manipulate the optimizer's function tolerance.
    nmax       : QSpinBox()
        A SpinBox used to manipulate the optimizer's maximum number of iterations.
    normalize  : QCheckBox()
        A checkbox that controls wheather or not the model parameters shall be normalized during the optimization.

    Methods
    -------
    normalize_change()
        Called upon change of the normalization widget.
    method_change(text)
        Called upon change of the fit_method widget.
    ftol_change()
        Called upon change of the function tolerance ftol.
    nmax_change(new_value)
        Called upon change of the nmax parameter
    refresh(self)
        This method is connected to the xstep's finish signal. All widgets are updated in order to match the current state of xstep.
    """

    def __init__(self, xstep):
        super().__init__()

        # init attributes
        self.xstep = xstep
        self.layout = QGridLayout()
        self.fit_method = QComboBox()
        self.fit_method.setMaximumWidth(200)
        self.ftol = QLineEdit()
        self.ftol.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.ftol.setMaximumWidth(200)
        self.nmax = QSpinBox()
        self.nmax.setMaximumWidth(200)

        # fit method lbl
        fit_method_lbl = QLabel("fit method:")

        # fit method combo box
        self.fit_method.addItems(self.xstep.available_fit_methods)
        self.fit_method.setCurrentText(self.xstep.fit_method)
        # self.fit_method.activated[str].connect(self.method_change)
        self.fit_method.currentTextChanged.connect(self.method_change)

        # ftol lbl
        ftol_lbl = QLabel("ftol:")

        # ftol value widget
        self.ftol.setText(str(self.xstep.f_tol))
        self.ftol.editingFinished.connect(self.ftol_change)

        title = QLabel("Optimizer Options")
        title.setFont(QFont("Times", 14, QFont.Bold))

        # nmax lbl
        n_max = QLabel("n_max:")

        # nmax widget
        self.nmax.setMaximum(1e3)
        self.nmax.setMinimum(0)
        self.nmax.setValue(self.xstep.n_step_max)
        self.nmax.valueChanged.connect(self.nmax_change)

        # normalize lbl
        normalize = QLabel("normalize?")

        # normalize widget
        self.normalize = QCheckBox()
        self.normalize.setChecked(self.xstep.normalize)
        self.normalize.stateChanged.connect(self.normalize_change)

        # create the layout
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(title, 0, 0, 1, 4, alignment=Qt.AlignCenter)
        self.layout.addWidget(fit_method_lbl, 1, 0)
        self.layout.addWidget(self.fit_method, 1, 1)
        self.layout.addWidget(ftol_lbl, 1, 2)
        self.layout.addWidget(self.ftol, 1, 3)
        self.layout.addWidget(n_max, 2, 0)
        self.layout.addWidget(self.nmax, 2, 1)
        self.layout.addWidget(normalize, 2, 2)
        self.layout.addWidget(self.normalize, 2, 3)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(3, 1)
        self.setLayout(self.layout)

    def normalize_change(self):
        """Called upon change of the normalization widget."""
        undo_stack.push(SetOptimizationParaNormalization(self.xstep, self.normalize))

    def method_change(self, text):
        """Called upon change of the fit_method widget."""
        undo_stack.push(SetOptimizationMethod(self.xstep, self.fit_method, text))

    def ftol_change(self):
        """Called upon change of the function tolerance ftol."""
        undo_stack.push(
            SetOptimizationTolerance(self.xstep, self.ftol, float(self.ftol.displayText()))
        )

    def nmax_change(self, new_value):
        """Called upon change of the nmax parameter"""
        undo_stack.push(SetOptimizationNmax(self.xstep, self.nmax, new_value))

    def refresh(self):
        """This method is connected to the xstep's finish and mcardChanged signal. All widgets are updated in order to match the current state of xstep."""
        self.nmax.setValue(self.xstep.n_step_max)
        self.nmax.repaint()
        self.normalize.setChecked(self.xstep.normalize)
        self.normalize.repaint()
        self.ftol.setText(str(self.xstep.f_tol))
        self.ftol.repaint()
        self.fit_method.setCurrentText(self.xstep.fit_method)
        self.fit_method.repaint()


class ExtractionStatusWidget(QWidget):
    """This widget is used to display relevant extraction information during an extraction and provides a cancel aswell as an exit Signal.

    Attributes
    ----------
    stop         : Signal()
        This signal is emitted upon clicking the stop_btn.
    cancel       : Signal()
        This signal is emitted upon clicking the cancel_btn.
    status_bar   : QStatusBar()
        This bar visualizes the current extraction progress.
    n            : int
        This integer represents the number of times the optimization has calculated the jacobian that is currently running.
    n_max        : int
        This integer represents the maximum allowed number of iterations for the optimization.
    layout       : QVBoxLayout()
        This is the layout of this widget.
    progress_bar : QProgressBar()
        This is the ProgressBar widget used to display the optimization progress.
    stop_btn     : QPushButton
        This button can be clicked during optimization in order to emit a stop Signal.
    cancel_btn   : QPushButton
        This button can be clicked during optimization in order to emit a cancel Signal.

    Methods
    -------
    start()
        This should be called at the start of an optimization in order to enable the buttons.
    stop_clicked()
        This method is called upon clicking the stop button and emits a stop Signal.
    cancel_clicked()
        This method is called upon clicking the cancel button and emits a cancel Signal.
    update()
        Increase the progress by one and update the bar.
    refresh()
        Reset the QProgressBar.
    """

    stop = Signal()  # should be connected inside the xstep
    cancel = Signal()  # should be connected inside the xstep

    def __init__(self, parent):
        # lengthy code selected on purpose here to increase readability
        super().__init__()
        self.step = None
        self.n = 0
        self.n_max = 100

        # init the progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat(f"")

        # fill the layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.progress_bar)
        self.setLayout(self.layout)

    def setStep(self, step):
        self.step = step
        self.n = 0
        self.n_max = self.step.n_step_max

    def stop_clicked(self):
        """This method is called upon clicking the stop button and emits a stop Signal."""
        self.stop.emit()
        logging.info("OptimizationWidget emitted stop Signal.")

    def cancel_clicked(self):
        """This method is called upon clicking the cancel button and emits a cancel Signal."""
        self.cancel.emit()
        logging.info("OptimizationWidget emitted cancel Signal.")

    def process(self):
        """Increase the progress by one and update the bar."""
        self.n = self.n + 1
        # progress = self.n/self.n_max*100.0
        self.progress_bar.setFormat(f"step: {self.n:{3}}/{self.n_max:{4}}")
        self.progress_bar.setValue(self.n / self.n_max * 100.0)
        self.progress_bar.repaint()

    def reset(self):
        """Reset the QProgressBar."""
        self.n = 0
        self.n_max = self.step.n_step_max
        self.progress_bar.setFormat(f"")
        self.progress_bar.setValue(0)
        self.progress_bar.repaint()


class PlotsWidget(QTabWidget):
    """This widget can display several plots that are defined in an DMT.XStep object in a tabbed view. It supports an interactive mode and allows to select extraction boundaries via clicking.

    Attributes
    ----------
    step        :  DMT.XStep()
        This is the XStep object that shall be displayed.
    layout      : QVBoxLayout
        This is the Layout of this widget.
    tabs        : QTabWidget
        This widget holds all plots and displays them using a QTabWidget.

    Methods
    -------
    init_gui_plot()
        This should be called in order to take the plot canvas from the xstep and put it into the tab view.
    refresh()
        This method redraws the plots according to the last extraction function evaluation.
    """

    def __init__(self, xstep):
        super().__init__()
        self.main_plot = None
        self.plots = None
        self.step = xstep
        if not xstep.op_selector:
            self.plot_methods = self.step.plot_methods[1:]  # all but main plot
        else:
            self.plot_methods = self.step.plot_methods[2:]  # all but main plot and op_selector_plot
        self.init_plots()
        logging.info("PlotsWidget emitted new Signal.")

    def init_plots(self):
        """This should be called in order to take the plot canvas from the xstep and put it into the tab view."""
        # remove existing tabs
        self.clear()

        # Get all plots -----------------------------------------
        self.plots = []
        for method in self.plot_methods:
            try:
                self.plots.append(PlotWidget(method))
            except (AttributeError, TypeError) as e:
                continue

        # put into tabs ------------------------------------------------
        for plot in self.plots:
            plot_name = LatexNodes2Text().latex_to_text(plot.name)
            self.addTab(plot, plot_name)

        # connect right
        self.setCurrentIndex(0)
        self.currentChanged[int].connect(lambda index: self.refresh(index=index))

    def refresh(self, index=None):
        """This method redraws the plots according to the last extraction function evaluation."""
        if index is None:
            for plot in self.plots:
                plot.refresh()

        else:
            self.plots[index].refresh()


class GlobalPlotWidget(QFrame):
    """This widget can display several plots that are defined in an DMT.XStep object in a tabbed view. It supports an interactive mode and allows to select extraction boundaries via clicking.

    Attributes
    ----------
    step        :  DMT.XStep()
        This is the XStep object that shall be displayed.
    layout      : QVBoxLayout
        This is the Layout of this widget.
    tabs        : QTabWidget
        This widget holds all plots and displays them using a QTabWidget.

    Methods
    -------
    init_gui_plot()
        This should be called in order to take the plot canvas from the xstep and put it into the tab view.
    refresh()
        This method redraws the plots according to the last extraction function evaluation.
    """

    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Plain)
        self.setLineWidth(1)
        self.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.window_layout = QHBoxLayout()
        self.window_layout.setContentsMargins(10, 10, 10, 10)  # important for nice loo

        self.tab_widget = QTabWidget()
        self.plots = None
        self.methods = None
        self.extraction = None

        self.window_layout.addWidget(self.tab_widget)
        self.setLayout(self.window_layout)

    def loadXtraction(self, extraction):
        self.extraction = extraction
        self.methods = self.extraction.global_plot_methods
        self.init_plots()

    def init_plots(self):
        """This should be called in order to take the plot canvas from the xstep and put it into the tab view."""
        # remove existing tabs
        self.tab_widget.clear()

        if len(self.methods) < 1:
            return

        # Get all plots -----------------------------------------
        self.plots = []
        for method in self.methods:
            self.plots.append(PlotWidget(method, mcard=self.extraction.mcard, new=True))

        self.plots[0].plot_bounds = 1

        # put into tabs ------------------------------------------------
        for plot in self.plots:
            self.tab_widget.addTab(plot, plot.name)

        # connect right
        self.refresh(index=0)
        self.tab_widget.setCurrentIndex(0)
        self.tab_widget.currentChanged[int].connect(lambda index: self.refresh(index=index))

    def refresh(self, index=None):
        """This method redraws the plots according to the last extraction function evaluation."""
        if not index:
            index = self.tab_widget.currentIndex()
        self.mcard = self.extraction.mcard
        for plot in self.plots:
            plot.mcard = self.mcard

        plot = self.plots[index]
        plot.refresh(mcard=self.extraction.mcard)


class PlotWidget(QWidget):
    def __init__(self, method, new=False, mcard=None, bounds=None):
        super().__init__()
        self.method = method
        legend_location = None
        try:
            self.plot = self.method(mcard=mcard, calc_all=True)
            legend_location = self.plot.legend_location
        except TypeError as err:
            raise IOError(
                "DMT -> PlotWidget: method" + str(method) + " did not return a valid plot."
            ) from err

        if new:
            self.plot.num = self.plot.num + "_"
            self.plot.name = "extraction plot " + self.plot.name

        self.name = self.plot.name
        self.plot_bounds = 0
        # rescale_icon   = self.main_plot.toolbar.style().standardIcon(getattr(QStyle, 'SP_BrowserReload'))
        # rescale_action = QAction(rescale_icon, 'Rescale', self)
        # rescale_action.triggered.connect(self.reset)
        # self.main_plot.toolbar.addAction(rescale_action)
        self.plot.__class__ = XPlot
        if legend_location is None:
            self.plot.legend_location = self.method().legend_location
        else:
            self.plot.legend_location = legend_location
        self.plot.__init_xplot__(self.method.__self__, bounds)
        self.plot.plot_pyqtgraph(show=False, only_widget=True)
        # self.plot.pw_pg.addItem(self.bounds_widget)

        self.layout_tab = QVBoxLayout()
        self.layout_tab.addWidget(self.plot.pw_pg)
        self.setLayout(self.layout_tab)

    def update_data(self, mcard=None):
        self.plot.data = self.method(mcard=mcard).data

    def refresh(self, mcard=None):
        self.update_data(mcard=mcard)
        self.plot.update_lines()
        if self.plot_bounds:
            self.plot.update_bounds()


class OpSelectorWidget(QWidget):
    def __init__(self, method, new=False, mcard=None, bounds=None):
        super().__init__()
        self.method = method
        try:
            self.plot = self.method(mcard=mcard, calc_all=True)
        except TypeError as err:
            raise IOError(
                "DMT -> OpSelectorPlot: method" + str(method) + " did not return a valid plot."
            ) from err

        if new:
            self.plot.num = self.plot.num + "_"
            self.plot.name = "op selector plot " + self.plot.name

        self.name = self.plot.name
        self.plot_bounds = 0

        self.plot.__class__ = OpSelectorPlot
        self.plot.legend_location = self.method().legend_location
        self.plot.__init_plot__(self.method.__self__, bounds)
        self.plot.plot_pyqtgraph(show=False, only_widget=True)

        self.layout_tab = QVBoxLayout()
        self.layout_tab.addWidget(self.plot.pw_pg)
        self.setLayout(self.layout_tab)

    def update_data(self, mcard=None):
        self.plot.data = self.method(mcard=mcard).data

    def refresh(self, mcard=None):
        self.update_data(mcard=mcard)
        self.plot.update_lines()
        if self.plot_bounds:
            self.plot.update_bounds()


class OptimizationWidget(QFrame):
    """This is the Main Widget for a single xstep.

    Parameters
    ----------
    xstep             :  DMT.XStep()
        The extraction step that is to be displayed by this widget.
    status_bar        : QStatusBar()
        This is the status_bar of the QMainWindow.
    window_layout     : QHBoxLayout()
        The top layout of this widget.
    para_editor       : DMT.ParaEditBox()
    canvas            : DMT.OptimizationPlotWidget()
    bounds_widget     : DMT.BoundsWidget()
    extraction_status : DMT.ExtractionStatusWidget()

    Methods
    -------
    process()
        Called during extraction in order to update the status bar.
    replot()
        This method invokes a recalculation and replot of the plots using the currently displayed ParaEditBox values.
    extract()
        This method starts the extraction of the XStep object.
    refresh()
        This clears the status_bar after the finish signal is emitted.
    stop()
        This method is called after the stop signal has been emitted.
    cancel()
        This method is called after the cancel signal has been emitted.
    save()
        Save button callback.
    quit()
        Quit button callback.
    get_inactive_paras()
        This method returns all parameters of the ParaEditBox widget that are set inactive.
    """

    def __init__(self, xstep, xtraction=None):
        super().__init__()
        self.setFrameStyle(QFrame.Plain)
        self.setLineWidth(1)
        self.setFrameStyle(QFrame.Box | QFrame.Sunken)

        # layouts
        self.window_layout = QHBoxLayout()  # Windows Layout is the one that contains everything
        self.window_layout.setContentsMargins(5, 5, 5, 5)  # 10 #important for nice look
        self.plots_layout = QVBoxLayout()
        self.plots_layout.setContentsMargins(5, 5, 5, 5)  # 10 #important for nice look

        self.xstep = xstep

        # optimization options widget
        self.optimization_options_widget = OptimizationOptionsWidget(self.xstep)

        # main_plot
        if not self.xstep.plot_methods:
            raise IOError(
                "The XStep class "
                + str(xstep.__class__)
                + " does not define a plot.\n"
                + "Make sure at least the main_plot is decorated with the DMT.extraction.x_step.plot decorator."
            )

        self.plot = PlotWidget(
            self.xstep.plot_methods[0], mcard=self.xstep.mcard, bounds=self.xstep.x_bounds
        )
        # op selection plot
        if self.xstep.op_selector:
            self.op_selection_plot = OpSelectorWidget(
                self.xstep.op_selection_plot,
                mcard=self.xstep.mcard,
                bounds=[self.xstep.op_selector_bounds],
            )

        # parameter view imbedded into a qscrollarea
        # But not for QSteps
        if not isinstance(self.xstep, QStep):
            self.para_editor = ParaEditBox(xstep, xtraction=xtraction)

        # Equation view
        tex_string = xstep.get_tex()
        tex_string = tex_string.lstrip()
        if (
            not "begin" in tex_string and tex_string
        ):  # if a tex environment is in the string, we dont need to add $
            if not tex_string.startswith("$"):
                tex_string = "$" + tex_string

            if not tex_string.endswith("$"):
                tex_string = tex_string + "$"

        equ_lbl = EquationWidget(tex_string)

        # Status
        self.extraction_status = None
        if xtraction is None:
            self.extraction_status = ExtractionStatusWidget(self)
            self.extraction_status.setStep(xstep)

        # fill global layout
        layout_options = QGridLayout()
        layout_options.setContentsMargins(20, 20, 20, 20)

        # add widget to right hand layout
        self.plots_layout.addWidget(self.plot)
        if self.xstep.op_selector:
            self.plots_layout.addWidget(self.op_selection_plot)
        self.window_layout.addLayout(self.plots_layout)

        self.status = QGroupBox()
        # self.status.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        # self.mcard_widget   = MCardWidgetStep(self.xstep)

        scrollArea = QScrollArea()
        scrollArea.setWidget(self.plot.plot.bounds_widget)
        # scrollArea.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.layout_options = QVBoxLayout()
        self.layout_options.addWidget(equ_lbl, alignment=Qt.AlignTop)
        if not isinstance(self.xstep, QStep):
            self.layout_options.addWidget(self.para_editor, alignment=Qt.AlignTop)

        self.layout_options.addWidget(scrollArea, alignment=Qt.AlignTop)
        self.layout_options.addWidget(self.optimization_options_widget, alignment=Qt.AlignBottom)
        if xtraction is None:
            self.layout_options.addWidget(self.extraction_status, alignment=Qt.AlignBottom)

        # self.tabs_rhs.addTab(options, 'Extraction Settings')
        self.status.setLayout(self.layout_options)
        self.status.setMaximumWidth(700)

        self.window_layout.addWidget(self.status)
        self.setLayout(self.window_layout)

    def refresh(self):
        if not isinstance(self.xstep, QStep):
            self.para_editor.refresh()

        self.optimization_options_widget.refresh()
        self.plot.refresh()
        if self.xstep.op_selector:
            self.op_selection_plot.refresh()
        if self.extraction_status is not None:
            self.extraction_status.reset()  # update the progress bar

    def update_bounds_widget(self):
        self.layout_options.addWidget(
            self.xstep.canvas.gui_plot.bounds_widget, 2, 0, 1, 2, alignment=Qt.AlignTop
        )

    def process(self):
        """Called during extraction in order to update the status bar."""
        self.extraction_status.process()  # update the progress bar

    def get_inactive_paras(self):
        """This method returns all parameters of the ParaEditBox widget that are set inactive."""
        return self.para_editor.get_inactive_paras()

    def close(self):
        self.canvas.main_plot.fig.clf()
        for plot in self.canvas.other_plots:
            plot["fig"].clf()

    def replot(self):
        self.canvas.refresh()


class EquationWidget(QWidget):
    """Small helper class that displays a tex file using the renderer from matplotlib to generate a QPixmap and a QLabel to show it."""

    def __init__(self, txt):
        super().__init__()
        layout = QVBoxLayout()
        pixmap = mathTex_to_QPixmap(txt, 12, textcolor=QPalette().windowText().color().getRgbF())

        title = QLabel("Model Equation")
        title.setFont(QFont("Times", 14, QFont.Bold))

        equ_lbl = QLabel()
        equ_lbl.setPixmap(pixmap)

        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addWidget(equ_lbl, alignment=Qt.AlignCenter)

        self.setLayout(layout)


class ParaGlobalEditWidget(object):
    """A ParaGlobalEditWidget allows to manipulate values of the global and local McParameter objects

    Parameters
    ----------
    name      :  str
        The name of the parameter.
    para      :  DMT.MCardParameter
        A MCardParameter object that shall be controlled with this widget.
    is_active : bool()
        This boolean can be set using the box. If it is False, this parameter shall be exclueded from the optimization.
    label     : QLabel
        This is the QLabel of this parameter.
    sp_value  : ScientificDoubleSpinBox()
        This SpinBox subclass is used to manipulate the value of the McParameter object.
    box       : QCheckBox()
        This box is used to set the is_active attribute.
    widgets   : []
        This list contains all widgets that belong to one McParameter.

    Methods
    -------
    valuechange()
        Called upon change of the spinbox that controls McParameter.value .
    set_active()
        Called upon a change of the setChecked of the box.
    refresh()
        Used to sync with the parameter currently active in xstep.
    """

    def __init__(self, extraction, step, para):
        self.local_para = None
        self.global_para = None
        self.para = para
        self.step = step
        self.extraction = extraction

        self.label = QLabel(self.para.name)

        self.sp_local_value, self.sp_global_value = (
            ScientificDoubleSpinBox(),
            ScientificDoubleSpinBox(),
        )
        self.sp_local_value.setRange(-np.inf, np.inf)
        self.sp_global_value.setRange(-np.inf, np.inf)
        self.sp_local_value.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.sp_global_value.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.sp_local_value.setReadOnly(True)
        self.sp_global_value.setReadOnly(True)

        self.refresh()

        self.widgets = [self.label, self.sp_local_value, self.sp_global_value]

    def refresh(self):
        """Sync the currently value with the para.value ."""
        self.global_para = self.extraction.mcard.get(self.para)
        self.local_para = self.step.mcard.get(self.para)
        self.sp_local_value.setValue(self.local_para.value)
        self.sp_global_value.setValue(self.global_para.value)


class ParaValueEditWidget(QObject):
    """A ParaValueEditWidget allows to manipulate one McParameter object.

    Parameters
    ----------
    name      :  str
        The name of the parameter.
    para      :  DMT.MCardParameter
        A MCardParameter object that shall be controlled with this widget.
    is_active : bool()
        This boolean can be set using the box. If it is False, this parameter shall be exclueded from the optimization.
    label     : QLabel
        This is the QLabel of this parameter.
    sp_value  : ScientificDoubleSpinBox()
        This SpinBox subclass is used to manipulate the value of the McParameter object.
    box       : QCheckBox()
        This box is used to set the is_active attribute.
    widgets   : []
        This list contains all widgets that belong to one McParameter.

    Methods
    -------
    valuechange()
        Called upon change of the spinbox that controls McParameter.value .
    set_active()
        Called upon a change of the setChecked of the box.
    refresh()
        Used to sync with the parameter currently active in xstep.
    """

    valueChanged = Signal()

    def __init__(self, step, para, is_active=True, is_editable=True):
        QObject.__init__(self)
        self.step = step
        self.para = copy.deepcopy(para)  # mvc design pattern
        self.name = para.name
        self.is_active = is_active
        self.is_editable = is_editable

        self.label = QLabel(self.name)

        self.sp_value = ScientificDoubleSpinBox()
        if not is_editable:
            pal = self.sp_value.palette()
            pal.setColor(QPalette.Base, Qt.gray)
            self.sp_value.setPalette(pal)
            self.sp_value.setReadOnly(True)
        self.sp_value.setRange(-np.inf, np.inf)
        # self.sp_value.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.box = QCheckBox()
        if not is_editable:
            pal = self.sp_value.palette()
            pal.setColor(QPalette.Base, Qt.gray)
            self.box.setPalette(pal)
            self.box.setCheckable(False)

        self.push = copy.deepcopy(self.is_active)  # default: all active parameters will be pushed
        self.push_box = QCheckBox()

        self.widgets = [self.label, self.sp_value, self.box, self.push_box]

        self.refresh()

        self.sp_value.editingFinished.connect(self.valuechange)
        self.push_box.stateChanged.connect(self.set_push)
        self.box.stateChanged.connect(self.set_active)

    def valuechange(self):
        """This function is called in case the spinbox value is changed."""
        self.para = copy.deepcopy(self.step.mcard.get(self.para))
        if self.para.value == self.sp_value.value():
            return
        try:
            self.para.value = self.sp_value.value()
        except (ValueTooSmallError, ValueTooLargeError):
            self.sp_value.setValue(self.para.value)

        undo_stack.push(SetPara(self.step, self.para))

    def set_active(self):
        """This function is called in case the box is checked or unchecked."""
        undo_stack.push(SetParaActive(self.step, self.para, self.box))

    def set_push(self):
        """This function is called in case the box is checked or unchecked."""
        undo_stack.push(SetParaPush(self.step, self.para, self.push_box))

    def refresh(self):
        """Sync the currently value with the para.value ."""
        self.para = copy.deepcopy(self.step.mcard.get(self.para))
        self.box.setChecked(
            self.para in self.step.paras_to_optimize
            or self.para.name in self.step.paras_derived.name
        )
        self.push_box.setChecked(
            self.para in self.step.paras_to_push or self.para.name in self.step.paras_derived.name
        )
        self.sp_value.setValue(self.para.value)


class ParaBoundsEditWidget(QObject):
    """ParaBoundsEditWidgets are used to manipulate the bounds of MCardParameter objects.

    Parameters
    ----------
    name    :  str
        The name of the parameter.
    para    :  DMT.MCardParameter
        A MCardParameter object that shall be controlled with this widget.
    min     : float()
        This variable contains the lower boundary of the Parameter.
    max     : float()
        This variable contains the high boundary of the Parameter.
    sp_min  : QLineEdit()
        This LineEdit controls the low attribute of the Parameter.
    sp_max  : QLineEdit()
        This LineEdit controls the high attribute of the Parameter.
    widgets : []
        This list contains all widgets that belong to a ParaBoundsEditWidget.

    Methods
    -------
    valuechange_min()
        This method is called upon a change of the sp_low LineEdit.
    valuechange_max()
        This method is called upon a change of the sp_high LineEdit.
    refresh()
        This method syncs the LineEdit string with the currently stored x_bounds object.
    """

    boundsChanged = Signal()

    def __init__(self, step, para):
        QObject.__init__(self)
        self.step = step
        self.para = para  # mvc design pattern

        self.label = QLabel(self.para.name)
        self.sp_min = QLineEdit()
        self.sp_max = QLineEdit()
        self.widgets = [self.label, self.sp_min, self.sp_max]

        self.refresh()

        self.sp_min.editingFinished.connect(self.valuechange_min)
        self.sp_max.editingFinished.connect(self.valuechange_max)

    def valuechange_min(self):
        """This function is called in case the sp_min value is changed."""
        self.para = self.step.mcard.get(self.para)  # mvc design pattern
        if self.sp_min.text() == "None":
            self.para.min = float("nan")
        else:
            try:
                if self.para.min == float(self.sp_min.text()):
                    return

                self.para.min = float(self.sp_min.text())
            except BoundsError:
                pass

        self.sp_min.setText(format_float(self.para.min))
        undo_stack.push(SetPara(self.step, self.para))

    def valuechange_max(self):
        """This function is called in case the sp_max value is changed."""
        self.para = self.step.mcard.get(self.para)
        if self.sp_max.text() == "None":
            self.para.max = float("nan")
        else:
            try:
                if self.para.max == float(self.sp_max.text()):
                    return

                self.para.max = float(self.sp_max.text())
            except BoundsError:
                pass

        self.sp_max.setText(format_float(self.para.max))
        undo_stack.push(SetPara(self.step, self.para))

    def refresh(self):
        self.para = copy.deepcopy(self.step.mcard.get(self.para.name))  # mvc design pattern
        self.sp_min.setText(format_float(self.para.min))
        self.sp_max.setText(format_float(self.para.max))


class ParaEditBox(QWidget):
    """The ParaEditBox holds the ParaEditWidgets that are used to manipulate MCardParameter objects.

    Parameters
    ----------
    modelcard  :  DMT.MCard
        The current modelcard of the extraction that holds ALL MCardParameters.
    paras      :  {string:DMT.MCardParameter}
        A dictionary that containts the relevant extraction parameters with the parameters' names as keys and the corresponding parameters as values.
    parent     :  QWidget
        The parent QWidget. Not necessary, but common practice to have this as an argument.
    """

    def __init__(self, step, xtraction=None):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.tabs = QTabWidget()
        self.xtraction = xtraction

        self.step = step
        self.paras = copy.deepcopy(step.paras_possible)

        # create the parameters' value and bounds editor widgets
        self.value_editors = []
        self.bounds_editors = []
        self.global_editors = []
        for para in self.paras:
            is_active = False
            if para in step.paras_to_optimize:
                is_active = True

            is_editable = True
            if para in step.paras_derived:  # derived paras can not be edited
                is_editable = False
                is_active = True

            self.value_editors.append(
                ParaValueEditWidget(step, para, is_active=is_active, is_editable=is_editable)
            )
            self.bounds_editors.append(ParaBoundsEditWidget(step, para))

        if self.xtraction:
            for para in self.paras:
                try:
                    para_global = self.xtraction.mcard.get(para.name)
                except KeyError:
                    self.xtraction.mcard.add(para)
                    para_global = self.xtraction.mcard.get(para.name)

                self.global_editors.append(ParaGlobalEditWidget(self.xtraction, step, para))

        lbl_title = QLabel("Extraction Parameters")
        lbl_title.setFont(QFont("Times", 14, QFont.Bold))
        self.layout.addWidget(lbl_title, alignment=Qt.AlignCenter)

        # value editor tab --------------------------------------------------
        lbl_col1 = QLabel("name")
        lbl_col1.setFont(QFont("Times", 12, QFont.Bold))
        lbl_col2 = QLabel("value")
        lbl_col2.setFont(QFont("Times", 12, QFont.Bold))
        lbl_col3 = QLabel("optimize")
        lbl_col3.setFont(QFont("Times", 12, QFont.Bold))
        lbl_col4 = QLabel("push")
        lbl_col4.setFont(QFont("Times", 12, QFont.Bold))

        para_value_editor = QWidget()
        para_value_editor_layout = QGridLayout()
        para_value_editor_layout.addWidget(lbl_col1, 0, 0, 1, 1, alignment=Qt.AlignCenter)
        para_value_editor_layout.addWidget(lbl_col2, 0, 1, 1, 2, alignment=Qt.AlignCenter)
        para_value_editor_layout.addWidget(lbl_col3, 0, 3, 1, 1, alignment=Qt.AlignCenter)
        para_value_editor_layout.addWidget(lbl_col4, 0, 4, 1, 1, alignment=Qt.AlignCenter)

        for i, editor in enumerate(self.value_editors):
            widgets = editor.widgets
            para_value_editor_layout.addWidget(widgets[0], i + 1, 0, 1, 1, alignment=Qt.AlignCenter)
            para_value_editor_layout.addWidget(widgets[1], i + 1, 1, 1, 2, alignment=Qt.AlignCenter)
            para_value_editor_layout.addWidget(widgets[2], i + 1, 3, 1, 1, alignment=Qt.AlignCenter)
            para_value_editor_layout.addWidget(widgets[3], i + 1, 4, 1, 1, alignment=Qt.AlignCenter)

        para_value_editor.setLayout(para_value_editor_layout)

        scrollArea = QScrollArea()
        scrollArea.setWidget(para_value_editor)
        scrollArea.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #turns off horizontal scrolling
        self.tabs.addTab(scrollArea, "Value Editor")
        # self.tabs.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # bounds editor tab -------------------------------------------------
        lbl_col1_ = QLabel("name")
        lbl_col1_.setFont(QFont("Times", 12, QFont.Bold))
        lbl_col2_ = QLabel("min")
        lbl_col2_.setFont(QFont("Times", 12, QFont.Bold))
        lbl_col3_ = QLabel("max")
        lbl_col3_.setFont(QFont("Times", 12, QFont.Bold))

        para_bounds_editor = QWidget()
        para_bounds_editor_layout = QGridLayout()
        para_bounds_editor_layout.addWidget(lbl_col1_, 0, 0, alignment=Qt.AlignCenter)
        para_bounds_editor_layout.addWidget(lbl_col2_, 0, 1, alignment=Qt.AlignCenter)
        para_bounds_editor_layout.addWidget(lbl_col3_, 0, 2, alignment=Qt.AlignCenter)

        for i, editor in enumerate(self.bounds_editors):
            for n_col, widget in enumerate(editor.widgets):
                para_bounds_editor_layout.addWidget(widget, i + 1, n_col, alignment=Qt.AlignCenter)

        para_bounds_editor.setLayout(para_bounds_editor_layout)
        scrollArea = QScrollArea()
        scrollArea.setWidget(para_bounds_editor)
        self.tabs.addTab(scrollArea, "Bounds Editor")

        # global paras tab---------------------------
        if self.xtraction:
            lbl_col1__ = QLabel("name")
            lbl_col1__.setFont(QFont("Times", 12, QFont.Bold))
            lbl_col2__ = QLabel("local")
            lbl_col2__.setFont(QFont("Times", 12, QFont.Bold))
            lbl_col3__ = QLabel("global")
            lbl_col3__.setFont(QFont("Times", 12, QFont.Bold))

            para_global_editor = QWidget()
            para_global_editor_layout = QGridLayout()
            para_global_editor_layout.addWidget(lbl_col1__, 0, 0, alignment=Qt.AlignCenter)
            para_global_editor_layout.addWidget(lbl_col2__, 0, 1, alignment=Qt.AlignCenter)
            para_global_editor_layout.addWidget(lbl_col3__, 0, 2, alignment=Qt.AlignCenter)

            for i, editor in enumerate(self.global_editors):
                for n_col, widget in enumerate(editor.widgets):
                    para_global_editor_layout.addWidget(
                        widget, i + 1, n_col, alignment=Qt.AlignCenter
                    )

            para_global_editor.setLayout(para_global_editor_layout)
            scrollArea = QScrollArea()
            scrollArea.setWidget(para_global_editor)
            self.tabs.addTab(scrollArea, "Global Editor")

        # finally initizalize the complete layout --------
        self.layout.addWidget(self.tabs, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)

    def refresh(self):
        """Look at the current modelcard and take over the values."""
        for value_editor, bounds_editor in zip(self.value_editors, self.bounds_editors):
            value_editor.refresh()
            bounds_editor.refresh()

        if self.xtraction:
            for global_editor in self.global_editors:
                global_editor.refresh()

    def get_inactive_paras(self):
        """Return a list of all parametrs whose checkbox is checked. This allows the user to remove certain parameters from the extraction."""
        inactive_paras = []
        for editor in self.value_editors:
            if not editor.is_active:
                inactive_paras.append(editor.name)

        return inactive_paras

    def get_push_paras(self):
        """Return a list of all parametrs whose checkbox is checked. This allows the user to remove certain parameters from the extraction."""
        push_paras = []
        for editor in self.value_editors:
            if editor.push:
                push_paras.append(editor.name)

        return push_paras


# helper stuff from Stackoverflow -------------------------------
# copy pasta freshly served -------------------------------------
# ---------------------------------------------------------------

# Regular expression to find floats. Match groups are the whole string, the
# whole coefficient, the decimal part of the coefficient, and the exponent
# part.
_float_re = re.compile(r"(([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)")


def valid_float_string(string):
    match = _float_re.search(string)
    return match.groups()[0] == string if match else False


class FloatValidator(QValidator):
    def validate(self, string, position):
        if valid_float_string(string):
            return self.State.Acceptable
        if string == "" or string[position - 1] in "e.-+":
            return self.State.Intermediate
        return self.State.Invalid

    def fixup(self, text):
        match = _float_re.search(text)
        return match.groups()[0] if match else ""


class ScientificDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimum(-np.inf)
        self.setMaximum(np.inf)
        self.validator = FloatValidator()
        self.setDecimals(1000)

        # dummy call
        # Workaround for Bug in Qt 5.13, see
        # https://www.qtcentre.org/threads/70632-QSpinBox-not-shrinking-to-content
        self.setStyleSheet("QLineEdit { background-color:white }")

    def validate(self, text, position):
        return self.validator.validate(text, position), text, position

    def fixup(self, text):
        return self.validator.fixup(text)

    def valueFromText(self, text):
        return float(text)

    def textFromValue(self, value):
        return format_float(value)

    def stepBy(self, steps):
        text = self.cleanText()
        groups = _float_re.search(text).groups()
        decimal = float(groups[1])
        decimal += steps
        new_string = "{:g}".format(decimal) + (groups[3] if groups[3] else "")
        self.lineEdit().setText(new_string)

    def sizeHint(self):
        size = super().sizeHint()
        size.setWidth(size.width() * 2.5)
        return size
