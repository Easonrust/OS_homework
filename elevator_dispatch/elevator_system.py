from Ui_elevator import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5 import QtCore, QtGui
from controller import ElevatorController, Controller


class myWindow(QMainWindow, Ui_Form):

    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)
        self.setupUi(self)

        # 五部电梯房间按钮连接函数
        for i in range(5):
            for j in range(20):
                self.controller.elevatorController[i].roombutton[j].clicked.connect(
                    self.operate_ele)

        # 五部电梯开门按钮连接函数
        for i in range(5):
            self.controller.elevatorController[i].openButton.clicked.connect(
                self.open_door)

        # 每层楼召唤电梯按钮连接函数
        for i in range(20):
            for j in range(2):
                if not (j == 0 and i == 19)and not (j == 1 and i == 0):
                    self.floorButton[i][j].clicked.connect(self.call_ele)

    # 开门函数

    def open_door(self):
        button = self.sender()
        for i in range(5):
            if button == self.controller.elevatorController[i].openButton:
                self.controller.elevatorController[i].open_request = 1
                break

    # 电梯内部按钮操控函数
    def operate_ele(self):
        button = self.sender()
        for i in range(5):
            for j in range(20):
                if button == self.controller.elevatorController[i].roombutton[j]:
                    self.controller.catch_room_quest(i+1, j+1)
                    break

    # 每层楼的召唤电梯函数
    def call_ele(self):
        button = self.sender()
        for i in range(20):
            for j in range(2):
                if button == self.floorButton[i][j]:
                    if j == 1:
                        dir = -1
                    elif j == 0:
                        dir = 1
                    self.controller.dispatch(i+1, dir)
                    break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywin = myWindow()
    mywin.show()

    sys.exit(app.exec_())
