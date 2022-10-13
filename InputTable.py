from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidget, QComboBox, QTableWidgetItem, QCheckBox, QMessageBox
import numpy as np
import pandas as pd

class InputTable(QTableWidget):

    def __init__(self, parent, df, name):
            super(QTableWidget, self).__init__(parent)
            self.name = name
            self.df = df

            cols = df.columns
            self.l = len(cols)

            self.oillabels   = ['Cal. Oil Rate']
            self.condlabels  = []#['Cal. Condensate Rate']
            self.waterlabels = []#['Cal. Water Rate']
            self.dailylabels = []#['Cal. Daily Fluid']
            self.UWIlabels   = ['UWI']

            self.passlabels  = [''] + self.UWIlabels
            self.datelabels  = ['Date']
            self.timelabels  = []#['Time On Production']
            self.fluidlabels = self.oillabels + self.condlabels + self.waterlabels + self.dailylabels
            self.gaslabels   = ['Cal. Gas Rate']

            self.toplist = self.passlabels + self.datelabels + self.timelabels + self.fluidlabels + self.gaslabels

            # Don't forget to update the proper conversion             
            self.datelist  = ['YYYY-MM-DD','YYYY-DD-MM','MM-DD-YYYY','DD-MM-YYYY','YYYY/MM/DD','YYYY/DD/MM','MM/DD/YYYY','DD/MM/YYYY','MMM-YY','YY-MMM','MMM/YY','YY/MMM']
            self.timelist  = ['Hours','Days','Months']
            self.fluidlist = ['m3/day','E3m3/day','bbl/day','Mbbl/day']
            self.gaslist   = ['E3m3/day','m3/day','Mscf/day','MMscf/day']

            self.dateconv  = ['YYYY-MM-DD','YYYY-DD-MM','MM-DD-YYYY','DD-MM-YYYY','YYYY/MM/DD','YYYY/DD/MM','MM/DD/YYYY','DD/MM/YYYY','%b-%y','%y-%b','%b/%y','%y/%b']
            self.timeconv  = [1,1/24,1/30.5]             # Converts everything into hours
            self.fluidconv = [1,1000,0.158987,158.987]   # Converts everything into m3/day
            self.gasconv   = [1,1/1000,35.3147,35314.7]  # Converts everything into 1000m3/day

            self.setColumnCount(self.l)
            self.setRowCount(25)

            self.last_iteration = np.array([])
            
            self.top_boxes = {}
            self.lower_boxes = {}

            for i in range(self.l):
                s = str(i)

                self.last_iteration = np.append(self.last_iteration,'')

                self.top_boxes[name+'_'+s] = QComboBox(self)
                self.top_boxes[name+'_'+s].addItems(self.toplist)
                self.top_boxes[name+'_'+s].activated.connect(self.changeTop)

                self.lower_boxes[name+'_'+s] = QComboBox(self)

                self.setCellWidget(0,i,self.top_boxes[name+'_'+s])
                self.setCellWidget(1,i,self.lower_boxes[name+'_'+s])
                self.setHorizontalHeaderItem(i,QTableWidgetItem(None))


                try:
                    if cols[i].startswith('Unnamed:'):
                        item = QTableWidgetItem('')
                    else:
                        item = QTableWidgetItem(cols[i])
                except:
                    try: 
                        item = QTableWidgetItem(str(cols[i]))
                    except:
                        item = QTableWidgetItem('')


                item.setTextAlignment(QtCore.Qt.AlignHCenter)
                self.setItem(2,i,item)



                for j in range(min(23, len(df[cols[0]]))):

                    if i == 0:
                        self.setCellWidget(j+2,0,QCheckBox(self))
                        self.cellWidget(j+2,0).setCheckState(2)

                    if not pd.isna(df[cols[i]][j]):
                        item = QTableWidgetItem(str(df[cols[i]][j]))
                    else:
                        item = QTableWidgetItem('')

                    item.setTextAlignment(QtCore.Qt.AlignHCenter)
                    self.setItem(j+3,i,item)

            for i in range(25):
                self.setVerticalHeaderItem(i,QTableWidgetItem(None))

            self.setHorizontalHeaderItem(0,QTableWidgetItem(None))
            self.horizontalHeader().setSectionResizeMode(1)
            self.verticalHeader().setSectionResizeMode(1)
            self.setSizePolicy(2,2)

    def changeTop(self, selected):

        i = 0

        for box in self.top_boxes:
            if self.last_iteration[i] != self.top_boxes[box].currentText():
                selection = self.top_boxes[box].currentText()
                self.last_iteration[i] = selection
                changed = box
                break
            else:
                i += 1
        else:
            selection = ''

        i = 0

        self.lower_boxes[box].clear()

        if selection in self.passlabels:
            pass
        elif selection in self.datelabels:
            self.lower_boxes[box].addItems(self.datelist)
        elif selection in self.timelabels:
            self.lower_boxes[box].addItems(self.timelist)
        elif selection in self.fluidlabels:
            self.lower_boxes[box].addItems(self.fluidlist)
        elif selection in self.gaslabels:
            self.lower_boxes[box].addItems(self.gaslist)

    def import_table(self):

        cols = self.df.columns

        save_df = self.df

        UWI  = False
        Date = False
        Rate = False


        return_df = pd.DataFrame()

        dropIndicies = []

        for i in range(22):
            try:
                if self.cellWidget(i+2,0).checkState() == 0:
                    dropIndicies.append(i)
            except AttributeError:
                pass

        if len(dropIndicies)>0:
            self.df.drop(self.df.index[dropIndicies], inplace = True)


        i = 0
        for box in self.top_boxes:
            if self.top_boxes[box].currentText() in self.gaslabels:
                return_df['gas'] = self.df[cols[i]] * self.gasconv[self.lower_boxes[box].currentIndex()]
                Rate = True

            elif self.top_boxes[box].currentText() in self.condlabels:
                return_df['cond'] = self.df[cols[i]] * self.fluidconv[self.lower_boxes[box].currentIndex()]
                Rate = True

            elif self.top_boxes[box].currentText() in self.waterlabels:
                return_df['water'] = self.df[cols[i]] * self.fluidconv[self.lower_boxes[box].currentIndex()]
                Rate = True

            elif self.top_boxes[box].currentText() in self.oillabels:
                return_df['oil'] = self.df[cols[i]] * self.fluidconv[self.lower_boxes[box].currentIndex()]      
                Rate = True     

            elif self.top_boxes[box].currentText() in self.dailylabels:
                return_df['daily'] = self.df[cols[i]] * self.fluidconv[self.lower_boxes[box].currentIndex()]
                Rate = True

            elif self.top_boxes[box].currentText() in self.datelabels:
                try:
                    print( self.dateconv[self.lower_boxes[box].currentIndex()])
                    return_df['date'] = pd.to_datetime(self.df[cols[i]], format = self.dateconv[self.lower_boxes[box].currentIndex()])
                    Date = True
                except:
                    try:
                        return_df['date'] = pd.to_datetime(self.df[cols[i]])
                        Date = True
                        msgBox = QMessageBox()
                        msgBox.setText('The given date format could not be parsed. \nAn alternate format was used please check the imported values')
                        msgBox.exec_()
                        self.df = save_df
                    except: 
                        msgBox = QMessageBox()
                        msgBox.setText('Date format could not be parsed. Table was not imported')
                        msgBox.exec_()
                        self.df = save_df
                        raise ValueError

            elif self.top_boxes[box].currentText() in self.timelabels:
                return_df['time'] = self.df[cols[i]] * self.timeconv[self.lower_boxes[box].currentIndex()]

            elif self.top_boxes[box].currentText() in self.UWIlabels:
                return_df['UWI'] = self.df[cols[i]]
                UWI = True

            i += 1


        if not all([UWI, Date, Rate]) and any([UWI, Date, Rate]):
            msgBox = QMessageBox()
            msgBox.setText('Need to map at least UWI, Date, and one rate \n Error on sheet "' + self.name+'"')
            msgBox.exec_()
            self.df = save_df
            raise ValueError

        if (not (UWI and Date and Rate)) and (not (UWI or Date or Rate)):
            self.df = save_df
            raise ValueError

        return_df.fillna(0,inplace = True)
        return return_df


