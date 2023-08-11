#import sys

from PyQt5 import uic , QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton


path = "D://Graduation Project//Brain-controlled-wheelchair-with-self-driving-mode//BCI_ssvep_realTime//Used_Ui_and_photos//"


class autoWindow(QMainWindow) :
    
    def __init__(self, parent=None):
        super().__init__()
        self.setStyleSheet("background-color: black;")
        uic.loadUi(path + "autowindow.ui",self)           #import the file named "autowindow.ui" from PC
        self.show()

    def setupUi(self,autoWindow):

            #set flags for every label

        self.flag_room1 = True
        self.flag_room2 = True
        self.flag_room3 = True
        self.flag_room4 = True


        self.setWindowTitle("AUTO")                       # named the GUI window
        self.setWindowIcon(QIcon(path + "icon.ico"))             #set icon to the window

        #connect with labels in Designer APP

        self.room1 = self.findChild(QLabel,"room1")       #the name room1 is the name of the label in the QT
        self.room2 = self.findChild(QLabel,"room2")       #the name room2 is the name of the label in the QT
        self.room3 = self.findChild(QLabel,"room3")       #the name room3 is the name of the label in the QT
        self.room4 = self.findChild(QLabel,"room4")       #the name room4 is the name of the label in the QT
  
        # creating timer for each room
        timer_room1 = QTimer(self, interval=83)          # 83.333msec = 12.0 HZ.333
        timer_room1.timeout.connect(self.flashing_room1)
        timer_room1.start()

        timer_room3 = QTimer(self, interval=100)             # 100msec = 10.0 HZ
        timer_room3.timeout.connect(self.flashing_room3)
        timer_room3.start()

        
        timer_room4 = QTimer(self, interval=114)           # 114.28msec = 8.75 HZ.28
        timer_room4.timeout.connect(self.flashing_room4)
        timer_room4.start()
        

        timer_room2 = QTimer(self, interval=133)            # 100msec = 7.5 HZ.33
        timer_room2.timeout.connect(self.flashing_room2)
        timer_room2.start()

     #creating functions for flashing boxs   
    def flashing_room1(self):
        if self.flag_room1:
            self.room1.show()
        else:
            self.room1.hide()
        self.flag_room1 = not self.flag_room1

    def flashing_room2(self):
        if self.flag_room2:
            self.room2.show()
        else:
            self.room2.hide()
        self.flag_room2 = not self.flag_room2

    def flashing_room3(self):
        if self.flag_room3:
            self.room3.show()
        else:
            self.room3.hide()
        self.flag_room3 = not self.flag_room3

    def flashing_room4(self):
        if self.flag_room4:
            self.room4.show()
        else:
            self.room4.hide()
        self.flag_room4 = not self.flag_room4
    




'''app = QApplication(sys.argv)
window = autoWindow()
window.show()

sys.exit(app.exec())'''


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = autoWindow()
    ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())