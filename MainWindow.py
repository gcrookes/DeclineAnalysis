import numpy as np
import pandas as pd
import datetime
import pickle
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTreeWidgetItem, QFileDialog, QFileDialog, QInputDialog, QSizePolicy
from Constraint_Menu import Ui_ConstraintWindow
from mainwindow_v5 import Ui_MainWindow
from Well import Well
from DraggableLine import DraggableLine
from ImportWindow import Ui_ImportWindow
from Constraint_Menu import Ui_ConstraintWindow, Ui_SelectorWindow

class ConstraintWindow(QMainWindow, Ui_ConstraintWindow):
	
	def __init__(self, parent = None):
		super(ConstraintWindow, self).__init__(parent)
		self.setupUi(self, parent)

class SelectWindow(QMainWindow, Ui_SelectorWindow):
	
	def __init__(self, parent = None):
		super(SelectWindow, self).__init__(parent)
		self.setupUi(self)

class DesignerImportWindow(QMainWindow, Ui_ImportWindow):

	def __init__(self, parent = None):
		super(DesignerImportWindow, self).__init__(parent)
		self.setupUi(self, parent)
		self.setWindowTitle('Decline Analysis Application')

class MainWindow(QMainWindow, Ui_MainWindow):
	
	first = True
	Field = None
	Well = None
	save_path = None

	def __init__(self, parent = None):
		# Initialize the main window
		# Setup the main window for the application
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setWindowTitle('Decline Analysis Application')
		
		# Setup other windows that can be called throughout the code
		self.importwindow     = DesignerImportWindow(self) 
		self.constraintwindow = ConstraintWindow(self)
		self.wellSelectUI     = SelectWindow(self)
		self.treeWidget.setHeaderHidden(True)

		self.Units = 1

		# Connect all of the widgets
		self.treeWidget.currentItemChanged.connect(self.new_selection)
		self.actionMetric.triggered.connect(lambda: self.changeUnits(0))
		self.actionImperial.triggered.connect(lambda: self.changeUnits(1))
		self.actionProject_Constraints.triggered.connect(lambda: self.set_constraints(False))
		self.actionConstrain_Well.triggered.connect(lambda: self.set_constraints(True))
		self.actionSave_File.triggered.connect(self.save_file)
		self.actionSave_File_As.triggered.connect(self.save_file_as)
		self.actionOpen_File.triggered.connect(self.open_file)
		self.actionImport_From_Excel.triggered.connect(self.Call_Import_Table)
		self.actionImport_From_Excel.setShortcut('Ctrl+i')
		self.actionProject_Constraints.setShortcut('Ctrl+p')
		self.actionConstrain_Well.setShortcut('Ctrl+w')
		self.actionSave_File.setShortcut('Ctrl+s')
		self.actionOpen_File.setShortcut('Ctrl+o')

		self.PlotUI.clicked.connect(self.toggleLine)
		self.UnitsUI.clicked.connect(self.toggleUnit)
		self.ExportToExcelUI.clicked.connect(self.excel_export)

		self.actionScatter.triggered.connect(lambda: self.plot_fun(True))
		self.actionLine.triggered.connect(lambda: self.plot_fun(False))
		self.plotScatter = False

		self.switch_Gas()

	def excel_export(self):

		if self.Field is None: return

		uwis = list(self.Field.keys())

		items = ('PDP','PD','TP','P+PDP','P+PD','TPP','P+P+PDP','P+P+PD','TPPP')
		item, ok = QInputDialog.getItem(self, 'Reserves Category ', 'Select Reserves Category:', items,0,False)

		d = {'UWI':uwis,'Plan':'Working','Segment Index':1,'Start Date': datetime.datetime.today(),'Reserves Category':item,'Cum To End':0,'Segment Volume':0,'N':0,'Df':0,'Di':0,'Qf':0,'Qi':0,'Duration':0,'Product':0}

		exportData = pd.DataFrame(d)
		exportData.set_index('UWI', inplace = True)

		for uwi in self.Field:
			
			well = self.Field[uwi]

			if well.best_fit_gas is None and well.best_fit_oil is None:
				exportData.drop([uwi], inplace = True)

			else:

				if well.best_fit_gas is not None:
					exportData.loc[uwi,'Cum To End'] = well.best_fit_gas.EUR
					exportData.loc[uwi,'Segment Volume'] = well.best_fit_gas.EUR
					exportData.loc[uwi,'N'] = well.best_fit_gas.N
					exportData.loc[uwi,'Df'] = well.best_fit_gas.Df
					exportData.loc[uwi,'Di'] = well.best_fit_gas.Di
					exportData.loc[uwi,'Qf'] = well.best_fit_gas.Qf
					exportData.loc[uwi,'Qi'] = well.best_fit_gas.Qi
					exportData.loc[uwi,'Duration'] = well.best_fit_gas.Dur
					exportData.loc[uwi,'Product'] = 'Gas'

				if well.best_fit_oil is not None:
					exportData.loc[uwi,'Cum To End'] = well.best_fit_oil.EUR
					exportData.loc[uwi,'Segment Volume'] = well.best_fit_gas.EUR
					exportData.loc[uwi,'N'] = well.best_fit_gas.N
					exportData.loc[uwi,'Df'] = well.best_fit_gas.Df
					exportData.loc[uwi,'Di'] = well.best_fit_gas.Di
					exportData.loc[uwi,'Qf'] = well.best_fit_gas.Qf
					exportData.loc[uwi,'Qi'] = well.best_fit_gas.Qi
					exportData.loc[uwi,'Duration'] = well.best_fit_gas.Dur
					exportData.loc[uwi,'Product'] = 'Oil'

		self.warningMessage('You take all responsibility for ensuring correct declines are loaded into ValNav\n This tool is for your convience and is not intended to be a perfect reserves solution')
		name = QFileDialog.getSaveFileName(self, 'Save File')
		name = name[0]

		try: exportData.to_csv(name+'.csv')
		except: self.warningMessage('Error encountered while saving')

		self.warningMessage('Gas Values in Mcf and Oil values in bbl')


	def toggleUnit(self):
		self.changeUnits([1,0][self.Units])

	def toggleLine(self):
		self.plotScatter = not self.plotScatter
		self.update_graph()

	def switch_Gas(self):
		try:
			if self.Well.best_fit_gas is None: 
				self.ParameterFrame.clear_text()
			else:
				self.ParameterFrame.set_text(self.Well.best_fit_gas.get_parameters())
		except:
			self.ParameterFrame.clear_text()

		self.ParameterFrame.set_units(['E3m3','Mcf'][self.Units])
		self.plotWidget.canvas.show_gas()

	def switch_Oil(self):
		try:
			if self.Well.best_fit_oil is None: 
				self.ParameterFrame.clear_text()
			else:
				self.ParameterFrame.set_text(self.Well.best_fit_oil.get_parameters())
		except:
			self.ParameterFrame.clear_text()

		self.ParameterFrame.set_units(['m3','bbl'][self.Units])
		self.plotWidget.canvas.show_oil()

	# ________________________________________________________________________________________________________________________________________________
	# ________________________________________________________________________________________________________________________________________________
	# The save and load code for the application

	def plot_fun(self, scatter):
		self.plotScatter = scatter
		self.update_graph()

	def get_save_path(self):
		# Pulls up the Dialog box to choose a save file name
		name = QFileDialog.getSaveFileName(self, 'Save File')

		# Add the format onto the end of the name if required
		if not name[0].endswith('.da'):
			self.save_path = str(name[0]) + '.da'
		else:
			self.save_path = name[0]

	def save_file_as(self):
		# If the Save As is pressed then we want to prompt for a path so set the path variable to None
		self.save_path = None
		self.save_file()

	def save_file(self):
		# Function to actually save file

		# Get a path name if you need it
		if self.save_path is None:
			self.get_save_path()

		file = open(self.save_path,'wb')

		# If the Field is empty skip the save file formatting and dump in a blank array
		if self.Field is None:
			save_array = []
		else:
			# Initialize the array
			save_array = np.zeros(14)

			# Loop over all of the well objects in the Field
			for uwi in self.Field:
				well = self.Field[uwi]
				
				# Determine if best fit lines have been created for the well
				if well.best_fit_gas is not None:
					a  = well.best_fit_gas.line
					an = well.best_fit_gas.N
				else:
					a  = None
					an = None
				if well.best_fit_oil is not None:
					b  = well.best_fit_oil.line
					bn = well.best_fit_oil.N
				else:
					b  = None
					bn = None

				# Stack the current well onto the end of the array
				save_array = np.vstack((save_array,np.array([uwi,well.gasRate,well.oilRate,well.dates,a,b,well.Qf_const_gas, well.Df_const_gas,well.Dur_const_gas,an,bn,well.Qf_const_oil, well.Df_const_oil,well.Dur_const_oil])))
			
		# Dump the array into the file and close it
		pickle.dump(save_array, file)
		file.close()

	# Should probably push some of the functionallity in this into the well class
	def open_file(self):
		# Open and load from a .da file

		# Get the file from a browser window and leave if no file was selected
		name = QFileDialog.getOpenFileName(self, 'Open File')
		if name == ('', ''): return

		# Check for a .da file format
		if name[0][-3:] != '.da':
				self.warningMessage('Invalid file type. Please import a .da file')
				return		

		# Open the file get out the array and close it
		with open(name[0], 'rb') as input:
			open_array = pickle.load(input)
			input.close()

		# Initialize the field
		self.Field = {}
		#	0      1            2           3     4 5        6              7                 8               9  10        11                  12              13
		#[uwi,well.gasRate,well.oilRate,well.dates,a,b,well.Qf_const_gas, well.Df_const_gas,well.Dur_const_gas,an,bn,well.Qf_const_oil, well.Df_const_oil,well.Dur_const_oil]
		
		# Cycle over each line in the loaded array and create a well from it
		for i in range(1, len(open_array)):
			self.Field[open_array[i,0]] = Well(open_array[i,0],open_array[i,3],open_array[i,1],open_array[i,2])
			self.Field[open_array[i,0]].Qf_const_gas = open_array[i,6]
			self.Field[open_array[i,0]].Df_const_gas = open_array[i,7]
			self.Field[open_array[i,0]].Dur_const_gas = open_array[i,8]

			self.Field[open_array[i,0]].Qf_const_oil = open_array[i,11]
			self.Field[open_array[i,0]].Df_const_oil = open_array[i,12]
			self.Field[open_array[i,0]].Dur_const_oil = open_array[i,12]

			if open_array[i,4] is not None:
				# Gas line is present
				x = open_array[i,4].get_xdata()
				y = open_array[i,4].get_ydata()

				self.Field[open_array[i,0]].best_fit_gas = DraggableLine(self,self.Field[open_array[i,0]],self.plotWidget.canvas.gascum,[x[0],x[50],x[-1]],[y[0],y[50],y[-1]],'r',1,ax2 = self.plotWidget.canvas.gastime)
				self.Field[open_array[i,0]].best_fit_gas.N = open_array[i,9]
				self.Field[open_array[i,0]].best_fit_gas.line = open_array[i,4]
				
			if open_array[i,5] is not None:
				# Oil line is present
				x = open_array[i,5].get_xdata()
				y = open_array[i,5].get_ydata()

				self.Field[open_array[i,0]].best_fit_oil = DraggableLine(self,self.Field[open_array[i,0]],self.plotWidget.canvas.oilcum,[x[0],x[50],x[-1]],[y[0],y[50],y[-1]],'g',2, self.plotWidget.canvas.oiltime)
				self.Field[open_array[i,0]].best_fit_oil.N = open_array[i,10]
				self.Field[open_array[i,0]].best_fit_oil.line = open_array[i,5]
 
 		# Clear the plot
		try: 
			for artist in self.plotWidget.canvas.gascum.lines + self.plotWidget.canvas.gascum.collections + self.plotWidget.canvas.oilcum.lines + self.plotWidget.canvas.oilcum.collections + self.plotWidget.canvas.gastime.lines + self.plotWidget.canvas.gastime.collections + self.plotWidget.canvas.oiltime.lines + self.plotWidget.canvas.oiltime.collections:
				artist.remove()
		except: pass
		
		# Redraw the plot and bring the final list into the application
		self.plotWidget.canvas.draw()
		self.update_list(self.Field)
		self.ParameterFrame.clear_text()
		self.save_path = name[0]

	# ________________________________________________________________________________________________________________________________________________
	# ________________________________________________________________________________________________________________________________________________
	# Load, Set, Reset Constraints

	# This function pulls up the constraint window
	def set_constraints(self, local):
		# local being true indicates that it is just this well
		# Check some conditions to set constraints
		if self.Field is None:
			self.warningMessage('Need to import wells before setting project constraint')
			return			

		if self.Well is None:
			self.warningMessage('Need an active well to set well constraints')
			return

		# Get current constraints and put it into the menu
		if self.activeFluid == 1:
			self.constraintwindow.load_menu(self.Well.Qf_const_gas,self.Well.Df_const_gas,self.Well.Dur_const_gas,self.Units,local,1)
		else:
			self.constraintwindow.load_menu(self.Well.Qf_const_oil,self.Well.Df_const_oil,self.Well.Dur_const_oil,self.Units,local,2)

	# This function changes the constraints after it is called
	def update_constraints(self, uwis, Qf, Df, Dur, fluid):

		for well in uwis:

			if fluid == 1:
				self.Field[well].Qf_const_gas  = Qf
				self.Field[well].Df_const_gas  = Df
				self.Field[well].Dur_const_gas = Dur

				if self.Field[well].best_fit_gas is not None:
					x = self.Field[well].best_fit_gas.line.get_xdata()
					y = self.Field[well].best_fit_gas.line.get_ydata()

					xs, ys, ts = self.Field[well].best_fit_gas.calc_line(x[0], y[0], x[50], y[50], self.Field[well].best_fit_gas.N)

					self.Field[well].best_fit_gas.line.set_xdata(xs)
					self.Field[well].best_fit_gas.line.set_ydata(ys)
					self.Field[well].best_fit_gas.line2.set_xdata(ts)
					self.Field[well].best_fit_gas.line2.set_ydata(ys)

					self.Field[well].best_fit_gas.canvas.draw()

			else:

				self.Field[well].Qf_const_oil  = Qf
				self.Field[well].Df_const_oil  = Df
				self.Field[well].Dur_const_oil = Dur

				if self.Field[well].best_fit_oil is not None:
					x = self.Field[well].best_fit_oil.line.get_xdata()
					y = self.Field[well].best_fit_oil.line.get_ydata()

					xs, ys, ts = self.Field[well].best_fit_oil.calc_line(x[0], y[0], x[50], y[50], self.Field[well].best_fit_oil.N)

					self.Field[well].best_fit_oil.line.set_xdata(xs)
					self.Field[well].best_fit_oil.line.set_ydata(ys)
					self.Field[well].best_fit_oil.line2.set_xdata(ts)
					self.Field[well].best_fit_oil.line2.set_ydata(ys)

					self.Field[well].best_fit_oil.canvas.draw()

	def changeUnits(self, unit):
		
		if self.Units == unit: return

		self.Units = unit
		self.plotWidget.canvas.update_units(unit)

		if unit == 0:
			# This will be metric units
			self.ParameterFrame.set_units(['E3m3','m3'][self.activeFluid - 1])
			fluid_conv = 1/6.289
			gas_conv   = 1/35.494
		elif unit == 1:
			# Imperial units
			self.ParameterFrame.set_units(['m3','bbl'][self.activeFluid - 1])
			fluid_conv = 6.289
			gas_conv   = 35.494

		if self.Field is None: return

		for well in self.Field:
			
			self.Field[well].gasRate        *= gas_conv
			self.Field[well].gasCum         *= gas_conv
			self.Field[well].gasCum_plot    *= gas_conv
			self.Field[well].oilRate	    *= fluid_conv 
			self.Field[well].oilCum		    *= fluid_conv
			self.Field[well].oilCum_plot    *= fluid_conv

			self.Field[well].Qf_const_gas   *= gas_conv
			self.Field[well].Qf_const_oil   *= fluid_conv

			if self.Field[well].best_fit_gas is not None: 
				self.Field[well].best_fit_gas.line.set_xdata(self.Field[well].best_fit_gas.line.get_xdata()*gas_conv)
				self.Field[well].best_fit_gas.line.set_ydata(self.Field[well].best_fit_gas.line.get_ydata()*gas_conv)
				self.Field[well].best_fit_gas.Qi = str(round(float(self.Field[well].best_fit_gas.Qi)*gas_conv,3))
				self.Field[well].best_fit_gas.Qf = str(round(float(self.Field[well].best_fit_gas.Qf)*gas_conv,3))
				try: self.Field[well].best_fit_gas.EUR = str(round(float(self.Field[well].best_fit_gas.EUR)*gas_conv,0))
				except: pass
				self.Field[well].best_fit_gas.final_point[0] *= gas_conv
				self.Field[well].best_fit_gas.final_point[1] *= gas_conv
				
			if self.Field[well].best_fit_oil is not None:
				self.Field[well].best_fit_oil.line.set_xdata(self.Field[well].best_fit_oil.line.get_xdata()*fluid_conv)
				self.Field[well].best_fit_oil.line.set_ydata(self.Field[well].best_fit_oil.line.get_ydata()*fluid_conv)
				self.Field[well].best_fit_oil.Qi = str(round(float(self.Field[well].best_fit_oil.Qi)*fluid_conv,3))
				self.Field[well].best_fit_oil.Qf = str(round(float(self.Field[well].best_fit_oil.Qf)*fluid_conv,3))
				try: self.Field[well].best_fit_oil.EUR = str(round(float(self.Field[well].best_fit_oil.EUR)*fluid_conv,0))
				except: pass
				self.Field[well].best_fit_oil.final_point[0] *= fluid_conv
				self.Field[well].best_fit_oil.final_point[1] *= fluid_conv

			try:self.Field[well].Selector_gas.disconnect()
			except: pass

			try:self.Field[well].Selector_oil.disconnect()
			except: pass

		self.update_graph()

		try: self.Well.best_fit_gas.update_UI()
		except: pass

		try: self.Well.best_fit_oil.update_UI()
		except: pass


	def Call_Import_Table(self):
		try:
			self.importwindow.open_file()
		except ImportError as err:
			self.warningMessage(err)

	def Load_Data(self, df):
		
		UWIs, ind, count = np.unique(np.array(df['UWI']), return_index = True, return_counts = True)

		Date  = np.array(df['date'])
		zerolen  = len(Date)

		try:
			Oil = np.array(df['oil'])
			self.constraintwindow.load_menu(0.001,1,30,self.Units,False,2)
		except:
			Oil = np.zeros(zerolen)

		try:
			Gas = np.array(df['gas'])
			self.constraintwindow.load_menu(0.01,1,30,self.Units,False,1)
		except:Gas = np.zeros(zerolen)

		Field = {}

		for i in range(0, len(UWIs)):
			UWI = UWIs[i]
			date  = Date[ind[i]:ind[i]+count[i]]
			oil   = Oil[ind[i]:ind[i]+count[i]]
			gas   = Gas[ind[i]:ind[i]+count[i]]

			Field[UWI] = Well(UWI, date, gas, oil)

		self.Field = Field
		self.update_list(Field) 
		self.ParameterFrame.clear_text()

	def Lasso_Decline(self):

		self.clear_lines()

		self.plotWidget.canvas.draw()

		if self.activeFluid == 1:
			self.Well.Selector_gas(self, self.plotWidget.canvas.gascum, self.plotWidget.canvas.gastime, self.gasScat)
			self.sel_gas  = self.Well.Selector_gas
			self.las_gas = self.Well.Selector_gas.lasso
		else:
			self.Well.Selector_oil(self, self.plotWidget.canvas.oilcum, self.plotWidget.canvas.oiltime, self.oilScat)
			self.sel_oil = self.Well.Selector_oil
			self.las_oil = self.Well.Selector_oil.lasso

	def clear_lines(self):
		if self.Well.best_fit_gas != None:

			try: self.Well.best_fit_gas.disconnect()
			except: pass

			try: self.Well.best_fit_gas.line.remove()
			except: pass

		if self.Well.best_fit_oil != None:

			try: self.Well.best_fit_oil.disconnect()
			except: pass

			try: self.Well.best_fit_oil.line.remove()
			except: pass

		try: self.sel_gas.line_gas.disconnect()
		except: pass
		
		try: self.sel_gas.disconnect()
		except: pass

		try: self.sel_gas.line_gas.line.remove()
		except: pass

		try: self.sel_oil.line_oil.disconnect()
		except: pass
		
		try: self.sel_oil.disconnect()
		except: pass

		try: self.sel_oil.line_oil.line.remove()
		except: pass

		try: self.las_gas.disconnect_events()
		except:pass
		try: self.las_oil.disconnect_events()
		except:pass

	def update_graph(self):

		if self.first:
			self.BestFitFromSelectionUI.clicked.connect(lambda:self.Lasso_Decline())
			self.first = False
		else:
			self.clear_lines()


		# This tries to clear the old plots if there is anything present
		try: 
			for artist in self.plotWidget.canvas.gascum.lines + self.plotWidget.canvas.gascum.collections:
				try: artist.remove()
				except: pass
		except: pass

		try: 
			for artist in self.plotWidget.canvas.gastime.lines + self.plotWidget.canvas.gastime.collections:
				try: artist.remove()
				except: pass
		except: pass

		try:
			for artist in self.plotWidget.canvas.oilcum.lines + self.plotWidget.canvas.oilcum.collections:
				try: artist.remove()
				except: pass
		except: pass

		try:
			for artist in self.plotWidget.canvas.oiltime.lines + self.plotWidget.canvas.oiltime.collections:
				try: artist.remove()
				except: pass
		except: pass

		#Plot rates and update axis limits
		if not self.plotScatter:
			self.gascum  = self.plotWidget.canvas.gascum.plot(self.Well.gasCum_plot, self.Well.gasRate, color = 'r', label = 'Gas Rate')
			self.oilcum = self.plotWidget.canvas.oilcum.plot(self.Well.oilCum_plot, self.Well.oilRate, color = 'g', label = 'Oil Rate')
			self.gasTScat = self.plotWidget.canvas.gastime.plot(self.Well.months, self.Well.gasRate, color = 'r', label = 'Gas Rate')
			self.oilTScat = self.plotWidget.canvas.oiltime.plot(self.Well.months, self.Well.oilRate, color = 'g', label = 'Oil Rate')

		self.gasScat  = self.plotWidget.canvas.gascum.scatter(self.Well.gasCum_plot, self.Well.gasRate, s = 5, c = 'r', label = 'Gas Rate')
		self.gasTScat = self.plotWidget.canvas.gastime.scatter(self.Well.months, self.Well.gasRate, s = 5, c = 'r', label = 'Gas Rate')
		self.oilScat  = self.plotWidget.canvas.oilcum.scatter(self.Well.oilCum_plot, self.Well.oilRate, s = 5, c = 'g', label = 'Oil Rate')
		self.oilTScat = self.plotWidget.canvas.oiltime.scatter(self.Well.months, self.Well.oilRate, s = 5, c = 'g', label = 'Oil Rate')
		
		if self.Well.best_fit_gas is None:
			self.plotWidget.canvas.update_axis(self.Well.gasCum_plot[-1] * 2, self.Well.months[-1] * 2, max(self.Well.gasRate) * 1.2, 2) 
		else:
			self.plotWidget.canvas.update_axis(self.Well.best_fit_gas.line.get_xdata()[-1] * 1.1, self.Well.months[-1] * 1.1, max(self.Well.gasRate) * 1.2, 2) 

		if self.Well.best_fit_oil is None:
			self.plotWidget.canvas.update_axis(self.Well.oilCum_plot[-1] * 2, self.Well.months[-1] * 2, max(self.Well.oilRate) * 1.2, 1)  
		else:
			self.plotWidget.canvas.update_axis(self.Well.best_fit_oil.line.get_xdata()[-1] * 1.1, self.Well.months[-1] * 1.1, max(self.Well.oilRate) * 1.2, 1)

		self.ParameterFrame.clear_text()

		if self.Well.best_fit_gas is None:
			self.Well.Selector_gas(self, self.plotWidget.canvas.gascum, self.plotWidget.canvas.gastime, self.gasScat)
			self.sel_gas = self.Well.Selector_gas
			self.las_gas = self.Well.Selector_gas.lasso
		else:
			self.sel_gas = self.Well.best_fit_gas
			self.Well.best_fit_gas.update_parent(self.sel_gas.canvas.gascum, self.sel_gas.canvas.gastime)
			self.sel_gas.connect()
			self.sel_gas.update_UI()

		if self.Well.best_fit_oil is None:
			self.Well.Selector_oil(self, self.plotWidget.canvas.oilcum, self.plotWidget.canvas.oiltime, self.oilScat)
			self.sel_oil = self.Well.Selector_oil
			self.las_oil = self.Well.Selector_oil.lasso
		else:
			self.sel_oil = self.Well.best_fit_oil
			self.Well.best_fit_oil.update_parent(self.sel_oil.canvas.oilcum,self.sel_oil.canvas.oiltime)
			self.sel_oil.connect()
			self.sel_oil.update_UI()

		self.plotWidget.canvas.draw()

	def new_selection(self, item):
		self.Well = self.Field[item.text(0)]
		self.update_graph()

	def update_list(self, Field):
		keys = list(Field.keys())

		self.tree_items = {}
		
		for uwi in keys:
			self.tree_items[uwi] = QTreeWidgetItem([uwi])
			self.treeWidget.addTopLevelItem(self.tree_items[uwi])

		self.Field = Field

	def warningMessage(self, text):
		msgBox = QMessageBox()
		msgBox.setText(str(text))
		msgBox.exec_()