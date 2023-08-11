import sys, time
import multiprocessing
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QTimer, QProcess, QObject, pyqtSignal
from PyQt5.QtGui import *
from Recording.main import Collect, save
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

path = "./Used_Ui_and_photos/"

class Window(QMainWindow):
    def __init__(self, maxIterations: int = 20, mainScreenShowTime: int = 5):
        super().__init__()
        self.setStyleSheet("background-color: black;")
        uic.loadUi(path + "GUI1.ui", self)  # import the file named "GUI1.ui" from PC
        self.show()

        self.iteration_count = 0
        self.max_iterations = maxIterations

        self.label_Id = 0
        self.arrow_Id = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_screens)
        self.timer.start(mainScreenShowTime * 1000)

    def setupUi(self, Window):
        # set flags for every label
        self.flag_up = True
        self.flag_down = True
        self.flag_left = True
        self.flag_right = True

        self.setWindowTitle("Manual")  # named the GUI window
        self.setWindowIcon(QIcon(path + "icon.ico"))  # set icon to the window

        # connect with labels in Designer APP

        self.forward = self.findChild(QLabel, "UP")  # the name UP is the name of the label in the QT
        self.backward = self.findChild(QLabel, "DOWN")  # the name DOWN is the name of the label in the QT
        self.right = self.findChild(QLabel, "RIGHT")  # the name RIGHT is the name of the label in the QT
        self.left = self.findChild(QLabel, "LEFT")  # the name LEFT is the name of the label in the QT

        self.forward_indicator = self.findChild(QLabel, "forwardIndicator")
        self.backward_indicator = self.findChild(QLabel, "backwardIndicator")
        self.right_indicator = self.findChild(QLabel, "rightIndicator")
        self.left_indicator = self.findChild(QLabel, "leftIndicator")

        self.blackScreen()
        self.forward_indicator.hide()
        self.backward_indicator.hide()
        self.right_indicator.hide()
        self.left_indicator.hide()

        # creating timer for each direction
        timer_up = QTimer(self, interval=83)  # 83.333msec = 12.0 HZ.333
        timer_up.timeout.connect(self.flashing_up)
        timer_up.start()

        timer_down = QTimer(self, interval=100)  # 100msec = 10.0 HZ
        timer_down.timeout.connect(self.flashing_down)
        timer_down.start()

        timer_right = QTimer(self, interval=114)  # 114.28msec = 8.75 HZ.28
        timer_right.timeout.connect(self.flashing_right)
        timer_right.start()

        timer_left = QTimer(self, interval=133)  # 100msec = 7.5 HZ.33
        timer_left.timeout.connect(self.flashing_left)
        timer_left.start()

    def toggle_screens(self):
        if self.iteration_count < self.max_iterations:
            if not self.forward.isVisible():
                self.showMainScreen()
                self.process1 = QProcess(self.forward)
                self.process1.readyReadStandardOutput.connect(self.print_output)
                t = '5'
                label = str(self.label_Id - 1)
                name = "trial_31_7_2023"
                train_path = "D:/Graduation Project/Brain-controlled-wheelchair-with-self-driving-mode/recorded_Data/Train"
                self.process1.start('python', ['record_and_save.py', t, label, name , train_path])
                self.process1.waitForFinished()

            else:
                # self.process1.terminate()
                self.blackScreen()

            self.iteration_count += 1
        else:
            self.timer.stop()
            self.close()

    # creating functions for flashing boxs
    def flashing_up(self):
        if self.flag_up:
            self.forward.setPixmap(QPixmap(path + "NEWUP.PNG"))
        else:
            self.forward.setPixmap(QPixmap(path + "WBD.PNG"))
        self.flag_up = not self.flag_up

    def flashing_down(self):
        if self.flag_down:
            self.backward.setPixmap(QPixmap(path + "NEWDOWN.PNG"))
        else:
            self.backward.setPixmap(QPixmap(path + "WBD.PNG"))
        self.flag_down = not self.flag_down

    def flashing_right(self):
        if self.flag_right:
            self.right.setPixmap(QPixmap(path + "NEWRIGHT.PNG"))
        else:
            self.right.setPixmap(QPixmap(path + "WBD.PNG"))
        self.flag_right = not self.flag_right

    def flashing_left(self):
        if self.flag_left:
            self.left.setPixmap(QPixmap(path + "NEWLEFT.PNG"))
        else:
            self.left.setPixmap(QPixmap(path + "WBD.PNG"))
        self.flag_left = not self.flag_left

    def indicator(self, labelId, show=True):
        labelList = [self.forward_indicator, self.right_indicator, self.backward_indicator, self.left_indicator]
        if show:
            labelList[labelId].show()
        else:
            labelList[labelId].hide()
        for Id, label in enumerate(labelList):
            if Id != labelId:
                label.hide()

    def showArrowsSequentially(self, arrowId):
        arrowList = [self.forward, self.right, self.backward, self.left]
        for Id, arrow in enumerate(arrowList):
            if Id != arrowId:
                arrow.hide()
            else:
                arrow.show()

    def blackScreen(self):
        self.forward.hide()
        self.backward.hide()
        self.left.hide()
        self.right.hide()
        if self.label_Id == 4:
            self.label_Id = 0
        self.indicator(self.label_Id, show=False)

    def showMainScreen(self):
        self.forward.show()
        self.backward.show()
        self.left.show()
        self.right.show()
        if self.label_Id == 4:
            self.label_Id = 0
        self.indicator(self.label_Id)
        self.label_Id += 1
        # if self.arrow_Id == 4:
        #     self.arrow_Id = 0
        # self.showArrowsSequentially(self.arrow_Id)
        # self.arrow_Id += 1

    def print_output(self):
        data = self.process1.readAllStandardOutput()
        output = bytes(data).decode().strip()
        print(output)

if __name__ == "__main__":
    start_time = time.time()
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    window = Window(mainScreenShowTime=6)
    window.setupUi(mainWindow)
    window.showFullScreen()
    app.exec()
    end_time = time.time()
    print(end_time - start_time)