# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'segmentwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QFrame

class SegmentWindow(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.setup_Window()

        self.BTN_Add.clicked.connect(parent.add_segment)
        self.BTN_Remove.clicked.connect(parent.remove_segment)

        self.Boxes = [self.LE_Qi, self.LE_Di, self.LE_N, self.LE_D, self.LE_Qf, self.LE_Df, self.LE_EUR, self.LE_LP]
        self.params = [None, None, None, None, None, None, None, None]

        for LE in self.Boxes:
            LE.setEnabled(False)

        self.LE_Qi.editingFinished.connect(lambda: self.parameterChange(0))
        self.LE_Di.editingFinished.connect(lambda: self.parameterChange(1))
        self.LE_N.editingFinished.connect(lambda: self.parameterChange(2))
        self.LE_D.editingFinished.connect(lambda: self.parameterChange(3))
        self.LE_Qf.editingFinished.connect(lambda: self.parameterChange(4))
        self.LE_Df.editingFinished.connect(lambda: self.parameterChange(5))
        self.LE_EUR.editingFinished.connect(lambda: self.parameterChange(6))
        self.LE_LP.editingFinished.connect(lambda: self.parameterChange(7))
        self.CB_Title.currentIndexChanged.connect(self.changeFluid)

    def changeFluid(self, i):

        if self.parent is None: return
        if self.parent.parent is None: return

        if i == 0:
            self.parent.parent.switch_Gas()
        elif i == 1:
            self.parent.parent.switch_Oil()

    def parameterChange(self, i):
        # need some kind of constraint update
        pass
        # print(self.Boxes[i])

    def set_values(self,params):
        
        #params = [Qi, Di, N, Dur, Qf, Df, EUR, LastProd]

        for i in [0,1,2,4,5]:
            try: 
                if params[i] is not None: self.Boxes[i].setText(str(round(float(params[i]),4)))
            except: 
                self.Boxes[i].setText('N/A')

        for i in [3,6]:

            try: 
                if params[i] is not None: self.Boxes[i].setText(str(round(float(params[i]),0)))
            except: 
                self.Boxes[i].setText('N/A')

        try: 
            if params[7] is not None: self.Boxes[7].setText(str(params[7]))
        except: 
            self.Boxes[i].setText('N/A')

        self.params = params

    def set_units(self, text):
        self.UNIT_Qi.setText(text + '/d')
        self.Unit_Qf.setText(text + '/d')
        self.label_19.setText(text)

    def get_values(self):

        params = []
        
        for text in self.params:

            try: params.append(float(text))
            except ValueError: params.append(text)
            except TypeError:  params.append(None)

        return params

    def setup_Window(self):
        self.setObjectName("SegmentWindow")
        self.resize(412, 178)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.Frame = QtWidgets.QFrame(self)
        self.Frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Frame.setObjectName("Frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Frame)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.CB_Title = QtWidgets.QComboBox(self.Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CB_Title.sizePolicy().hasHeightForWidth())
        self.CB_Title.setSizePolicy(sizePolicy)
        self.CB_Title.setModelColumn(0)
        self.CB_Title.setObjectName("CB_Title")
        self.CB_Title.addItem("")
        self.CB_Title.addItem("")
        self.gridLayout_2.addWidget(self.CB_Title, 0, 0, 1, 2)
        self.BTN_Remove = QtWidgets.QPushButton(self.Frame)
        self.BTN_Remove.setObjectName("BTN_Remove")
        self.gridLayout_2.addWidget(self.BTN_Remove, 0, 2, 1, 2)
        self.BTN_Add = QtWidgets.QPushButton(self.Frame)
        self.BTN_Add.setObjectName("BTN_Add")
        self.gridLayout_2.addWidget(self.BTN_Add, 0, 4, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.Frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.LE_Qi = QtWidgets.QLineEdit(self.Frame)
        self.LE_Qi.setObjectName("LE_Qi")
        self.gridLayout_2.addWidget(self.LE_Qi, 1, 1, 1, 1)
        self.UNIT_Qi = QtWidgets.QLabel(self.Frame)
        self.UNIT_Qi.setObjectName("UNIT_Qi")
        self.gridLayout_2.addWidget(self.UNIT_Qi, 1, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.Frame)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 1, 3, 1, 1)
        self.LE_Qf = QtWidgets.QLineEdit(self.Frame)
        self.LE_Qf.setObjectName("LE_Qf")
        self.gridLayout_2.addWidget(self.LE_Qf, 1, 4, 1, 1)
        self.Unit_Qf = QtWidgets.QLabel(self.Frame)
        self.Unit_Qf.setObjectName("Unit_Qf")
        self.gridLayout_2.addWidget(self.Unit_Qf, 1, 5, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.Frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.LE_Di = QtWidgets.QLineEdit(self.Frame)
        self.LE_Di.setObjectName("LE_Di")
        self.gridLayout_2.addWidget(self.LE_Di, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.Frame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 2, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.Frame)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 2, 3, 1, 1)
        self.LE_Df = QtWidgets.QLineEdit(self.Frame)
        self.LE_Df.setObjectName("LE_Df")
        self.gridLayout_2.addWidget(self.LE_Df, 2, 4, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.Frame)
        self.label_18.setObjectName("label_18")
        self.gridLayout_2.addWidget(self.label_18, 2, 5, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.Frame)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.LE_N = QtWidgets.QLineEdit(self.Frame)
        self.LE_N.setObjectName("LE_N")
        self.gridLayout_2.addWidget(self.LE_N, 3, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.Frame)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 3, 3, 1, 1)
        self.LE_EUR = QtWidgets.QLineEdit(self.Frame)
        self.LE_EUR.setObjectName("LE_EUR")
        self.gridLayout_2.addWidget(self.LE_EUR, 3, 4, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.Frame)
        self.label_19.setObjectName("label_19")
        self.gridLayout_2.addWidget(self.label_19, 3, 5, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.Frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.LE_D = QtWidgets.QLineEdit(self.Frame)
        self.LE_D.setObjectName("LE_D")
        self.gridLayout_2.addWidget(self.LE_D, 4, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.Frame)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 4, 2, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.Frame)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 4, 3, 1, 1)
        self.LE_LP = QtWidgets.QLineEdit(self.Frame)
        self.LE_LP.setObjectName("LE_LP")
        self.gridLayout_2.addWidget(self.LE_LP, 4, 4, 1, 1)
        self.gridLayout.addWidget(self.Frame, 1, 2, 1, 1)    
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SegmentWindow", "SegmentWindow"))
        self.CB_Title.setItemText(0, _translate("SegmentWindow", "Gas"))
        self.CB_Title.setItemText(1, _translate("SegmentWindow", "Oil"))
        self.BTN_Remove.setText(_translate("SegmentWindow", "Remove Segment"))
        self.BTN_Add.setText(_translate("SegmentWindow", "Add Segment"))
        self.label_2.setText(_translate("SegmentWindow", "Qi"))
        self.UNIT_Qi.setText(_translate("SegmentWindow", "Mcf/d"))
        self.label_12.setText(_translate("SegmentWindow", "Qf"))
        self.Unit_Qf.setText(_translate("SegmentWindow", "Mcf/d"))
        self.label_3.setText(_translate("SegmentWindow", "Di"))
        self.label.setText(_translate("SegmentWindow", "%/Year"))
        self.label_13.setText(_translate("SegmentWindow", "Df"))
        self.label_18.setText(_translate("SegmentWindow", "%/year"))
        self.label_4.setText(_translate("SegmentWindow", "N"))
        self.label_14.setText(_translate("SegmentWindow", "EUR"))
        self.label_19.setText(_translate("SegmentWindow", "Mcf"))
        self.label_5.setText(_translate("SegmentWindow", "Duration"))
        self.label_10.setText(_translate("SegmentWindow", "Years"))
        self.label_15.setText(_translate("SegmentWindow", "Last Production"))

        QtCore.QMetaObject.connectSlotsByName(self)


