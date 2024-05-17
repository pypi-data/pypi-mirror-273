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
from qtpy.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QSizePolicy
from qtpy.QtGui import QFont, QPalette
from qtpy.QtCore import Qt

import pyqtgraph as pg
import numpy as np

import copy

from DMT.core import Plot
from DMT.extraction import XBounds, YBounds, XYBounds
from DMT.gui.commands import UpdateBounds
from DMT.gui import mathTex_to_QPixmap, undo_stack


class XPlot(Plot):
    """Extends Plot class by some stuff that is necessary for using the Plot in a GUI."""

    def __init__(self, xstep, style=None, x_label=None, y_label=None, num=0, bounds=None):
        Plot.__init__(
            self, xstep.title, style=style, x_label=x_label, y_label=y_label, num=num, bounds=None
        )
        self.__init_xplot__(xstep, bounds)

    def __init_xplot__(self, xstep, bounds):
        self.canvas = None
        self.span = None  # span selector
        self.span2 = None  # second span selector for XY bounds
        self.xstep = xstep
        self._bounds_widget = None
        self.bounds = bounds

    def plot_pyqtgraph(self, *args, **kwargs):
        try:
            self.canvas = super().plot_pyqtgraph(*args, **kwargs)
        except ValueError:
            print("The error occurred at the plot " + self.num)
            raise

        # self.canvas = FigureCanvas(self.fig)
        # self.canvas.setStyleSheet("background-color:transparent;") # pylint: disable=no-member
        # self.canvas.draw_idle()
        self.connect()  # connect the plot with the span selector

    def update_lines(self):
        for line, dict_line in zip(self.pw_pg.getPlotItem().listDataItems(), self.data):
            if self.x_axis_scale == "log":
                x = np.abs(dict_line["x"]) * self.x_scale
            else:
                x = np.real(dict_line["x"]) * self.x_scale

            if self.y_axis_scale == "log":
                y = np.abs(dict_line["y"]) * self.y_scale
            else:
                y = np.real(dict_line["y"]) * self.y_scale
            line.setData(x, y)

    @property
    def bounds_widget(self):
        if self._bounds_widget is None:
            self._bounds_widget = BoundsWidget(self)

        return self._bounds_widget

    def connect(self):
        """Connect the rectangle selector from matplotlib with the line_select_callback function and the correct plot's FigureCanvas."""
        try:
            lows = [bound.low for bound in self.bounds]
            highs = [bound.high for bound in self.bounds]
        except TypeError:  # some plots have no bounds
            return

        if not lows and not highs:
            return

        if all(isinstance(bound, XBounds) for bound in self.bounds):
            # get lowest and highest point in bounds
            x_low = np.min([low for low in lows])
            x_high = np.max([high for high in highs])
            d_x = np.abs(x_high - x_low)

            self.span = pg.LinearRegionItem(orientation="vertical")
            if self.x_axis_scale == "log":
                self.span.setRegion(
                    (np.log10(x_low * self.x_scale), np.log10(x_high * self.x_scale))
                )
            else:  # linear
                # increase slightly for smooth look
                d_x = d_x * 1.1
                x_low = x_low - d_x * 0.05
                x_high = x_high + d_x * 0.05
                self.span.setRegion((x_low * self.x_scale, x_high * self.x_scale))
            self.span.sigRegionChangeFinished.connect(self.line_select_callback)

        elif all(isinstance(bound, YBounds) for bound in self.bounds):
            # get lowest and highest point in bounds
            y_low = np.min([low for low in lows])
            y_high = np.max([high for high in highs])
            d_y = np.abs(y_high - y_low)

            self.span = pg.LinearRegionItem(orientation="horizontal")

            # increase slightly for smooth look
            if self.y_axis_scale == "log":
                self.span.setRegion(
                    (
                        np.log10(np.abs(y_low) * self.y_scale),
                        np.log10(np.abs(y_high) * self.y_scale),
                    )
                )
            else:  # linear
                d_y = d_y * 1.1
                y_low = y_low - d_y * 0.05
                y_high = y_high + d_y * 0.05
                self.span.setRegion((y_low * self.y_scale, y_high * self.y_scale))

            self.span.sigRegionChangeFinished.connect(self.line_select_callback)

        elif all(isinstance(bound, XYBounds) for bound in self.bounds):
            self.span = pg.ROI((0, 0), pen=(255, 69, 0))
            self.span.addScaleHandle((0, 0), (0.5, 0.5))
            self.span.addScaleHandle((1, 1), (0.5, 0.5))
            # get lowest and highest point in bounds
            x_low = np.min([low[0] for low in lows])
            y_low = np.min([low[1] for low in lows])
            x_high = np.max([high[0] for high in highs])
            y_high = np.max([high[1] for high in highs])

            xmin = x_low * self.x_scale
            xmax = x_high * self.x_scale
            ymin = y_low * self.y_scale
            ymax = y_high * self.y_scale
            if self.x_axis_scale == "log":
                xmin = np.log10(xmin)
                xmax = np.log10(xmax)
            if self.y_axis_scale == "log":
                ymin = np.log10(ymin)
                ymax = np.log10(ymax)

            d_x = np.abs(xmax - xmin)
            d_y = np.abs(ymax - ymin)

            # increase slightly for smooth look
            if not self.x_axis_scale == "log":
                d_x = d_x * 1.01
                xmin = xmin - d_x * 0.005

            if not self.y_axis_scale == "log":
                d_y = d_y * 1.01
                ymin = ymin - d_y * 0.005

            # delta_x = d_x*self.x_scale #scaled and accounted for axis scale
            # delta_y = d_y*self.y_scale #scaled and accounted for axis scale

            self.span.setPos((xmin, ymin), finish=False)
            self.span.setSize((d_x, d_y), finish=False)
            self.span.sigRegionChangeFinished.connect(self.rectangle_select_callback)

        else:
            raise IOError("DMT->XPlot: Bounds class not known.")

        self.pw_pg.addItem(self.span)

    def rectangle_select_callback(self, _span):
        """Callback function that is called upon clicking and holding the left mouse button in a matplotlib FigureCanvas with the rectangle selector."""
        # read
        rect = self.span.parentBounds()

        p_min = rect.bottomLeft()
        x_min = p_min.x()
        y_min = p_min.y()
        p_max = rect.topRight()
        x_max = p_max.x()
        y_max = p_max.y()

        # switch
        if x_min > x_max:
            x_max, x_min = x_min, x_max
        if y_min > y_max:
            y_max, y_min = y_min, y_max

        if self.x_axis_scale == "log":
            x_max, x_min = 10**x_max, 10**x_min
        if self.y_axis_scale == "log":
            y_max, y_min = 10**y_max, 10**y_min

        for bounds_editor in self.bounds_widget.x_bounds_editors:
            minimum = ((x_min / bounds_editor.scale[0]), (y_min / bounds_editor.scale[1]))
            maximum = ((x_max / bounds_editor.scale[0]), (y_max / bounds_editor.scale[1]))
            bounds_editor.set(minimum, maximum)

        self.bounds_widget.update_bounds()

    def line_select_callback(self, span):
        """Callback function that is called upon clicking and holding the left mouse button in a matplotlib FigureCanvas with the span selectors."""
        scale = None  # pyqtgraph scales its output data...catch this here
        if self.span.orientation == "horizontal":
            try:  # catch bug due to different QT versions
                scale = bool(self.pw_pg.centralWidget.ctrl.logYCheck.checkState().value)
            except AttributeError:
                scale = bool(self.pw_pg.centralWidget.ctrl.logYCheck.checkState())
        else:
            try:  # catch bug due to different QT versions
                scale = bool(self.pw_pg.centralWidget.ctrl.logXCheck.checkState().value)
            except AttributeError:
                scale = bool(self.pw_pg.centralWidget.ctrl.logXCheck.checkState())

        x1, x2 = span.getRegion()
        if scale:
            x1 = 10**x1
            x2 = 10**x2

        # in case the boundaries have been selected the wrong way, swap
        if not x1 < x2:
            x1, x2 = x2, x1

        for bounds_editor in self.bounds_widget.x_bounds_editors:
            low = x1 / bounds_editor.scale
            high = x2 / bounds_editor.scale
            bounds_editor.set(low, high)

        self.bounds_widget.update_bounds()


