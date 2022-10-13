# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectorwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SelectorWindow(object):
    def setupUi(self, SelectorWindow):
        SelectorWindow.setObjectName("SelectorWindow")
        SelectorWindow.resize(400, 300)
        self.centralWidget = QtWidgets.QWidget(SelectorWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.WellTree = QtWidgets.QTreeWidget(self.centralWidget)
        self.WellTree.setObjectName("WellTree")
        self.WellTree.headerItem().setText(0, "1")
        self.WellTree.header().setVisible(False)
        self.gridLayout.addWidget(self.WellTree, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        SelectorWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(SelectorWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menuBar.setObjectName("menuBar")
        SelectorWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(SelectorWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        SelectorWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(SelectorWindow)
        self.statusBar.setObjectName("statusBar")
        SelectorWindow.setStatusBar(self.statusBar)

        self.retranslateUi(SelectorWindow)
        QtCore.QMetaObject.connectSlotsByName(SelectorWindow)

    def retranslateUi(self, SelectorWindow):
        _translate = QtCore.QCoreApplication.translate
        SelectorWindow.setWindowTitle(_translate("SelectorWindow", "SelectorWindow"))
        self.pushButton.setText(_translate("SelectorWindow", "Ok"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SelectorWindow = QtWidgets.QMainWindow()
    ui = Ui_SelectorWindow()
    ui.setupUi(SelectorWindow)
    SelectorWindow.show()
    sys.exit(app.exec_())

