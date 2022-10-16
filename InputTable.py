from PyQt5 import QtCore
import PyQt5 as Qt
from PyQt5.QtWidgets import QTableWidget, QComboBox, QTableWidgetItem, QCheckBox, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QHeaderView
import numpy as np
import pandas as pd


class Fluid:

	def __init__(self, fluid_type, title, conversions):
		self.title = title
		self.fluid_type = fluid_type
		self.unit_conversions = conversions

	def fluid(self):
		return self.fluid_type

	def fluid_title(self):
		return self.title

	def conversion(self, unit):
		try:
			return self.unit_conversions[unit]
		except:
			raise ValueError("That is not a valid unit for this fluid")

	def unit_list(self):
		return self.unit_conversions.keys()


class FluidList:

	def __init__(self):

		# Converts everything into m3/day
		liquid_conversions = {'m3/day': 1, 'E3m3/day': 1000, 'bbl/day': 0.158987, 'Mbbl/day': 158.987}
		gas_conversions = {'E3m3/day': 1, 'm3/day': 1/1000, 'Mscf/day': 35.3147, 'MMscf/day': 35314.7}  # Converts everything into 1000m3/day

		self.fluids = [
			Fluid('oil', 'Cal. Oil Rate', liquid_conversions),
			Fluid('water', 'Cal. Condensate Rate', liquid_conversions),
			Fluid('cond', 'Cal. Water Rate', liquid_conversions),
			Fluid('daily', 'Cal. Daily Fluid', liquid_conversions),
			Fluid('gas', 'Cal. Gas Rate', gas_conversions)]

	def label_list(self):
		return [fluid.fluid_title() for fluid in self.fluids]

	def type_of(self, fluid_title):
		for fluid in self.fluids:
			if fluid.fluid_title() == fluid_title:
				return fluid.fluid()

	def units_of(self, fluid_title):
		for fluid in self.fluids:
			if fluid.fluid_title() == fluid_title:
				return fluid.unit_list()

	def conversion(self, fluid_title, unit):
		for fluid in self.fluids:
			if fluid.fluid_title == fluid_title:
				return fluid.conversion(unit)


class ComboBoxPair(QWidget):

	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()
		self.setLayout(layout)
		self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

		self.top = QComboBox()
		self.bottom = QComboBox()
		self.top.setMinimumWidth(20)
		self.bottom.setMinimumWidth(20)
		layout.addWidget(self.top)
		layout.addWidget(self.bottom)

		self.top.currentIndexChanged.connect(self.updateUnits)

	def updateUnits(self, index):
		self.bottom.clear()
		units = self.top.itemData(index)

		if units is not None:
			self.bottom.addItems(units)

	def populateItems(self, item_dict):
		for label, items in item_dict.items():
			self.top.addItem(label, items)

class ComboBoxes(QWidget):

	def __init__(self):
		super().__init__()
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)

	def populate(self, number, items):
		for _ in range(number):
			box = ComboBoxPair()
			box.populateItems(items)
			self.layout.addWidget(box)


