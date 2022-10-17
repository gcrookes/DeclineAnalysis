import sys
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QApplication, QMainWindow, QAbstractItemView,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConstraintWindow(object):
	
	def setupUi(self, Constraint_Window, parent):
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
		# self.mainToolBar = QtWidgets.QToolBar(Constraint_Window)
		# self.mainToolBar.setObjectName("mainToolBar")
		# Constraint_Window.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
		self.statusBar = QtWidgets.QStatusBar(Constraint_Window)
		self.statusBar.setObjectName("statusBar")
		Constraint_Window.setStatusBar(self.statusBar)

		self.ok_Button.clicked.connect(self.update_constraints)
		self.setWindowModality(2)
		self.setTabOrder(self.Qf_Const,self.Df_Const)
		self.setTabOrder(self.Df_Const,self.Dur_Const)
		self.setTabOrder(self.Dur_Const,self.ok_Button)

		self.retranslateUi(Constraint_Window)
		QtCore.QMetaObject.connectSlotsByName(Constraint_Window)

		self.Window = Constraint_Window
		self.parent = parent

	def retranslateUi(self, Constraint_Window):
		_translate = QtCore.QCoreApplication.translate
		Constraint_Window.setWindowTitle(_translate("Constraint_Window", "Constraint Window"))
		self.Qf_unit.setText(_translate("Constraint_Window", "TextLabel"))
		self.label_2.setText(_translate("Constraint_Window", "Df:"))
		self.Df_unit.setText(_translate("Constraint_Window", "TextLabel"))
		self.label_3.setText(_translate("Constraint_Window", "Duration:"))
		self.label.setText(_translate("Constraint_Window", "Qf:"))
		self.Dur_unit.setText(_translate("Constraint_Window", "TextLabel"))
		self.multiwell_Box.setText(_translate("Constraint_Window", "Constrain Multiple Wells"))
		self.ok_Button.setText(_translate("Constraint_Window", "Ok"))

		self.Qf_unit.setText('E3m3/d')
		self.Df_unit.setText('%/year')
		self.Dur_unit.setText('years')

	def load_menu(self,Qf,Df,Dur, units, local, fluid):
		
		self.local = local
		self.fluid = fluid

		# Update the text for the units
		if self.fluid == 1:
			self.Window.setWindowTitle('Gas Constraints')
			self.Qf_unit.setText(['E3m3/d','Mcf/d'][units])
		else:
			self.Window.setWindowTitle('Oil Constraints')
			self.Qf_unit.setText(['m3/d','bbl/d'][units])

		# Update the text for the units
		self.Qf_Const.setText(str(round(float(Qf),3)))
		self.Df_Const.setText(str(round(float(Df),3)))
		self.Dur_Const.setText(str(round(float(Dur),3)))

		# Update the box to determine if multiple declines are to be reconstrained
		self.multiwell_Box.setEnabled(local)
		self.multiwell_Box.setCheckState(False)
		
		self.show()

	def update_constraints(self):
				
		# Close the main window
		self.close()

		# Check all of the inputs to make sure they are valid
		try:
			Qf  = float(self.Qf_Const.text())
			Df  = float(self.Df_Const.text())
			Dur = float(self.Dur_Const.text())
		except:
			self.parent.warningMessage('Please Enter Numbers For All Inputs')
			return

		# Check if all inputs are above 0
		if Qf  <= 0 or Df  <= 0 or Dur <= 0: 
			self.parent.warningMessage('Inputs must be greater then 0')
		elif not self.local:
			# Confirm the selection if the multiwell box is checked
			msgBox = QMessageBox()
			response = msgBox.question(self,'Confirm Reconstraint','You are about to reconstrain all wells to these values.\n This cannot be undone. Would you like to continue?',QMessageBox.Yes, QMessageBox.No)
			if response == QMessageBox.No: return
				
		# Assemble the list of uwis to feed into the update function
		if self.multiwell_Box.checkState() == 2:
			# Multiwell option selected
			self.parent.wellSelectUI.load_list(self.parent, Qf, Df, Dur, self.fluid)
		else:
			if self.local:
				# Update just this well
				uwi_list = [self.parent.Well.UWI]
			else:
				# Update all wells
				uwi_list = list(self.parent.Field.keys())

			self.parent.update_constraints(uwi_list, Qf, Df, Dur, self.fluid)

class Ui_SelectorWindow(object):
	
	def setupUi(self, SelectorWindow):
		SelectorWindow.setObjectName("SelectorWindow")
		SelectorWindow.resize(300, 300)
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
		self.WellTree.setSelectionMode(QAbstractItemView.MultiSelection)
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
		self.setWindowModality(2)
		self.retranslateUi(SelectorWindow)
		QtCore.QMetaObject.connectSlotsByName(SelectorWindow)
		self.pushButton.clicked.connect(self.on_click)

	def retranslateUi(self, SelectorWindow):
		_translate = QtCore.QCoreApplication.translate
		SelectorWindow.setWindowTitle(_translate("SelectorWindow", "Constrain Wells "))
		self.pushButton.setText(_translate("SelectorWindow", "Ok"))
		SelectorWindow.setFixedSize(300, 600)

	def load_list(self, parent, Qf, Df, Dur, fluid):

		self.parent = parent
		self.Qf     = Qf
		self.Df     = Df
		self.Dur    = Dur
		self.fluid  = fluid

		keys = list(self.parent.Field.keys())
		active_uwi = self.parent.Well.UWI
		for uwi in keys:
			item = QtWidgets.QTreeWidgetItem([uwi])
			self.WellTree.addTopLevelItem(item)
			if uwi == active_uwi:
				item.setSelected(True)

		self.show()

	def on_click(self):
		# Close the GUI and pull the selected wells
		self.close()
		uwis = [index.data() for index in self.WellTree.selectedIndexes()]
		self.parent.update_constraints(uwis, self.Qf, self.Df, self.Dur, self.fluid)