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
import re
import matplotlib

from matplotlib.backends.backend_agg import FigureCanvasAgg
from qtpy.QtCore import Qt
from qtpy.QtGui import QImage, QPixmap
from qtpy.QtWidgets import (
    QTabWidget,
    QTabBar,
    QStylePainter,
    QStyleOptionTab,
    QStyle,
    QStackedWidget,
    QWidget,
)


def mathTex_to_QPixmap(mathTex, fs, textcolor="black"):
    """Copied from Stackoverflow. Creates a figure from a tex expression that can be displayed in PyQt. Taken from https://stackoverflow.com/questions/32035251/displaying-latex-in-pyqt-pyside-qtablewidget"""
    # ---- set up a mpl figure instance ----
    # matplotlib.pyplot.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx}') # do not touch the rc file anywhere except in plot.py

    fig = matplotlib.figure.Figure()
    fig.patch.set_facecolor("none")
    fig.set_canvas(FigureCanvasAgg(fig))
    renderer = fig.canvas.get_renderer()

    # ---- plot the mathTex expression ----

    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.patch.set_facecolor("none")
    t = ax.text(
        0,
        0,
        mathTex,
        horizontalalignment="left",
        verticalalignment="bottom",
        fontsize=fs,
        color=textcolor,
    )

    # ---- fit figure size to text artist ----

    fwidth, fheight = fig.get_size_inches()
    fig_bbox = fig.get_window_extent(renderer)

    text_bbox = t.get_window_extent(renderer)

    tight_fwidth = text_bbox.width * fwidth / fig_bbox.width
    tight_fheight = text_bbox.height * fheight / fig_bbox.height

    fig.set_size_inches(tight_fwidth * 1.1, tight_fheight * 1.1)

    # ---- convert mpl figure to QPixmap ----

    buf, size = fig.canvas.print_to_buffer()
    qimage = QImage.rgbSwapped(QImage(buf, size[0], size[1], QImage.Format_ARGB32))
    qpixmap = QPixmap(qimage)

    return qpixmap


class HorizontalTabBar(QTabBar):
    def paintEvent(self, event):
        # pylint: disable=unused-argument
        painter = QStylePainter(self)
        option = QStyleOptionTab()
        for index in range(self.count()):
            self.initStyleOption(option, index)
            painter.drawControl(QStyle.CE_TabBarTabShape, option)
            painter.drawText(
                self.tabRect(index), Qt.AlignCenter | Qt.TextDontClip, self.tabText(index)
            )

    def tabSizeHint(self, index):
        size = QTabBar.tabSizeHint(self, index)
        size.setHeight(20)
        size.setWidth(200)
        return size


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)
        self.setTabBar(HorizontalTabBar())
        self.setTabPosition(QTabWidget.West)


class CenterTabView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.stack = QStackedWidget()
        self.optimization_tabs = HorizontalTabBar()
        self.optimization_tabs.setExpanding(False)
        self.global_tabs = HorizontalTabBar()
        self.global_tabs.setExpanding(False)
        self.optimization_tabs.setShape(QTabBar.RoundedWest)
        self.global_tabs.setShape(QTabBar.RoundedWest)

    def addOptimizationWidget(self, step, widget):
        self.stack.addWidget(widget)
        self.optimization_tabs.addTab(step.name)
        self.global_tabs.addTab(step.name)


def format_float(value):
    """Modified form of the 'g' format specifier."""
    string = f"{value:g}".replace("e+", "e")
    string = re.sub(r"e(-?)0*(\d+)", r"e\1\2", string)
    return string
