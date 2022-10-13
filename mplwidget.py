from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox, QCheckBox, QProgressBar, QComboBox
from PyQt5.QtWidgets import QLabel, QStyleFactory, QFontDialog, QDialog, QVBoxLayout, QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

import numpy as np

class MplCanvas(FigureCanvas):

	def __init__(self, parent):

		self.parent = parent

		self.fig = Figure()

		self.oilcum = self.fig.add_subplot(221)
		self.oilcum.set_xlabel('Cumulative Oil [bbl]')
		self.oilcum.set_ylabel('Oil Rate [bbl/d]')

		self.oiltime = self.fig.add_subplot(222)
		self.oiltime.set_xlabel('Time [Months]')
		self.oiltime.set_ylabel('Oil Rate [bbl/d]')

		self.gascum = self.fig.add_subplot(223)
		self.gascum.set_xlabel('Cumulative Gas [Mcf]')
		self.gascum.set_ylabel('Gas Rate [Mcf/d]')

		self.gastime = self.fig.add_subplot(224)
		self.gastime.set_xlabel('Time [Months]')
		self.gastime.set_ylabel('Gas Rate [Mcf/d]')

		print(self.fig)

		FigureCanvas.__init__(self, self.fig)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

		self.Units = 0

	def show_oil(self):
		self.gascum.set_visible(False)
		self.gastime.set_visible(False)
		self.oilcum.set_visible(True)
		self.oiltime.set_visible(True)
				
		self.gastime.set_position([0.55,1.1,0.4,0.88])
		self.gascum.set_position([0.05,1.1,0.4,0.88])
		self.oiltime.set_position([0.55,0.1,0.4,0.88])
		self.oilcum.set_position([0.05,0.1,0.4,0.88])

		self.parent.activeFluid = 2
		self.draw()

	def show_gas(self):
		self.gascum.set_visible(True)
		self.gastime.set_visible(True)
		self.oilcum.set_visible(False)
		self.oiltime.set_visible(False)

		self.oiltime.set_position([0.55,-1.1,0.4,0.88])
		self.oilcum.set_position([0.05,-1.1,0.4,0.88])
		self.gastime.set_position([0.55,0.1,0.4,0.88])
		self.gascum.set_position([0.05,0.1,0.4,0.88])
		self.parent.activeFluid = 1
		self.draw()

	def update_axis(self, maxx, maxt, maxy, plot):

		if plot == 1:
			self.oilcum.set_xlim(0,max(maxx,0.1))
			self.oiltime.set_xlim(0,max(maxt,0.001))
			self.oilcum.set_ylim(0,max(maxy,0.1))
			self.oiltime.set_ylim(0,max(maxy,0.1))
		elif plot == 2:
			self.gascum.set_xlim(0,max(maxx,0.1))
			self.gastime.set_xlim(0,max(maxt,0.001))
			self.gascum.set_ylim(0,max(maxy,0.1))
			self.gastime.set_ylim(0,max(maxy,0.1))

	def update_units(self, units):
		self.Units = units

		if units == 0:
			self.oilcum.set_xlabel('Cumulative Oil [m3]')
			self.oilcum.set_ylabel('Oil Rate [m3/d]')
			self.oiltime.set_xlabel('Time [Months]')
			self.oiltime.set_ylabel('Oil Rate [m3/d]')
			self.gascum.set_xlabel('Cumulative Gas [E3m3]')
			self.gascum.set_ylabel('Gas Rate [E3m3/d]')
			self.gastime.set_xlabel('Time [Months]')
			self.gastime.set_ylabel('Gas Rate [E3m3/d]')
		else:
			self.oilcum.set_xlabel('Cumulative Oil [bbl]')
			self.oilcum.set_ylabel('Oil Rate [bbl/d]')
			self.oiltime.set_xlabel('Time [Months]')
			self.oiltime.set_ylabel('Oil Rate [bbl/d]')
			self.gascum.set_xlabel('Cumulative Gas [Mscf]')
			self.gascum.set_ylabel('Gas Rate [Mscfd]')
			self.gastime.set_xlabel('Time [Months]')
			self.gastime.set_ylabel('Gas Rate [Mscfd]')

	def drawRectangle(self, rect):
		# Draw the zoom rectangle to the QPainter.  _draw_rect_callback needs
		# to be called at the end of paintEvent.
		if rect is not None:
			def _draw_rect_callback(painter):
				pen = QtGui.QPen(QtCore.Qt.red, 1 / self._dpi_ratio, QtCore.Qt.DotLine)
				painter.setPen(pen)
				painter.drawRect(*(pt / self._dpi_ratio for pt in rect))
		else:
			def _draw_rect_callback(painter):
				return

		self._draw_rect_callback = _draw_rect_callback
		self.update()


class MplWidget(QWidget):
	def __init__(self, parent = None):
		QWidget.__init__(self, parent)
		self.canvas = MplCanvas(parent)
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.vbl = QVBoxLayout()
		self.vbl.addWidget(self.canvas)
		self.vbl.addWidget(self.toolbar)
		self.setLayout(self.vbl)