class BoundsWidget(QWidget):
    """This widget displays the currently active bounds for the extraction.

    Parameters
    ----------
    bounds : [float()]
        The extraction step's active bounds.
    """

    def __init__(self, xplot):
        # lengthy code selected on purpose here to increase readability
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.xplot = xplot
        self.xstep = xplot.xstep

        if self.xstep.bounds_class == XBounds:
            self.scale = self.xstep.main_fig.x_scale
        elif self.xstep.bounds_class == YBounds:
            self.scale = self.xstep.main_fig.y_scale
        elif self.xstep.bounds_class == XYBounds:
            self.scale = (self.xstep.main_fig.x_scale, self.xstep.main_fig.y_scale)

        self.x_bounds_editors = []

        # create all widgets
        for label, x_bounds in zip(self.xstep.labels, self.xstep.x_bounds):
            bounds_editor = BoundsEditor(self, x_bounds, self.scale, label)
            self.x_bounds_editors.append(bounds_editor)

        if all(isinstance(bounds, XBounds) for bounds in self.xstep.x_bounds):
            lbl_bounds = QLabel("Selected X Boundaries")
        elif all(isinstance(bounds, YBounds) for bounds in self.xstep.x_bounds):
            lbl_bounds = QLabel("Selected Y Boundaries")
        elif all(isinstance(bounds, XYBounds) for bounds in self.xstep.x_bounds):
            lbl_bounds = QLabel("Selected XY Boundaries")

        lbl_bounds.setFont(QFont("Times", 14, QFont.Bold))
        self.layout.addWidget(lbl_bounds, alignment=Qt.AlignCenter)

        # place the widgets in the layout
        for bounds_editor in self.x_bounds_editors:
            self.layout.addWidget(bounds_editor)

        self.setLayout(self.layout)

    def update_bounds(self):
        # tale over the xbounds from the widgets
        new_bounds = []
        for widget in self.x_bounds_editors:
            new_bounds.append(widget.x_bounds)

        undo_stack.push(UpdateBounds(self.xstep, self, new_bounds))

    def set_bounds(self, bounds):
        self.xstep.x_bounds = bounds
        for editor, bound in zip(self.x_bounds_editors, self.xstep.x_bounds):
            editor.set(bound.low, bound.high)

    # def refresh(self):
    #     self.x_bounds = copy.deepcopy( self.xstep.x_bounds )
    #     for bounds_editor, x_bounds in zip(self.x_bounds_editors, self.x_bounds):
    #         bounds_editor.x_bounds = x_bounds
    #         bounds_editor.refresh()


