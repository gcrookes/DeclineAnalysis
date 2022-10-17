# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'constraint_window.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConstraintWindow(object):
    def setupUi(self, Constraint_Window):
        Constraint_Window.setObjectName("Constraint_Window")
        Constraint_Window.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Constraint_Window.sizePolicy().hasHeightForWidth())
        Constraint_Window.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(Constraint_Window)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.Qf_unit = QtWidgets.QLabel(self.centralWidget)
        self.Qf_unit.setObjectName("Qf_unit")
        self.gridLayout.addWidget(self.Qf_unit, 0, 2, 1, 1)
        self.Qf_Const = QtWidgets.QLineEdit(self.centralWidget)
        self.Qf_Const.setObjectName("Qf_Const")
        self.gridLayout.addWidget(self.Qf_Const, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.Df_unit = QtWidgets.QLabel(self.centralWidget)
        self.Df_unit.setObjectName("Df_unit")
        self.gridLayout.addWidget(self.Df_unit, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.Dur_Const = QtWidgets.QLineEdit(self.centralWidget)
        self.Dur_Const.setObjectName("Dur_Const")
        self.gridLayout.addWidget(self.Dur_Const, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.Df_Const = QtWidgets.QLineEdit(self.centralWidget)
        self.Df_Const.setObjectName("Df_Const")
        self.gridLayout.addWidget(self.Df_Const, 1, 1, 1, 1)
        self.Dur_unit = QtWidgets.QLabel(self.centralWidget)
        self.Dur_unit.setObjectName("Dur_unit")
        self.gridLayout.addWidget(self.Dur_unit, 2, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.multiwell_Box = QtWidgets.QCheckBox(self.centralWidget)
        self.multiwell_Box.setObjectName("multiwell_Box")
        self.horizontalLayout.addWidget(self.multiwell_Box)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.ok_Button = QtWidgets.QPushButton(self.centralWidget)
        self.ok_Button.setObjectName("ok_Button")
        self.horizontalLayout.addWidget(self.ok_Button)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 3)
        Constraint_Window.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(Constraint_Window)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 278, 22))
        self.menuBar.setObjectName("menuBar")
        Constraint_Window.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(Constraint_Window)
        self.mainToolBar.setObjectName("mainToolBar")
        Constraint_Window.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(Constraint_Window)
        self.statusBar.setObjectName("statusBar")
        Constraint_Window.setStatusBar(self.statusBar)

        self.retranslateUi(Constraint_Window)
        QtCore.QMetaObject.connectSlotsByName(Constraint_Window)

    def retranslateUi(self, Constraint_Window):
        _translate = QtCore.QCoreApplication.translate
        Constraint_Window.setWindowTitle(_translate("Constraint_Window", "Constraint_Window"))
        self.Qf_unit.setText(_translate("Constraint_Window", "TextLabel"))
        self.label_2.setText(_translate("Constraint_Window", "Df:"))
        self.Df_unit.setText(_translate("Constraint_Window", "TextLabel"))
        self.label_3.setText(_translate("Constraint_Window", "Duration:"))
        self.label.setText(_translate("Constraint_Window", "Qf:"))
        self.Dur_unit.setText(_translate("Constraint_Window", "TextLabel"))
        self.multiwell_Box.setText(_translate("Constraint_Window", "Constrain Multiple Wells"))
        self.ok_Button.setText(_translate("Constraint_Window", "Ok"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Constraint_Window = QtWidgets.QMainWindow()
    ui = Ui_Constraint_Window()
    ui.setupUi(Constraint_Window)
    Constraint_Window.show()
    sys.exit(app.exec_())

