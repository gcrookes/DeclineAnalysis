import numpy as np
import pandas as pd
import calendar
from SelectFromCollection import SelectFromCollection
from scipy.signal import argrelextrema

class Well():
	# Each Well will be a member of this class and needs to have production data input

	def __init__(self, UWI, date, gasRate, oilRate):
		# Feed in production rates and calculate cumulatives. Default to 0's if not given
		self.UWI = UWI
		self.best_fit_gas = None
		self.best_fit_oil = None
		self.dates = date

		self.Prod_Time = np.zeros(len(date))
		self.months = np.zeros(len(date))
		self.days = np.zeros(len(date))

		firstMonth = pd.to_datetime(date[0]).month
		firstYear  = pd.to_datetime(date[0]).year
		firstDay   = pd.to_datetime(date[0]).day

		for i in range(len(date)):
			self.Prod_Time[i] = calendar.monthrange(pd.to_datetime(date[i]).year, pd.to_datetime(date[i]).month)[1]
			self.months[i] = (pd.to_datetime(date[i]).year - firstYear) * 12 + (pd.to_datetime(date[i]).month - firstMonth)

		self.days = self.months * 30.5

		self.gasRate = gasRate
		self.gasCum, self.gasCum_plot = self.Cumulative(self.Prod_Time, gasRate)


		self.oilRate = oilRate
		self.oilCum, self.oilCum_plot = self.Cumulative(self.Prod_Time, oilRate)

		self.Qf_const_gas  = 0.01
		self.Df_const_gas  = 1
		self.Dur_const_gas = 30

		self.Qf_const_oil  = 0.001
		self.Df_const_oil  = 1
		self.Dur_const_oil = 30

		self.Selector_gas  = SelectFromCollection(self, 1)
		self.Selector_oil  = SelectFromCollection(self, 2)

	def Cumulative(self, Prod_Time, rate, previous = 0):
		if len(rate) > 0 and len(Prod_Time) == len(rate):
			Cum = np.zeros(len(Prod_Time))
			Cum_plot = np.zeros(len(Prod_Time))

			Cum[0] = Prod_Time[0] * rate[0] + previous
			Cum_plot[0] = Prod_Time[0] * rate[0] / 2 + previous

			for i in range(1, len(Prod_Time)):
				Cum[i] = Prod_Time[i]*rate[i]+Cum[i-1]
				Cum_plot[i] = Prod_Time[i] * rate[i] / 2 + Cum[i-1]
			return Cum, Cum_plot
		else:
			return np.array([]), np.array([])

	def findDiscontinuities(self, fluid):

		if fluid == 'gas':
			self.rate = self.gasRate
			self.cum  = self.gasCum
		elif fluid == 'oil':
			self.rate = self.oilRate
			self.cum  = self.oilCum
		elif fluid == 'cond':
			self.rate = self.condRate
			self.cum  = self.condCum
		elif fluid == 'water':
			self.rate = self.waterRate
			self.cum  = self.waterCum

		if np.sum(self.rate) == 0:
			return

		type1, self.movingAverage = self.discontinuities(self.rate, self.days)
		self.derivative = np.gradient(self.movingAverage)
		type2, dummy = self.discontinuities(self.derivative, self.days)

		for i in range(0, len(type2[0])):
			day_val= type2[0][i]
			type2[2][i] = np.max((self.days == day_val)*self.rate)


		day_disc  = np.append(type1[0], type2[0])
		rate_disc = np.append(type1[2], type2[2])

		self.disc = np.unique(day_disc)

	def discontinuities(self, rate, days):
		
		N = 3
		cuttoff = 0.15 * np.average(rate)

		movingAverage = np.convolve(rate, np.ones((N,))/N, mode = 'same')
		for _ in range(0, int(np.log(len(rate))/np.log(2))-1):
			movingAverage = np.convolve(movingAverage, np.ones((N,))/N, mode = 'same')


		residuals = abs(movingAverage - rate)
		res = residuals
		for _ in range(0, int(len(rate)/2)):
			residuals = np.convolve(residuals, np.ones((N,))/N, mode = 'same')

		maxima_ind = argrelextrema(residuals, np.greater)[0]

		max_days  = np.array([])
		max_res  = np.array([])
		max_rate = np.array([])

		for i in maxima_ind:
			if res[i] > cuttoff:
				max_days  = np.append(max_days, days[i])
				max_res  = np.append(max_res, res[i])
				max_rate = np.append(max_rate, rate[i])

		return [max_days, max_res, max_rate], movingAverage

	def curveFit(self):

		if np.sum(self.rate) == 0:
			self.fit_x = []
			self.fit_y = []
			self.fit_c = []
			return

		if self.disc != np.array([]):
			if len(self.rate) - np.argmax(self.days == self.disc[-1]) < 7:
				start_ind = -8
			else:
				start_ind = np.argmax(self.days == self.disc[-1]) + 3
		else:
			start_ind = 0

		par = np.polyfit(self.cum[start_ind:-1], self.rate[start_ind:-1], 1)
		self.fit_y = self.cum[start_ind:-1] * par[0] + par[1]
		self.fit_c = self.cum[start_ind:-1]
