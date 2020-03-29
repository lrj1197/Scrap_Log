from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import sys
import os
import datetime
import pyodbc
from verify_win import *
from settings_win import *

class MAIN_WIN(QWidget):
    def __init__(self):
        super().__init__()
        wh = 600
        wd = 600
        names = []
        self.idx = []
        self.ADMINUSER = []
        try:
            cxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1;DATABASE=Quality_Tracking;UID=lrj1000;PWD=Resistor97!")
            cus = cxn.cursor()
            cmd = """select name,admin from Quality_Tracking.dbo.USERS;"""
            cus.execute(cmd)
            rows = cus.fetchall()
            for row in rows:
                if row[1] == 'yes':
                    self.ADMINUSER.append(row[0])
                names.append(row[0])
            cmd = """select idx from Quality_Tracking.dbo.SCRAP;"""
            cus.execute(cmd)
            rows = cus.fetchall()
            for i in rows:
                self.idx.append(i[0])
            cxn.close()
        except Exception as e:
            print(e)
            names.append('None')
        # names = ['joe','bob','tom','bill']
        if (1):
    ################################################################################
            self.PN = QLineEdit(self)
            self.PN.move(75,50)
            self.PN.resize(100,25)
            self.PN_L = QLabel("Part Number",self)
            self.PN_L.move(75,25)

            self.QTY = QLineEdit(self)
            self.QTY.move(200,50)
            self.QTY.resize(100,25)
            self.QTY_L = QLabel("Quantity",self)
            self.QTY_L.move(200,25)

            self.DATE = QLineEdit(self)
            self.DATE.move(325,50)
            self.DATE.resize(100,25)
            self.DATE.setReadOnly(True)
            today = datetime.datetime.now().strftime("%D")
            self.DATE.setText(today)
            self.DATE_L = QLabel("Date",self)
            self.DATE_L.move(325,25)

            self.NAME = QComboBox(self)
            self.NAME.move(450,50)
            self.NAME.resize(100,25)
            self.NAME_L = QLabel("Name",self)
            self.NAME_L.move(450,25)
            for name in names:
                self.NAME.addItem(name)
    ################################################################################
            self.REASON = QTextEdit(self)
            self.REASON.move(75,125)
            self.REASON.resize(475,100)
            self.REASON_L = QLabel("Reason",self)
            self.REASON_L.move(225,100)

            self.NOTES = QTextEdit(self)
            self.NOTES.move(75,275)
            self.NOTES.resize(475,100)
            self.NOTES_L = QLabel("NOTES",self)
            self.NOTES_L.move(225,250)
    ################################################################################
            self.SUBMIT = QPushButton("Submit",self)
            self.SUBMIT.move(75,400)
            self.SUBMIT.resize(75,25)
            self.SUBMIT.setStyleSheet("background-color: green")
            self.SUBMIT.clicked.connect(self.SUBMIT_)

            self.VERIFY = QPushButton("Verify",self)
            self.VERIFY.move(162,400)
            self.VERIFY.resize(75,25)
            self.VERIFY.setStyleSheet("background-color: blue")
            self.VERIFY.clicked.connect(self.VERIFY_)

            self.HELP = QPushButton("Help",self)
            self.HELP.move(75,437)
            self.HELP.resize(75,25)
            self.HELP.setStyleSheet("background-color: orange")
            self.HELP.clicked.connect(self.HELP_)

            self.EXIT = QPushButton("Exit",self)
            self.EXIT.move(162,437)
            self.EXIT.resize(75,25)
            self.EXIT.setStyleSheet("background-color: red")
            self.EXIT.clicked.connect(self.EXIT_)

            self.EXCT = QPushButton("Extract",self)
            self.EXCT.move(249,437)
            self.EXCT.resize(75,25)
            self.EXCT.setStyleSheet("background-color: blue")
            self.EXCT.clicked.connect(self.EXCT_)

            self.SET = QPushButton("Settings",self)
            self.SET.move(249,400)
            self.SET.resize(75,25)
            self.SET.setStyleSheet("background-color: orange")
            self.SET.clicked.connect(self.SET_)
    ################################################################################

        self.setWindowTitle("I am Homer")
        self.setGeometry(100,100,wh,wd)
        # self.setStyleSheet("background-color: rbg(255,255,255)")
        self.show()

    def SUBMIT_(self):
        part_num = self.PN.text()
        qty = self.QTY.text()
        date = self.DATE.text()
        name = self.NAME.currentText()
        reason = self.REASON.toPlainText()
        notes = self.NOTES.toPlainText()
        is_verified = 'no'
        try:
            cxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1;DATABASE=Quality_Tracking;UID=lrj1000;PWD=Resistor97!")
            cus = cxn.cursor()
            cmd = """select cost from Quality_Tracking.dbo.COST where PartNum = '{}';""".format(part_num)
            cus.execute(cmd)
            row = cus.fetchall()
            cost = float(qty)*row[0][0]
            cmd = """select idx from Quality_Tracking.dbo.SCRAP;"""
            cus.execute(cmd)
            rows = cus.fetchall()
            # print(self.idx)
            if len(self.idx) == 0:
                idx = 0
            else:
                idx = self.idx[-1]+1
            self.idx.append(idx)
            cmd = """
            INSERT INTO [Quality_Tracking].[dbo].[SCRAP] (Part_Num, Qty, Date, Name, Reason, Notes, Is_Verified, Total_Cost, idx) VALUES ('{}',{},'{}','{}','{}','{}','{}',{},{}) ;
            """.format(part_num, qty, date, name, reason, notes, is_verified, cost, idx)
            cus.execute(cmd)
            cus.commit()
            cxn.close()
        except Exception as e:
            print(e)
            return


    def VERIFY_(self):
        if (self.NAME.currentText() in self.ADMINUSER) == True:
            self.V = VERIFY_WIN()
            self.V.show()
        else:
            print("Access Denied")
            return
    def HELP_(self):
        return

    def EXIT_(self):
        sys.exit()

    def EXCT_(self):
        try:
            cxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1;DATABASE=Quality_Tracking;UID=lrj1000;PWD=Resistor97!")
            df = pd.read_sql("""select * from Quality_Tracking.dbo.SCRAP;""",cxn)
            cxn.close()
            df.to_csv(os.path.join(os.path.expanduser("~"),'scrap.csv'))
        except Exception as e:
            print(e)
    def SET_(self):
        self.S = SETTINGS_WIN()
        self.S.show()
        return

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MAIN_WIN()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
