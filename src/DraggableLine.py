import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
import datetime
from PreArrayMathForDecline_working import Calculations as m

class DraggableLine(m):

	lock = None
	calculating = None

	def __init__(self, GUI, well, parent, x, y, colour = 'k', fluid = 1, ax2 = None):
		self.GUI      = GUI
		self.well     = well
		self.ax       = parent
		self.ax2      = ax2
		self.canvas   = self.ax.figure.canvas
		self.canvas2  = self.ax2.figure.canvas
		self.hang_int = 50
		self.N        = 0
		self.fluid    = fluid

		self.c = colour

		if self.fluid == 1:
			self.final_point = [self.well.gasCum[-1], y[1]]
		else:
			self.final_point = [self.well.oilCum[-1], y[1]]

		if self.fluid == 1:
			self.final_point = [self.well.gasCum[-1], y[1]]
		else:
			self.final_point = [self.well.oilCum[-1], y[1]]

		xs, ys, ts = self.calc_line(x[0], y[0], self.final_point[0], y[1], self.N)

		self.line = Line2D(xs, ys, c = colour, marker = 's', ms = 7, markevery = [0, self.hang_int, -1], linewidth = 1, linestyle = 'solid', markerfacecolor = 'k', fillstyle = 'full')
		self.ax.add_line(self.line)
		self.canvas.draw()

		self.line2 = Line2D(ts, ys, c = colour, marker = 's', ms = 7, markevery = [-1], linewidth = 1, linestyle = 'solid', markerfacecolor = 'k', fillstyle = 'full')
		self.ax2.add_line(self.line2)
		self.canvas2.draw()

		self.update_limits()

		self.connect()
		if fluid == 1:
			self.well.best_fit_gas = self
		elif fluid == 2:
			self.well.best_fit_oil = self
                
		self.N = 0
		self.update_UI()

	def update_parent(self, parent, ax2):
		self.ax = parent
		self.canvas = self.ax.figure.canvas
		self.line = Line2D(self.line.get_xdata(), self.line.get_ydata(), c = self.c, marker = 's', ms = 7, markevery = [0, self.hang_int, -1], linewidth = 1, linestyle = 'solid', markerfacecolor = 'k', fillstyle = 'full')
		self.ax.add_line(self.line)

		self.ax2 = ax2
		self.canvas2 = self.ax2.figure.canvas
		self.line2 = Line2D(self.line2.get_xdata(), self.line2.get_ydata(), c = self.c, marker = 's', ms = 7, markevery = [-1], linewidth = 1, linestyle = 'solid', markerfacecolor = 'k', fillstyle = 'full')
		self.ax2.add_line(self.line2)
		self.update_limits()

	def connect(self):
		#self.line.figure.canvas
		self.cid_press   = self.canvas.mpl_connect('button_press_event', self.on_press)
		self.cid_move    = self.canvas.mpl_connect('motion_notify_event', self.on_motion)
		self.cid_release = self.canvas.mpl_connect('button_release_event', self.on_release)
		self.cid_scroll  = self.canvas.mpl_connect('scroll_event', self.on_scroll)

	def calc_timeLine(self, t, q, ti, qi, N):

		if self.fluid == 1:
			Qf_const  = self.well.Qf_const_gas
			Df_const  = self.well.Df_const_gas
			Dur_const = self.well.Dur_const_gas
		else:
			Qf_const  = self.well.Qf_const_oil
			Df_const  = self.well.Df_const_oil
			Dur_const = self.well.Dur_const_oil

		if N == 0:
			ai,EUR,DurationYears,LastProduction,qf, x, y = self.ExponentialDecline_Time(t, q, ti, qi, datetime.datetime.today(), MaxYears=Dur_const, qf=Qf_const)


	def calc_line(self, Q, q, Qi, qi, N):

		x = np.concatenate((np.linspace(Q,Qi,self.hang_int+1), np.linspace(Qi,Q+Qi,self.hang_int+1)))

		if self.fluid == 1:
			Qf_const  = self.well.Qf_const_gas
			Df_const  = self.well.Df_const_gas
			Dur_const = self.well.Dur_const_gas
			month_min = self.well.months[np.argmin(np.abs(Q - self.well.gasCum))]
			month_hang = self.well.months[np.argmin(np.abs(Qi - self.well.gasCum))]
		else:
			Qf_const  = self.well.Qf_const_oil
			Df_const  = self.well.Df_const_oil
			Dur_const = self.well.Dur_const_oil
			month_min = self.well.months[np.argmin(np.abs(Q - self.well.oilCum))]
			month_hang = self.well.months[np.argmin(np.abs(Qi - self.well.oilCum))]


		if N == 0:

			# Calculate Exponential Decline Parameters
			ai,EUR,DurationYears,LastProduction,qf, x, y, t = self.ExponentialDecline_Cum(q,Q/1000,qi,Qi/1000,datetime.datetime.today(), MaxYears=Dur_const, qf=Qf_const, month_min = month_min, month_hang = month_hang)
			af = ai

		elif round(N,3) == 1:

			ai,EUR,DurationYears,LastProduction,af,qf, x, y, t = self.HarmonicDecline_Cum(q,Q/1000,qi,Qi/1000,datetime.datetime.today(),MaxYears=Dur_const,paf=Df_const,qf=Qf_const, month_min = month_min, month_hang = month_hang)

		else:

			ai,EUR,DurationYears,LastProduction,af,qf, x, y, t = self.HyperbolicDecline_Cum(q,Q/1000,qi,Qi/1000,N,datetime.datetime.today(),MaxYears=Dur_const,paf=Df_const,qf=Qf_const, month_min = month_min, month_hang = month_hang)

		self.Qi   = str(round(qi,3))
		self.Di   = str(round(ai*36525, 6))
		self.Qf   = str(round(qf,3))
		try:
			self.EUR  = str(int(EUR*1000))
		except ValueError:
			self.EUR  = 'N/A'

		self.Df   = str(round(af*36525,3))
		self.Dur  = str(round(DurationYears,2))
		self.Last = str(LastProduction)[0:str(LastProduction).find(' ')]
	
		self.update_UI()
		return x, y, t

	def to_datetime(self, dt64, tzinfo=None):
		ts = pd.to_datetime(dt64)
		if tzinfo is not None:
			return datetime.datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second, tzinfo=tzinfo)
		return datetime.datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second)

	def on_press(self, event):
		if self.canvas.toolbar._active is not None: return
		if event.inaxes != self.ax: return

		self.x_click = event.xdata
		self.y_click = event.ydata

		x = self.ax.get_xlim()
		dx = (x[1] - x[0]) * 0.08
		xs = self.line.get_xdata()

		if self.x_click > (xs[0]-dx) and self.x_click < (xs[0]+dx):
			self.ind = 0
		elif self.x_click > (xs[self.hang_int]-dx) and self.x_click < (xs[self.hang_int]+dx):
			self.ind = self.hang_int
		else:
			return

		if event.dblclick and self.ind == self.hang_int:

			x_orig = self.line.get_xdata()
			y_orig = self.line.get_ydata()

			dx = self.final_point[0] - x_orig[self.hang_int]
			dy = self.final_point[1] - y_orig[self.hang_int]

			self.line.set_xdata(self.line.get_xdata() + dx)
			self.line.set_ydata(self.line.get_ydata() + dy)


			x_orig = self.line.get_xdata()
			y_orig = self.line.get_ydata()


			xs, ys, ts = self.calc_line(x_orig[0], y_orig[0], x_orig[self.hang_int], y_orig[self.hang_int], self.N)

			self.line.set_xdata(xs)
			self.line.set_ydata(ys)
			self.line2.set_xdata(ts)
			self.line2.set_ydata(ys)

			self.update_UI()
			return

		self.lock = self
		self.canvas.draw()
		

	def on_motion(self, event):
		if self.lock != self: return
		if event.inaxes != self.ax: return
		if self.GUI.activeFluid != self.fluid: return

		x0 = self.line.get_xdata()[0]

		x = event.xdata
		y = event.ydata

		if self.ind == 0 and x != None and y != None:
			# Left Most Point
			x_orig = self.line.get_xdata()
			y_orig = self.line.get_ydata()


			xs, ys, ts = self.calc_line(x, y, x_orig[self.hang_int], y_orig[self.hang_int], self.N)

			self.line.set_xdata(xs)
			self.line.set_ydata(ys)
			self.line2.set_xdata(ts)
			self.line2.set_ydata(ys)

		elif self.ind == self.hang_int:
			# Middle Point
			if event.button != 2:
				dx = 0
				if y is not None:
					dy = y - self.line.get_ydata()[self.hang_int]
				else:
					dy = 0
				self.line.set_ydata(self.line.get_ydata() + dy)

			else:
				dx = x - self.line.get_xdata()[self.hang_int]
				dy = y - self.line.get_ydata()[self.hang_int]
				self.line.set_xdata(self.line.get_xdata() + dx)
				self.line.set_ydata(self.line.get_ydata() + dy)

			x_orig = self.line.get_xdata()
			y_orig = self.line.get_ydata()
			
			xs, ys, ts = self.calc_line(x_orig[0], y_orig[0], x_orig[self.hang_int], y_orig[self.hang_int], self.N)
			
			self.line.set_xdata(xs)
			self.line.set_ydata(ys)
			self.line2.set_xdata(ts)
			self.line2.set_ydata(ys)

		self.update_limits()

		self.canvas2.draw()
		self.canvas.draw()
		self.calculating = None

	def update_limits(self):

		y_fac = 1.2
		x_fac = 2
		l_fac = 1.1

		if self.fluid == 1:
			y = max(self.well.gasRate)*y_fac
			f = 2
			if self.line.get_xdata()[-1] < x_fac/l_fac * self.well.gasCum[-1]:
				x = self.well.gasCum[-1] * x_fac
			else:
				x = self.line.get_xdata()[-1] * l_fac
		else:
			y = max(self.well.oilRate)*y_fac
			f = 1
			if self.line.get_xdata()[-1] < x_fac/l_fac * self.well.oilCum[-1]:
				x = self.well.oilCum[-1] * x_fac
			else:
				x = self.line.get_xdata()[-1] * l_fac


		if self.line2.get_xdata()[-1] < x_fac/l_fac * self.well.months[-1]:
			t = self.well.months[-1] * x_fac
		else:
			t = self.line2.get_xdata()[-1] * l_fac

		self.canvas.update_axis(x,t,y,f)


	def on_scroll(self, event):
		#MPL MouseEvent: xy=(308,183) xydata=(331.374358627,1.40582730418) button=down dblclick=False inaxes=AxesSubplot(0.125,0.11;0.775x0.77)
		#Want to know wheither button = up|down tells which way we are scrolling

		if event.inaxes != self.ax: return
		if self.calculating is not None: return
		if self.GUI.activeFluid != self.fluid: return

		interval = 0.1
		

		if event.button == 'down':
			self.N += interval
		else:
			self.N -= interval
		
		self.N = min(2, max(0, self.N))

		x_orig = self.line.get_xdata()
		y_orig = self.line.get_ydata()

		if self.lock != self:
			x = x_orig[0]
			y = y_orig[0]
		else:
			x = event.xdata
			y = event.ydata

		x = x_orig[0]
		y = y_orig[0]

		xs, ys, ts = self.calc_line(x, y, x_orig[self.hang_int], y_orig[self.hang_int], self.N)

		self.line.set_xdata(xs)
		self.line.set_ydata(ys)
		self.line2.set_xdata(ts)
		self.line2.set_ydata(ys)

		self.update_limits

		self.update_UI()
		self.canvas.draw()

	def on_release(self, event):
		self.lock = None
		self.canvas.draw()
		
		if self.fluid == 1:
			self.well.best_fit_gas = self
		elif self.fluid == 2:
			self.well.best_fit_oil = self

	def update_UI(self):

		try:
			x = self.line.get_xdata()
			self.GUI.ParameterFrame.set_text(self.get_parameters())
		except AttributeError:
			self.GUI.ParameterFrame.clear_text()
			return

		if self.GUI.Units == 0:
			self.GUI.ParameterFrame.set_units(['E3m3','m3'][self.fluid - 1])
		else:
			self.GUI.ParameterFrame.set_units(['Mcf', 'bbl'][self.fluid - 1])


	def disconnect(self):
			self.canvas.mpl_disconnect(self.cid_press)
			self.canvas.mpl_disconnect(self.cid_move)
			self.canvas.mpl_disconnect(self.cid_release)
			self.canvas.mpl_disconnect(self.cid_scroll)

	def get_parameters(self):
		return [self.Qi, self.Di, self.N, self.Dur, self.Qf, self.Df, self.EUR, self.Last]