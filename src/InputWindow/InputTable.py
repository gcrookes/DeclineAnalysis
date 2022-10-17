from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QCheckBox, QSizePolicy

class InputTable(QTableWidget):

	def __init__(self, parent, df):
		super(QTableWidget, self).__init__(parent)

		self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
		self.setColumnCount(len(df.columns))
		self.setRowCount(min(25, len(df.index)))

		# Add data to table
		for col in range(self.columnCount()):

			self.setHorizontalHeaderItem(col, QTableWidgetItem(None))

			for row in range(self.rowCount()):
				item = QTableWidgetItem(str(df.iloc[row,col]))
				item.setTextAlignment(QtCore.Qt.AlignHCenter)
				self.setItem(row, col, item)

		# Add check boxes on the left to the table
		for row in range(self.rowCount()):
			self.setCellWidget(row, 0, QCheckBox(self))
			self.cellWidget(row, 0).setCheckState(2)
			self.setVerticalHeaderItem(row, QTableWidgetItem(None))

		# Force table to fill space
		self.horizontalHeader().setSectionResizeMode(1)
		self.verticalHeader().setSectionResizeMode(1)

	def dropped_columns(self):
		return [i for i in range(25) if self.cellWidget(i, 0).checkState() == 0]