class BoundsEditor(QWidget):
    def __init__(self, box, x_bounds, scale, label):
        # lengthy code selected on purpose here to increase readability
        super().__init__()
        self.layout = QHBoxLayout()
        self.box = box

        self.label = QLabel()
        # textcolor = "black"
        # palette_text_color =
        # if (
        #     palette_text_color.red() > 200
        #     and palette_text_color.blue() > 200
        #     and palette_text_color.green() > 200
        # ):
        #     textcolor = "white"
        pixmap = mathTex_to_QPixmap(label, 12, textcolor=QPalette().windowText().color().getRgbF())
        self.label.setPixmap(pixmap)

        self.name_low = QLabel("low")
        self.name_high = QLabel("high")

        self.x_bounds = copy.deepcopy(x_bounds)
        self.scale = scale

        self.line_edit_low = QLineEdit()
        self.line_edit_low.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.line_edit_high = QLineEdit()
        self.line_edit_high.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.set(self.x_bounds.low, self.x_bounds.high)

        self.line_edit_low.editingFinished.connect(self.valuechange)
        self.line_edit_high.editingFinished.connect(self.valuechange)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.name_low)
        self.layout.addWidget(self.line_edit_low)
        self.layout.addWidget(self.name_high)
        self.layout.addWidget(self.line_edit_high)

        self.setLayout(self.layout)

    def valuechange(self):
        """Callback function that is called if the bounds text has been modified"""
        val_low, val_high = self.get_values_from_text()

        if self.x_bounds.low == val_low and self.x_bounds.high == val_high:
            return

        self.set(val_low, val_high)
        self.box.update_bounds()

    def set(self, low, high):
        # ensure that the valuechange due to formatting does not let this recast bounds
        if isinstance(self.x_bounds, XYBounds):  # separated by space..
            self.line_edit_low.setText(
                f"{low[0]*self.scale[0]:.4g}" + "   " + f"{low[1]*self.scale[1]:.4g}"
            )
            self.line_edit_high.setText(
                f"{high[0]*self.scale[0]:.4g}" + "   " + f"{high[1]*self.scale[1]:.4g}"
            )
        else:
            self.line_edit_low.setText(f"{low*self.scale:.4g}")
            self.line_edit_high.setText(f"{high*self.scale:.4g}")

        # there might be a scale bug here
        val_low, val_high = self.get_values_from_text()

        self.x_bounds.low = val_low
        self.x_bounds.high = val_high

    def get_values_from_text(self):
        if isinstance(self.x_bounds, XYBounds):  # separated by space..
            str_low = self.line_edit_low.displayText().split()
            val_low = (float(str_low[0]) / self.scale[0], float(str_low[1]) / self.scale[1])
            str_high = self.line_edit_high.displayText().split()
            val_high = (float(str_high[0]) / self.scale[0], float(str_high[1]) / self.scale[1])
        else:
            val_low = float(self.line_edit_low.displayText()) / self.scale
            val_high = float(self.line_edit_high.displayText()) / self.scale

        return val_low, val_high


