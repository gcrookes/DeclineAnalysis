import numpy as np
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
from DraggableLine import DraggableLine

class SelectFromCollection(object):

	def __init__(self, well, fluid):
		# General Declarations
		self.well   = well

		# 1 = gas, 2 = oil
		self.fluid  = fluid

	def __call__(self, GUI, ax, ax2, collection):
		self.GUI        = GUI 
		self.ax         = ax
		self.ax2 		= ax2
		self.fig        = ax.figure
		self.canvas     = ax.figure.canvas
		self.xys_g = collection.get_offsets()
		self.ind = []
		self.lasso = LassoSelector(self.ax, onselect = self.onselectLasso, useblit = False, button = 1)

	def onselectLasso(self, verts, cuttoff = 0.1):
		path = Path(verts)
		ind_g = np.nonzero(path.contains_points(self.xys_g))[0]

		self.ind = ind_g
		self.xys = self.xys_g
		self.c   = 'red'

		# Takes the most selected line
		selected = self.xys[self.ind]

		# Control For one or less points being selected
		if len(selected) > 1:
			x_selected = selected[:,0]
			y_selected = selected[:,1]

			m, c = np.polyfit(x_selected, y_selected, 1)

			x  = x_selected


			for i in range(1, len(self.xys[:,1])):
				if self.xys[-i,:][1] != 0:
					hang  = self.xys[-i,:]
					break
			
			xlim = self.ax.get_xlim()
			ylim = self.ax.get_ylim()

			x1 = hang[0]
			y1 = hang[1]

			x0 = xlim[1] * 0.1
			y0 = y1 - (x1-x0) * m
			
			if y0 > ylim[1]:
				y0 = 0.9 * ylim[1]
				x0 = x1 - (y1 - y0)/m 

			y2 = cuttoff
			x2 = (y2 - y1)/m + x1

			try:
				l = self.declineplot.pop()
				l.remove()
				del l
			except:
				pass


			self.list_points = []

			xlim = self.ax.get_xlim()
			ylim = self.ax.get_ylim()

			ratio = 0.05
			size = [ratio/2 * (xlim[1]-xlim[0]), ratio * (ylim[1]-ylim[0])]


			if self.fluid == 1:
				self.line_gas = DraggableLine(self.GUI, self.well, self.ax, [x0,x1,x2], [y0,y1,y2], colour = 'r', fluid = 1, ax2 = self.ax2)
			elif self.fluid == 2:
				self.line_oil = DraggableLine(self.GUI, self.well, self.ax, [x0,x1,x2], [y0,y1,y2], colour = 'g', fluid = 2, ax2 = self.ax2)

		self.canvas.draw_idle()
		self.disconnect()

	def disconnect(self):
		self.lasso.disconnect_events()
		self.canvas.draw_idle()

	def clearFigure(self):

		self.axes.clear()
		self.axes.grid(True)
		del(self.list_points[:])
		self.updateFigure()

	def updateFigure(self):

		self.canvas.draw()
