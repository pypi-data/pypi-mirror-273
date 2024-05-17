# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui',
# licensing of 'main_window.ui' applies.
#
# Created: Thu Jul 18 10:44:55 2019
#      by: pyside2-uic  running on qtpy 5.13.0
#
# WARNING! All changes made in this file will be lost!

from qtpy import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(1163, 779)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.mainStack = QtWidgets.QStackedWidget(self.centralwidget)
        self.mainStack.setObjectName("mainStack")
        self.xtraction_view = XtractionView()
        self.xtraction_view.setObjectName("xtraction_view")
        self.mainStack.addWidget(self.xtraction_view)
        self.global_mcard = MCardWidget()
        self.global_mcard.setObjectName("global_mcard")
        self.mainStack.addWidget(self.global_mcard)
        self.global_plots = GlobalPlotWidget()
        self.global_plots.setObjectName("global_plots")
        self.mainStack.addWidget(self.global_plots)
        self.gridLayout.addWidget(self.mainStack, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 1163, 25))
        self.menubar.setObjectName("menubar")
        self.menuFiles = QtWidgets.QMenu(self.menubar)
        self.menuFiles.setObjectName("menuFiles")
        self.menuSave_Figure_As = QtWidgets.QMenu(self.menuFiles)
        self.menuSave_Figure_As.setObjectName("menuSave_Figure_As")
        # self.menuOptions = QtWidgets.QMenu(self.menubar)
        # self.menuOptions.setObjectName("menuOptions")
        # self.menuExtraction = QtWidgets.QMenu(self.menubar)
        # self.menuExtraction.setObjectName("menuExtraction")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        # self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMovable(False)
        self.toolBar.setOrientation(QtCore.Qt.Vertical)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.showXtraction = QtWidgets.QAction(MainWindow)
        self.showXtraction.setObjectName("showXtraction")
        # self.showDuts = QtWidgets.QAction(MainWindow)
        # self.showDuts.setObjectName("showDuts")
        self.showMcard = QtWidgets.QAction(MainWindow)
        self.showMcard.setObjectName("showMcard")
        self.showGlobalPlots = QtWidgets.QAction(MainWindow)
        self.showGlobalPlots.setObjectName("showGlobalPlots")
        self.actionLoadXtraction = QtWidgets.QAction(MainWindow)
        self.actionLoadXtraction.setObjectName("actionLoadXtraction")
        self.actionSaveXtraction = QtWidgets.QAction(MainWindow)
        self.actionSaveXtraction.setObjectName("actionSaveXtraction")
        self.actionLoadDuts = QtWidgets.QAction(MainWindow)
        self.actionLoadDuts.setObjectName("actionLoadDuts")
        self.actionImportDuts = QtWidgets.QAction(MainWindow)
        self.actionImportDuts.setObjectName("actionImportDuts")
        self.actionSaveDuts = QtWidgets.QAction(MainWindow)
        self.actionSaveDuts.setObjectName("actionSaveDuts")
        self.actionLoad_XStep = QtWidgets.QAction(MainWindow)
        self.actionLoad_XStep.setObjectName("actionLoad_XStep")
        self.actionScale_all = QtWidgets.QAction(MainWindow)
        self.actionScale_all.setObjectName("actionScale_all")
        self.actionScale_resistances = QtWidgets.QAction(MainWindow)
        self.actionScale_resistances.setObjectName("actionScale_resistances")
        self.actionScale_capacitances = QtWidgets.QAction(MainWindow)
        self.actionScale_capacitances.setObjectName("actionScale_capacitances")
        self.actionDeemb_to_internal = QtWidgets.QAction(MainWindow)
        self.actionDeemb_to_internal.setObjectName("actionDeemb_to_internal")
        self.actionSave_Figures = QtWidgets.QAction(MainWindow)
        self.actionSave_Figures.setObjectName("actionSave_Figures")
        self.actionCreate_XDoc = QtWidgets.QAction(MainWindow)
        self.actionCreate_XDoc.setObjectName("actionCreate_XDoc")
        self.actionTikz = QtWidgets.QAction(MainWindow)
        self.actionTikz.setObjectName("actionTikz")
        self.actionPng = QtWidgets.QAction(MainWindow)
        self.actionPng.setObjectName("actionPng")
        self.actionSave_MCard = QtWidgets.QAction(MainWindow)
        self.actionSave_MCard.setObjectName("actionSave_MCard")
        self.actionLoad_MCard = QtWidgets.QAction(MainWindow)
        self.actionLoad_MCard.setObjectName("actionLoad_MCard")
        self.menuSave_Figure_As.addAction(self.actionTikz)
        self.menuSave_Figure_As.addAction(self.actionPng)
        self.menuFiles.addAction(self.actionLoadXtraction)
        self.menuFiles.addAction(self.actionSaveXtraction)
        self.menuFiles.addSeparator()
        self.menuFiles.addAction(self.actionLoad_MCard)
        self.menuFiles.addAction(self.actionSave_MCard)
        self.menuFiles.addSeparator()
        self.menuFiles.addAction(self.menuSave_Figure_As.menuAction())
        self.menuFiles.addAction(self.actionSave_Figures)
        self.menuFiles.addSeparator()
        self.menuFiles.addAction(self.actionCreate_XDoc)
        # self.menuExtraction.addAction(self.actionScale_all)
        # self.menuExtraction.addAction(self.actionScale_resistances)
        # self.menuExtraction.addAction(self.actionScale_capacitances)
        # self.menuExtraction.addAction(self.actionDeemb_to_internal)
        self.menubar.addAction(self.menuFiles.menuAction())
        # self.menubar.addAction(self.menuOptions.menuAction())
        # self.menubar.addAction(self.menuExtraction.menuAction())
        self.toolBar.addAction(self.showXtraction)
        # self.toolBar.addAction(self.showDuts)
        self.toolBar.addAction(self.showMcard)
        self.toolBar.addAction(self.showGlobalPlots)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtWidgets.QApplication.translate("MainWindow", "DMT Gui 0.2", None, -1)
        )
        self.menuFiles.setTitle(QtWidgets.QApplication.translate("MainWindow", "Fi&les", None, -1))
        self.menuSave_Figure_As.setTitle(
            QtWidgets.QApplication.translate("MainWindow", "Sa&ve Figure As", None, -1)
        )
        # self.menuOptions.setTitle(
        #     QtWidgets.QApplication.translate("MainWindow", "O&ptions", None, -1)
        # )
        # self.menuExtraction.setTitle(
        #     QtWidgets.QApplication.translate("MainWindow", "Ex&traction", None, -1)
        # )
        self.toolBar.setWindowTitle(
            QtWidgets.QApplication.translate("MainWindow", "toolBar", None, -1)
        )
        self.showXtraction.setText(
            QtWidgets.QApplication.translate("MainWindow", "Xtraction", None, -1)
        )
        # self.showDuts.setText(QtWidgets.QApplication.translate("MainWindow", "DUTs", None, -1))
        self.showMcard.setText(QtWidgets.QApplication.translate("MainWindow", "MCard", None, -1))
        # self.showGlobalPlots.setText(
        #     QtWidgets.QApplication.translate("MainWindow", "Plots", None, -1)
        # )
        self.actionLoadXtraction.setText(
            QtWidgets.QApplication.translate("MainWindow", "&Load Xtraction", None, -1)
        )
        self.actionSaveXtraction.setText(
            QtWidgets.QApplication.translate("MainWindow", "&Save Xtraction", None, -1)
        )
        self.actionLoadDuts.setText(
            QtWidgets.QApplication.translate("MainWindow", "Load &Dut", None, -1)
        )
        self.actionImportDuts.setText(
            QtWidgets.QApplication.translate("MainWindow", "&Import Dut", None, -1)
        )
        self.actionSaveDuts.setText(
            QtWidgets.QApplication.translate("MainWindow", "S&ave Dut", None, -1)
        )
        self.actionLoad_XStep.setText(
            QtWidgets.QApplication.translate("MainWindow", "Load XStep", None, -1)
        )
        # self.actionScale_all.setText(
        #     QtWidgets.QApplication.translate("MainWindow", "&Scale all", None, -1)
        # )
        # self.actionScale_resistances.setText(
        #     QtWidgets.QApplication.translate("MainWindow", "Scale &resistances", None, -1)
        # )
        # self.actionScale_capacitances.setText(
        #     QtWidgets.QApplication.translate("MainWindow", "Scale &capacitances", None, -1)
        # )
        # self.actionDeemb_to_internal.setText(
        #     QtWidgets.QApplication.translate("MainWindow", "&Deemb to internal", None, -1)
        # )
        self.actionDeemb_to_internal.setToolTip(
            QtWidgets.QApplication.translate(
                "MainWindow",
                "Perform deembedding of the internal transistor according to the HICUM compact model",
                None,
                -1,
            )
        )
        self.actionSave_Figures.setText(
            QtWidgets.QApplication.translate("MainWindow", "Save &Figures", None, -1)
        )
        self.actionCreate_XDoc.setText(
            QtWidgets.QApplication.translate("MainWindow", "&Create XDoc", None, -1)
        )
        self.actionTikz.setText(QtWidgets.QApplication.translate("MainWindow", "&tikz", None, -1))
        self.actionPng.setText(QtWidgets.QApplication.translate("MainWindow", "&png", None, -1))
        self.actionSave_MCard.setText(
            QtWidgets.QApplication.translate("MainWindow", "S&ave MCard", None, -1)
        )
        self.actionSave_MCard.setToolTip(
            QtWidgets.QApplication.translate("MainWindow", "Save global MCard", None, -1)
        )
        self.actionLoad_MCard.setText(
            QtWidgets.QApplication.translate("MainWindow", "Load &MCard", None, -1)
        )
        self.actionLoad_MCard.setToolTip(
            QtWidgets.QApplication.translate("MainWindow", "Load global MCard", None, -1)
        )


from DMT.gui.mcard_widget import MCardWidget
from DMT.gui.x_step_widget import GlobalPlotWidget
from DMT.gui.xtraction_view import XtractionView
