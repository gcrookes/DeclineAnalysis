from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
from InputWindow.ImportTab import ImportTab

class Ui_ImportWindow(object):

	def setupUi(self, ImportWindow, parent):
		ImportWindow.setObjectName("ImportWindow")
		ImportWindow.resize(726, 544)
		self.centralWidget = QtWidgets.QWidget(ImportWindow)
		self.centralWidget.setObjectName("centralWidget")
		self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
		self.verticalLayout.setContentsMargins(11, 11, 11, 11)
		self.verticalLayout.setSpacing(6)
		self.verticalLayout.setObjectName("verticalLayout")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)
		self.ImportButton = QtWidgets.QPushButton(self.centralWidget)
		self.ImportButton.setObjectName("ImportButton")
		self.horizontalLayout.addWidget(self.ImportButton)
		self.CancelButton = QtWidgets.QPushButton(self.centralWidget)
		self.CancelButton.setObjectName("CancelButton")
		self.horizontalLayout.addWidget(self.CancelButton)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
		self.tabWidget.setObjectName("tabWidget")
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(255)
		sizePolicy.setVerticalStretch(255)
		self.verticalLayout.addWidget(self.tabWidget)
		ImportWindow.setCentralWidget(self.centralWidget)
		self.menuBar = QtWidgets.QMenuBar(ImportWindow)
		self.menuBar.setGeometry(QtCore.QRect(0, 0, 726, 22))
		self.menuBar.setObjectName("menuBar")
		ImportWindow.setMenuBar(self.menuBar)
		self.statusBar = QtWidgets.QStatusBar(ImportWindow)
		self.statusBar.setObjectName("statusBar")
		ImportWindow.setStatusBar(self.statusBar)

		self.retranslateUi(ImportWindow)
		self.setWindowModality(2)

		self.CancelButton.clicked.connect(self.close_window)
		self.ImportButton.clicked.connect(self.import_items)
		self.parent = parent

	def retranslateUi(self, ImportWindow):
		_translate = QtCore.QCoreApplication.translate
		ImportWindow.setWindowTitle(_translate("ImportWindow", "MainWindow"))
		self.ImportButton.setText(_translate("ImportWindow", "Import"))
		self.CancelButton.setText(_translate("ImportWindow", "Cancel"))

	def close_window(self):
		self.close()

	# Method to open an excel file so you can read data in
	def open_file(self):
		
		# Get Filename 
		name, _ = QFileDialog.getOpenFileName(self, 'Open File')
		if name == '': return
		if name.find('.xls') < 0: raise ImportError("File type not supported. \nPlease select an Excel Workbook")

		sheets = pd.read_excel(name, sheet_name = None)
		self.tabs = []

		self.tabWidget.clear()
		for name, sheet in sheets.items():
			tab = ImportTab(self.tabWidget, sheet)

			self.tabs.append(tab)
			self.tabWidget.addTab(tab, name)

		self.showMaximized()

	def import_items(self):

		df = pd.DataFrame()

		for tab in self.tabs:
			df = pd.concat([df, tab.import_data()])

		df = df.fillna(0)

		if not df.empty:
			self.parent.Load_Data(df)

		self.close_window()
