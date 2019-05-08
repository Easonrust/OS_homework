
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
from controller import Controller
import time

# 用于显示整个电梯系统


class Ui_Form(object):
    def setupUi(self, Form):
        Form.resize(1800, 758)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        Form.setFont(font)

        # 楼层数
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 20, 222, 720))
        self.gridLayout = QtWidgets.QGridLayout(self.verticalLayoutWidget_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.floor = []
        for i in range(20):
            self.floor.append(QtWidgets.QLabel(self.verticalLayoutWidget_2))
            self.floor[i].setStyleSheet("border-width:1px;border-style:solid")
            self.floor[i].setText(str(i+1))
            self.gridLayout.addWidget(self.floor[i], 21-i, 2, 1, 1)

        # 添加每层的开关
        self.floorButton = [[] for i in range(20)]
        for i in range(20):
            for j in range(2):
                self.floorButton[i].append(
                    QtWidgets.QPushButton(self.verticalLayoutWidget_2))
                self.gridLayout.addWidget(
                    self.floorButton[i][j], 21-i, j, 1, 1)
                if j == 0:
                    self.floorButton[i][j].setText(("↑"))
                    if not i == 19:
                        self.floorButton[i][j].setCheckable(True)
                        self.floorButton[i][j].setStyleSheet(
                            "QPushButton:checked{color:yellow}")
                else:
                    self.floorButton[i][j].setText(("↓"))
                    if not i == 0:
                        self.floorButton[i][j].setCheckable(True)
                        self.floorButton[i][j].setStyleSheet(
                            "QPushButton:checked{color:yellow}")

         # 电梯总控制器
        self.controller = Controller(Form)
        elevatorThread = []
        for i in range(5):
            elevatorThread.append(Thread(target=self.controller.elevator[i].run, args=()))
            elevatorThread[i].start()

        QtCore.QMetaObject.connectSlotsByName(Form)

  
