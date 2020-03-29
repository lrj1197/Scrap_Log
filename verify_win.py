from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import sys
import os
import datetime
import pyodbc
import pandas as pd

class VERIFY_WIN(QWidget):
    def __init__(self):
        super().__init__()
        wh = 800
        wd = 600
        try:
            cxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1;DATABASE=Quality_Tracking;UID=lrj1000;PWD=Resistor97!")
            df = pd.read_sql("""select * from Quality_Tracking.dbo.SCRAP where Is_Verified='No';""",cxn)
            cxn.close()
        except Exception as e:
            print(e)
            df = pd.DataFrame()
        if (1):
    ################################################################################
            self.view = QTableWidget(self)
            headers = list(df)
            self.view.setRowCount(df.shape[0])
            self.view.setColumnCount(df.shape[1])
            self.view.setHorizontalHeaderLabels(headers)

            # getting data from df is computationally costly so convert it to array first
            df_array = df.values
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    self.view.setItem(row, col, QTableWidgetItem(str(df_array[row,col])))

            # model = pandasModel(df)
            # self.view = QTableView(self)
            # self.view.setModel(model)
            self.view.resize(800, 400)
    ################################################################################

            self.VERIFY = QPushButton("Verify",self)
            self.VERIFY.move(75,400)
            self.VERIFY.resize(75,25)
            self.VERIFY.setStyleSheet("background-color: green")
            self.VERIFY.clicked.connect(self.VERIFY_)

            self.HELP = QPushButton("Help",self)
            self.HELP.move(75,474)
            self.HELP.resize(75,25)
            self.HELP.setStyleSheet("background-color: orange")
            self.HELP.clicked.connect(self.HELP_)

            self.EXIT = QPushButton("Exit",self)
            self.EXIT.move(75,437)
            self.EXIT.resize(75,25)
            self.EXIT.setStyleSheet("background-color: red")
            self.EXIT.clicked.connect(self.EXIT_)
    ################################################################################

        self.setWindowTitle("I am Homer")
        self.setGeometry(100,100,wh,wd)
        # self.setStyleSheet("background-color: rbg(255,255,255)")
        self.show()

    def VERIFY_(self):
        cxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1;DATABASE=Quality_Tracking;UID=lrj1000;PWD=Resistor97!")
        cus = cxn.cursor()
        for currentQTableWidgetItem in self.view.selectedItems():
            cmd = """
            update [Quality_Tracking].[dbo].[SCRAP] set Is_Verified='Yes' where Part_Num = '{}' and idx = {};
            """.format(currentQTableWidgetItem.text(), self.view.item(currentQTableWidgetItem.row(),8).text())
            cus.execute(cmd)
            cus.commit()
        cxn.close()

        try:
            cxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1;DATABASE=Quality_Tracking;UID=lrj1000;PWD=Resistor97!")
            df = pd.read_sql("""select * from Quality_Tracking.dbo.SCRAP where Is_Verified='no';""",cxn)
            cxn.close()
        except Exception as e:
            print(e)
            df = pd.DataFrame()
        if (1):
    ################################################################################
            self.view.clear()
            headers = list(df)
            self.view.setRowCount(df.shape[0])
            self.view.setColumnCount(df.shape[1])
            self.view.setHorizontalHeaderLabels(headers)

            # getting data from df is computationally costly so convert it to array first
            df_array = df.values
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    self.view.setItem(row, col, QTableWidgetItem(str(df_array[row,col])))

        return

    def HELP_(self):
        return

    def EXIT_(self):
        self.close()
