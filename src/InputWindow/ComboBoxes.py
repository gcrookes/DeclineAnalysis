from PyQt5.QtWidgets import QWidget, QHBoxLayout
from InputWindow.ComboBoxPair import ComboBoxPair

class ComboBoxes(QWidget):

	def __init__(self):
		super().__init__()
		self.my_layout = QHBoxLayout()
		self.setLayout(self.my_layout)
		self.boxes = []

	def populate(self, number, items):
		for _ in range(number):
			box = ComboBoxPair()
			box.populateItems(items)
			self.boxes.append(box)
			self.my_layout.addWidget(box)

	def get_indexes(self):
		filled_boxes = {}
		for i, boxes in enumerate(self.boxes):
			
			items = boxes.get_items()

			if items is not None:
				filled_boxes[i] = items

		return filled_boxes