class OpSelectorPlot(Plot):
    """Extends Plot class by some stuff that is necessary for using the Plot in a GUI."""

    def __init__(self, xstep, style=None, x_label=None, y_label=None, num=0):
        Plot.__init__(
            self, xstep.title, style=style, x_label=x_label, y_label=y_label, num=num, bounds=None
        )
        self.__init_xplot__(xstep, bounds)

    def __init_plot__(self, xstep, bounds):
        self.canvas = None
        self.span = None  # span selector
        self.xstep = xstep
        self.bounds = bounds

    def plot_pyqtgraph(self, *args, **kwargs):
        try:
            self.canvas = super().plot_pyqtgraph(*args, **kwargs)
        except ValueError:
            print("The error occurred at the plot " + self.num)
            raise

        self.connect()  # connect the plot with the span selector

    def update_lines(self):
        for line, dict_line in zip(self.pw_pg.getPlotItem().listDataItems(), self.data):
            line.setData(dict_line["x"] * self.x_scale, dict_line["y"] * self.y_scale)

    def connect(self):
        """Connect the rectangle selector from matplotlib with the line_select_callback function and the correct plot's FigureCanvas."""
        if self.span is None:
            lows = [bound.low for bound in self.bounds]
            highs = [bound.high for bound in self.bounds]
            # get lowest and highest point in bounds
            x_low = np.min([low for low in lows])
            x_high = np.max([high for high in highs])
            d_x = np.abs(x_high - x_low)

            # increase slightly for smooth look
            d_x = d_x * 1.1
            x_low = x_low - d_x * 0.05
            x_high = x_high + d_x * 0.05

            self.span = pg.LinearRegionItem(orientation="vertical")
            self.span.setRegion((x_low * self.x_scale, x_high * self.x_scale))
            self.span.sigRegionChangeFinished.connect(self.line_select_callback)
            self.pw_pg.addItem(self.span)

    def line_select_callback(self, span):
        """Callback function that is called upon clicking and holding the left mouse button in a matplotlib FigureCanvas with the span selectors."""
        x1, x2 = span.getRegion()
        # in case the boundaries have been selected the wrong way, swap
        if not x1 < x2:
            x1, x2 = x2, x1

        self.xstep.op_selector_bounds.low = x1
        self.xstep.op_selector_bounds.high = x2

        # calculate average and update
        x_data = self.data[0]["x"]
        y_data = self.data[0]["y"]
        bool_array = (x_data * self.x_scale >= x1) & (x_data * self.x_scale <= x2)
        y_data_new = y_data[bool_array]
        para_obj = self.xstep.mcard[self.xstep.op_selector_para]
        para_obj.value = np.average(y_data_new)
        self.xstep.mcard.set(para_obj)
        self.xstep.mcardChanged.emit()
        # print('id of mcard in Xplot.line_select_callback: ' + str(id(self.xstep.mcard)))