class InputTable(QTableWidget):

	def sizeHint(self):
		return QtCore.QSize(500, 500)

	def __init__(self, parent, df, name):
		super(QTableWidget, self).__init__(parent)
		self.name = name
		self.df = df

		# self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

		cols = df.columns
		self.l = len(cols)
		self.setColumnCount(self.l)
		self.setRowCount(25)
		self.last_iteration = np.array([''] * self.l)

		self.fluids = FluidList()
		self.fluidlabels = self.fluids.label_list()
		self.UWIlabels = ['UWI']

		self.datelabels = ['Date']
		self.timelabels = []  # ['Time On Production']

		self.toplist = [""] + self.UWIlabels + self.datelabels + self.timelabels + self.fluidlabels

		# Don't forget to update the proper conversion
		self.datelist = ['YYYY-MM-DD', 'YYYY-DD-MM', 'MM-DD-YYYY', 'DD-MM-YYYY', 'YYYY/MM/DD', 'YYYY/DD/MM', 'MM/DD/YYYY', 'DD/MM/YYYY', 'MMM-YY', 'YY-MMM', 'MMM/YY', 'YY/MMM']
		self.timelist = ['Hours', 'Days', 'Months']

		self.dateconv = ['YYYY-MM-DD', 'YYYY-DD-MM', 'MM-DD-YYYY', 'DD-MM-YYYY', 'YYYY/MM/DD', 'YYYY/DD/MM', 'MM/DD/YYYY', 'DD/MM/YYYY', '%b-%y', '%y-%b', '%b/%y', '%y/%b'] # Converts everything into hours
		self.timeconv = [1, 1/24, 1/30.5]

		self.top_boxes = {}
		self.lower_boxes = {}

		# items = {f.fluid_title():f.unit_list() for f in self.fluids.fluids}
		# items[""] = [""]
		# items["UWI"] = [""]
		# items["Date"] = self.datelist

		# self.boxes = ComboBoxes(self.l, items)
		# self.setCellWidget(1, -1, self.boxes)
		self.setMinimumWidth(50)

		for i in range(self.l):
			#Create the tab at the top of the page
			item = QTableWidgetItem(str(cols[i]))
			item.setTextAlignment(QtCore.Qt.AlignHCenter)
			self.setItem(0, i, item)

			for j in range(min(23, len(df[cols[0]]))):

				if i == 0:
					self.setCellWidget(j+2, 0, QCheckBox(self))
					self.cellWidget(j+2, 0).setCheckState(2)

				if not pd.isna(df[cols[i]][j]):
					item = QTableWidgetItem(str(df[cols[i]][j]))
				else:
					item = QTableWidgetItem('')

				item.setTextAlignment(QtCore.Qt.AlignHCenter)
				self.setItem(j+3, i, item)

		for i in range(25):
			self.setVerticalHeaderItem(i, QTableWidgetItem(None))

		self.setHorizontalHeaderItem(0, QTableWidgetItem(None))
		self.horizontalHeader().setSectionResizeMode(1)
		self.verticalHeader().setSectionResizeMode(1)

	def import_table(self):

		cols = self.df.columns
		save_df = self.df
		return_df = pd.DataFrame()

		UWI = Date = Rate = False

		dropIndicies = [i for i in range(22) if self.cellWidget(i+2, 0).checkState() == 0]

		if len(dropIndicies) > 0:
			self.df.drop(self.df.index[dropIndicies], inplace=True)

		for i, box in enumerate(self.top_boxes):

			text = self.top_boxes[box].currentText()
			unit = self.lower_boxes[box].currentText()
			fluid_type = self.fluids.type_of(text)

			if text == "":
				continue

			if fluid_type is not None:
				return_df[fluid_type] = self.df[cols[i]] * self.fluids.conversion(text, unit)
				continue

			if text in self.datelabels:
				try:
					return_df['date'] = pd.to_datetime(
						self.df[cols[i]], format=self.dateconv[self.lower_boxes[box].currentIndex()])
					Date = True
				except:
					try:
						return_df['date'] = pd.to_datetime(self.df[cols[i]])
						Date = True
						msgBox = QMessageBox()
						msgBox.setText(
							'The given date format could not be parsed. \nAn alternate format was used please check the imported values')
						msgBox.exec_()
						self.df = save_df
					except:
						msgBox = QMessageBox()
						msgBox.setText(
							'Date format could not be parsed. Table was not imported')
						msgBox.exec_()
						self.df = save_df
						raise ValueError

			elif self.top_boxes[box].currentText() in self.timelabels:
				return_df['time'] = self.df[cols[i]] * \
					self.timeconv[self.lower_boxes[box].currentIndex()]

			elif self.top_boxes[box].currentText() in self.UWIlabels:
				return_df['UWI'] = self.df[cols[i]]
				UWI = True

		if not all([UWI, Date, Rate]) and any([UWI, Date, Rate]):
			msgBox = QMessageBox()
			msgBox.setText(
				'Need to map at least UWI, Date, and one rate \n Error on sheet "' + self.name+'"')
			msgBox.exec_()
			self.df = save_df
			raise ValueError

		if (not (UWI and Date and Rate)) and (not (UWI or Date or Rate)):
			self.df = save_df
			raise ValueError

		return_df.fillna(0, inplace=True)
		return return_df
