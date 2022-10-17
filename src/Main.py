from __future__ import with_statement
import sys
from PyQt5.QtWidgets import QApplication
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib import style
from MainWindow import MainWindow
style.use('dark_background')

if __name__ == "__main__":
	app = QApplication(sys.argv)
	dmw = MainWindow()
	dmw.show()
	status = app.exec_()
	sys.exit(status)