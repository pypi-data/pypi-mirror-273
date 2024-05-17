# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xtraction_view_ui.ui',
# licensing of 'xtraction_view_ui.ui' applies.
#
# Created: Tue May 14 11:32:18 2019
#      by: pyside2-uic  running on qtpy 5.12.2
#
# WARNING! All changes made in this file will be lost!

from qtpy import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        # Form.resize(760, 478)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.extractButton = QtWidgets.QToolButton(Form)
        self.extractButton.setObjectName("extractButton")
        self.horizontalLayout.addWidget(self.extractButton)
        self.stopButton = QtWidgets.QToolButton(Form)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        self.undoButton = QtWidgets.QToolButton(Form)
        self.undoButton.setObjectName("undoButton")
        self.horizontalLayout.addWidget(self.undoButton)
        self.redoButton = QtWidgets.QToolButton(Form)
        self.redoButton.setObjectName("redoButton")
        self.horizontalLayout.addWidget(self.redoButton)
        self.pushButton = QtWidgets.QToolButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pullButton = QtWidgets.QToolButton(Form)
        self.pullButton.setObjectName("pullButton")
        self.horizontalLayout.addWidget(self.pullButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.extractionStatus = ExtractionStatusWidget(Form)
        self.extractionStatus.setObjectName("extractionStatus")
        self.verticalLayout.addWidget(self.extractionStatus)
        self.treeView = XtractionTreeView(Form)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.stackedWidget = QtWidgets.QStackedWidget(Form)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.horizontalLayout_2.addWidget(self.stackedWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.extractButton.setToolTip(
            QtWidgets.QApplication.translate(
                "Form", "<html><head/><body><p>Start Extraction</p></body></html>", None, -1
            )
        )
        self.extractButton.setText(QtWidgets.QApplication.translate("Form", "extract", None, -1))
        self.stopButton.setToolTip(
            QtWidgets.QApplication.translate(
                "Form", "<html><head/><body><p>Stop Extraction</p></body></html>", None, -1
            )
        )
        self.stopButton.setText(QtWidgets.QApplication.translate("Form", "...", None, -1))
        self.undoButton.setToolTip(
            QtWidgets.QApplication.translate(
                "Form", "<html><head/><body><p>Undo</p></body></html>", None, -1
            )
        )
        self.undoButton.setText(QtWidgets.QApplication.translate("Form", "...", None, -1))
        self.redoButton.setToolTip(
            QtWidgets.QApplication.translate(
                "Form", "<html><head/><body><p>Redo</p></body></html>", None, -1
            )
        )
        self.redoButton.setText(QtWidgets.QApplication.translate("Form", "...", None, -1))
        self.pushButton.setToolTip(
            QtWidgets.QApplication.translate(
                "Form",
                "<html><head/><body><p>Push checked local modelcard parameters</p></body></html>",
                None,
                -1,
            )
        )
        self.pushButton.setText(QtWidgets.QApplication.translate("Form", "...", None, -1))
        self.pullButton.setToolTip(
            QtWidgets.QApplication.translate(
                "Form",
                "<html><head/><body><p>Pull all global modelcard parameters</p></body></html>",
                None,
                -1,
            )
        )
        self.pullButton.setText(QtWidgets.QApplication.translate("Form", "...", None, -1))


# pylint: disable-all
from DMT.gui.x_step_widget import ExtractionStatusWidget
from DMT.gui.xtraction_tree_view import XtractionTreeView
