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
import sys
import logging
import _pickle as cpickle
from pathlib import Path
from qtpy.QtWidgets import QApplication, QMainWindow, QMessageBox
from qtpy.QtCore import Signal, Qt

# pyside2-uic main_window.ui -o main_window.py

from DMT.external import slugify
from DMT.config import DATA_CONFIG
from DMT.extraction import Xtraction, DocuXtraction
from DMT.gui import file_dialog, OptimizationWidget, PlotsWidget
from DMT.gui.main_window import Ui_MainWindow

matplotlib_logger = logging.getLogger("matplotlib")  # disable matplotlib logging
matplotlib_logger.setLevel(logging.CRITICAL)
matplotlib_tex = logging.getLogger("matplotlib.texmanager")
matplotlib_tex.setLevel(logging.CRITICAL)


class XtractionGUI(QMainWindow, Ui_MainWindow):
    loadedXtraction = Signal(Xtraction)  # Signal with a pointer to the Xtraction object.

    def __init__(self, extraction=None):
        if not QApplication.instance():
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()

        super().__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        self.extraction = None

        # connect Actions, which is not possible in QtDesigner
        # lambdas are needed here, if not given, then somehow self.extraction is transformed into a PyCapsule object which can not be pickled...
        self.actionLoadXtraction.triggered.connect(self.loadXtraction)
        # self.actionSaveXtraction.triggered.connect(
        #     lambda: self.extraction.save()
        # )  # pylint: disable=unnecessary-lambda
        self.actionLoad_MCard.triggered.connect(self.load_mcard)
        self.actionSave_MCard.triggered.connect(self.save_mcard)

        self.actionSave_Figures.triggered.connect(self.save_figures)
        self.actionTikz.triggered.connect(lambda: self.save_curr_figure_as(extension="tikz"))
        self.actionPng.triggered.connect(lambda: self.save_curr_figure_as(extension="png"))
        self.actionCreate_XDoc.triggered.connect(self.create_xdoc)
        # self.actionScale_all.triggered.connect(
        #     lambda: self.extraction.technology.scaleAll(self.extraction.mcard)
        # )
        # self.actionScale_capacitances.triggered.connect(
        #     lambda: self.extraction.technology.scaleCapacitances(self.extraction.mcard)
        # )
        # self.actionScale_capacitances.triggered.connect(
        #     lambda: self.extraction.technology.scaleResistances(self.extraction.mcard)
        # )

        self.xtraction_view = self.mainStack.widget(0)
        self.mcard_view = self.mainStack.widget(1)
        # self.global_plots = self.mainStack.widget(2)

        # #connect self signals
        self.loadedXtraction[Xtraction].connect(self.xtraction_view.loadXtraction)
        self.loadedXtraction[Xtraction].connect(
            lambda xtraction: self.mcard_view.set_mcard(xtraction)
        )  # pylint: disable=unnecessary-lambda
        self.loadedXtraction[Xtraction].connect(self.global_plots.loadXtraction)
        self.showXtraction.triggered.connect(lambda: self.mainStack.setCurrentIndex(0))
        self.showMcard.triggered.connect(lambda: self.mainStack.setCurrentIndex(1))
        # self.showGlobalPlots.triggered.connect(lambda: self.mainStack.setCurrentIndex(2))

        # #connect other signals
        self.xtraction_view.statusMessage[str].connect(self.showStatusMessage)

        if extraction is not None:
            self.set_xtraction(extraction)

    def loadXtraction(self, dir_=None):
        """Load an Xtraction object into the Xtraction Gui.

        This will invoke a QFileDialog if the path is not given in dir_

        Parameters
        ----------
        dir_ : str, optional
            The path to the directory, where the Xtraction is saved.
        """
        if dir_ is None or not dir_:
            extraction_file = file_dialog()

        else:
            extraction_file = dir_

        if not extraction_file:
            return

        logging.info(
            "Xtraction Gui is loading xtraction object and will emit loadedXtraction Signal!"
        )
        self.set_xtraction(Xtraction.load(extraction_file))

    def set_xtraction(self, extraction: Xtraction):
        # remove old extraction (if needed)
        if self.extraction:
            # do something?
            pass

        # save the new extraction object
        self.extraction = extraction

        # load into the different views using the signal
        self.loadedXtraction.emit(self.extraction)

    def load_mcard(self):
        """Load a new global mcard from a saved pickle file."""
        mcard_file = file_dialog(fmt=("mcard", "*"))
        if not mcard_file:
            return

        # load the object using pickle, to preserve McParameterCollection subclass
        with open(mcard_file, "rb") as my_db:
            mcard = cpickle.load(my_db)

        # are there any parameters in the current mcard, which are not in the new? If not, add them...
        for para in self.extraction.mcard:
            if para.name not in mcard.name:
                mcard.add(para)

        # ok now overwrite the old one..
        self.extraction.mcard = mcard

        logging.info("Loaded a modelcard from %s as the new global modelcard", mcard_file)

    def save_mcard(self):
        """Save the global mcard to a pickle or a text file."""
        mcard_file = file_dialog(fmt=("json", "mcard", "txt", "*"))
        if not mcard_file:
            return

        if mcard_file.endswith("mcard"):
            self.extraction.mcard.save(mcard_file)
        elif mcard_file.endswith("txt"):
            self.extraction.mcard.print_to_file(mcard_file)
        elif mcard_file.endswith("json"):
            self.extraction.mcard.dump_json(mcard_file)
        else:
            print("DMT->GUI: Unknown file ending to save modelcards!")
            return

        logging.info("Saved the global modelcard to %s", mcard_file)

    def save_curr_figure_as(self, extension):
        directory = file_dialog(directory=DATA_CONFIG["directories"]["x_doc_dir"], isFolder=True)
        if directory is None:  # Abort value...
            return

        if directory == "":  # default value
            directory = self.extraction.dirs["save_dir"]

        widget = self.xtraction_view.currWidget
        if isinstance(widget, OptimizationWidget):
            fig = widget.plot.plot  # plot of the plot widget ... genius naming here
        elif isinstance(widget, PlotsWidget):
            fig = widget.currentWidget().plot
        else:
            raise IOError(
                "DMT -> GUI -> save_curr_figure_as : current widget type not implemented."
            )

        if directory.is_file:
            directory = directory.parent

        if extension == "tikz":
            file_name = slugify(fig.num)

            fig.legend_location = "upper right outer"
            # save one figure as tikz standalone
            fig.save_tikz(
                directory, "standalone_" + file_name, width="0.5\\textwidth", standalone=True
            )
            # save one figure for integration into other docs
            fig.save_tikz(
                directory,
                file_name,
                standalone=False,
                build=False,
                clean=False,
                mark_repeat=1,
                width=None,
                height=None,
                fontsize="normalsize",
                extension=r"tikz",
            )
        elif extension == "png":
            fig.save_png(directory)
        else:
            raise IOError("DMT -> GUI: save_curr_figure_as: extension unknown.")

    def save_figures(self):
        """Saves all figures in a location to parse"""
        directory = file_dialog(directory=self.extraction.dirs["save_dir"], isFolder=True)
        if directory is None:  # Abort value...
            return

        if directory == "":  # default value
            directory = self.extraction.dirs["save_dir"]

        root_item_xstep_views = self.xtraction_view.treeView.model().rootItem

        ## for figure in self.plots...
        for child_item in root_item_xstep_views.childItems:
            child_item.childItems[0].widget.plot.plot.save_tikz(
                directory,
                standalone=True,
                legend_location="upper right outer",
                width="0.6\\textwidth",
            )  # optimiziation widget
            # child_item.childItems[0].widget.plot.plot.save_png(directory) # optimiziation widget

            for plot_widget in child_item.childItems[1].widget.plots:
                try:
                    plot_widget.plot.save_tikz(
                        directory,
                        standalone=True,
                        legend_location="upper right outer",
                        width="0.6\\textwidth",
                    )

                except ValueError:
                    pass

    def create_xdoc(self):
        """Creates a automatic extraction documentation with the current state defined for the xtraction object by the GUI."""

        # PyQT5 BUG (MK:?)
        dir_dst = file_dialog(directory=DATA_CONFIG["directories"]["x_doc_dir"], isFolder=True)
        if dir_dst is None:
            return  # Abort value...
        elif dir_dst == "":
            dir_dst = Path(DATA_CONFIG["directories"]["x_doc_dir"]).resolve()
        self.showStatusMessage("building.")  # set the status bar

        # get DocuXtraction object:
        docu_xtraction = DocuXtraction(
            self.extraction, gui_extraction=self, dir_destination=dir_dst
        )

        # copy the template:
        docu_xtraction.copy_template()  # paths are set inside the docu object

        # create documentation
        docu_xtraction.create_subfiles()

        if DATA_CONFIG["build_doc"]:
            # compile documentation
            docu_xtraction.build()
            self.showStatusMessage("Build Autodoc.")
        else:
            # store documentation
            docu_xtraction.generate_tex()
            self.showStatusMessage("Generated Autodoc.")

    def showStatusMessage(self, message):
        self.statusbar.showMessage(message)

    def start(self):
        print("Starting DMT GUI ...")
        self.show()  # Show the form
        # self.showFullScreen()                    # Show the form
        self.app.exec_()

    def closeEvent(self, event):
        msg_box = QMessageBox()
        msg_box.setText("Do you want to exit?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Save)
        msg_box.setDefaultButton(QMessageBox.No)
        ret = msg_box.exec_()

        if ret == QMessageBox.Yes:
            # Don't save was clicked
            event.accept()
        elif ret == QMessageBox.No:
            event.ignore()
            # cancel was clicked
        elif ret == QMessageBox.Save:
            # Save was clicked
            self.extraction.save()
            event.accept()
        else:
            # should never be reached
            raise OSError("Something went wrong")


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = XtractionGUI()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == "__main__":  # if we're running file directly and not importing it
    main()  # run the main function
