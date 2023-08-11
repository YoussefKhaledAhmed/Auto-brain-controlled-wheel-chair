from PyQt5 import uic ,QtWidgets , QtCore
from PyQt5.QtCore import QTimer , QProcess
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow 

path = "D://Graduation Project//Brain-controlled-wheelchair-with-self-driving-mode//BCI_ssvep_realTime//Used_Ui_and_photos//"


class Window(QMainWindow) :
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")
        uic.loadUi(path+"GUI1.ui",self)               #import the file named "GUI1.ui" from PC
        self.show()

    def setupUi(self,Window) :


        #set flags for every label
        self.flag_up = True
        self.flag_down = True
        self.flag_left = True
        self.flag_right = True

        self.setWindowTitle("Manual")                # named the GUI window
        self.setWindowIcon(QIcon(path+"icon.ico"))     #set icon to the window


        #connect with labels in Designer APP

        self.forward = self.findChild(QLabel,"UP")         #the name UP is the name of the label in the QT
        self.backward = self.findChild(QLabel,"DOWN")      #the name DOWN is the name of the label in the QT
        self.right = self.findChild(QLabel,"RIGHT")        #the name RIGHT is the name of the label in the QT
        self.left = self.findChild(QLabel,"LEFT")          #the name LEFT is the name of the label in the QT

        # creating timer for each direction
        timer_up = QTimer(self, interval=83)                     # 83.333msec = 12.0 HZ.333
        timer_up.timeout.connect(self.flashing_up)
        timer_up.start()

        timer_down = QTimer(self, interval=100)                      # 100msec = 10.0 HZ
        timer_down.timeout.connect(self.flashing_down)
        timer_down.start()

        
        timer_right = QTimer(self, interval=114)                  # 114.28msec = 8.75 HZ.28
        timer_right.timeout.connect(self.flashing_right)
        timer_right.start()
        

        timer_left = QTimer(self, interval=133)                   # 100msec = 7.5 HZ.33
        timer_left.timeout.connect(self.flashing_left)
        timer_left.start()

     #creating functions for flashing boxs   
    def flashing_up(self):
        if self.flag_up:
            self.forward.setPixmap(QPixmap(path+"NEWUP.PNG"))
        else:
            self.forward.setPixmap(QPixmap(path+"WBD.PNG"))
        self.flag_up = not self.flag_up

    def flashing_down(self):
        if self.flag_down:
            self.backward.setPixmap(QPixmap(path+"NEWDOWN.PNG"))
        else: 
            self.backward.setPixmap(QPixmap(path+"WBD.PNG"))
        self.flag_down = not self.flag_down

    def flashing_right(self):
        if self.flag_right:
            self.right.setPixmap(QPixmap(path+"NEWRIGHT.PNG"))
        else:
            self.right.setPixmap(QPixmap(path+"WBD.PNG"))
        self.flag_right = not self.flag_right

    def flashing_left(self):
        if self.flag_left:
            self.left.setPixmap(QPixmap(path+"NEWLEFT.PNG"))
        else:
            self.left.setPixmap(QPixmap(path+"WBD.PNG"))
        self.flag_left = not self.flag_left   





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow() 
    window = Window()
    window.setupUi(mainWindow)
    window.show()

    sys.exit(app.exec())



