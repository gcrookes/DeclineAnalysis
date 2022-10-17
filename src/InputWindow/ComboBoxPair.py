from PyQt5.QtWidgets import QComboBox, QWidget, QVBoxLayout, QSizePolicy

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

	def get_items(self):

		if self.top.currentText() == "":
			return None

		return [self.top.currentText(), self.bottom.currentText()]