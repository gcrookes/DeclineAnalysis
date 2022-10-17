from InputWindow.FluidList import FluidList
from InputWindow.ComboBoxes import ComboBoxes
from InputWindow.InputTable import InputTable
from PyQt5.QtWidgets import QWidget, QGridLayout
import pandas as pd

class ImportTab(QWidget):

	def __init__(self, parent, df):
		super().__init__()

		self.df = df.fillna("")
	
		self.fluids = FluidList()
		self.fluidlabels = self.fluids.label_list()
		datelist = ['YYYY-MM-DD', 'YYYY-DD-MM', 'MM-DD-YYYY', 'DD-MM-YYYY', 'YYYY/MM/DD', 'YYYY/DD/MM', 'MM/DD/YYYY', 'DD/MM/YYYY', 'MMM-YY', 'YY-MMM', 'MMM/YY', 'YY/MMM']

		items = {"":[""], "UWI":[""], "Date":datelist}
		items.update({f.fluid_title():f.unit_list() for f in self.fluids.fluids})

		self.boxes = ComboBoxes()
		self.boxes.populate(len(df.columns), items)
		self.table = InputTable(parent, df)

		layout = QGridLayout()
		self.setLayout(layout)

		layout.addWidget(self.boxes, 0,0,1,1)
		layout.addWidget(self.table, 1,0,-1,-1)

	def import_data(self):

		# Get the check boxes that were filled in and return if there are not enough
		filled_boxes = self.boxes.get_indexes()
		if len(filled_boxes) < 3:
			return None

		return_df = pd.DataFrame()

		# Drop any rows that were unchecked
		to_drop = self.table.dropped_columns()
		if len(to_drop) > 0:
			self.df = self.df.drop(index = to_drop)

		name = date = fluid = 0

		for col, item in filled_boxes.items():
			label, unit = item
 
			if label == "UWI":
				return_df[label] = self.df.iloc[:,col]
				name = 1
				continue
			
			if label == "Date":
				return_df['date'] = pd.to_datetime(self.df.iloc[:,col], unit)
				date = 1
				continue

			fluid_type = self.fluids.type_of(label)
			if fluid_type is not None:
				return_df[fluid_type] = self.df.iloc[:,col]
				conversion = self.fluids.conversion(label, unit)
				return_df[fluid_type] *= conversion
				fluid = 1

		if (name + date + fluid) < 3:
			return None

		return return_df