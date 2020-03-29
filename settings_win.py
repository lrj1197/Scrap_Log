from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import sys
import os
import datetime
import pyodbc
import pandas as pd

class SETTINGS_WIN(QWidget):
    def __init__(self):
        super().__init__()
        wh = 800
        wd = 600

        if (1):
    ################################################################################

    ################################################################################

            self.SAVE = QPushButton("Save",self)
            self.SAVE.move(75,400)
            self.SAVE.resize(75,25)
            self.SAVE.setStyleSheet("background-color: green")
            self.SAVE.clicked.connect(self.SAVE_)

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

    def SAVE_(self):
        return

    def EXIT_(self):
        self.close()