class ParameterFrame(QFrame, QWidget):

    # Implemenation
    # self.ParameterFrame = ParameterFrame(self.centralWidget)
    # self.ParameterFrame.setObjectName("ParameterFrame")
    # self.gridLayout.addWidget(self.ParameterFrame, 5, 1, 4, 11)  

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.parent = parent

        self.setup_frame(parent)
        self.segments = []
        self.add_segment()


    def setup_frame(self, parent):
        self.Frame = QFrame(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Frame.sizePolicy().hasHeightForWidth())
        self.Frame.setSizePolicy(sizePolicy)
        self.Frame.setFrameShape(QtWidgets.QFrame.Box)
        self.Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Frame.setObjectName("ParameterFrame")
        self.Frame.horizontalLayout = QtWidgets.QHBoxLayout(self.Frame)
        self.Frame.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.Frame.horizontalLayout.setSpacing(2)
        self.Frame.horizontalLayout.setObjectName("horizontalLayout")

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.addWidget(self.Frame)

    def add_segment(self):
        self.segments.append(SegmentWindow(self))
        self.Frame.horizontalLayout.addWidget(self.segments[-1])
        self.format()

    def remove_segment(self):
        sw = self.segments.pop(-1)
        self.Frame.horizontalLayout.removeWidget(sw)
        sw.setParent(None)
        del sw
        self.format()

    def format(self):

        for seg in self.segments:
            seg.CB_Title.hide()
            seg.BTN_Remove.hide()
            seg.BTN_Add.hide()

        self.segments[0].CB_Title.show()
        
        # if len(self.segments) > 1: self.segments[-1].BTN_Remove.show()
        # if len(self.segments) < 3: self.segments[-1].BTN_Add.show()

    def clear_text(self):

        for sw in self.segments:
            for LE in sw.Boxes:
                LE.setText('')

    def set_text(self, params):

        for sw in self.segments:
            sw.set_values(params)

    def set_units(self, text):

        for sw in self.segments:
            sw.set_units(text)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    ParameterFrame = ParameterFrame(window)

    window.setCentralWidget(ParameterFrame)
    window.show()
    sys.exit(app.exec_())



