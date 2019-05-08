from PyQt5 import QtCore, QtGui, QtWidgets
import time

# 电梯控制器类包括单个电梯的房间、按钮、状态显示、以及控制单个电梯的函数


class Elevator(object):
    def __init__(self, Form, elevator_id):
        # 对窗口进行引用
        self.form = Form

        # 电梯的房间
        '''self.room = QtWidgets.QSlider(Form)
        self.room.setGeometry(QtCore.QRect(460+320*elevator_id, 20, 60, 720))
        self.room.setStyleSheet("background-color:rgb(255, 255, 127)")
        self.room.setMinimum(1)
        self.room.setMaximum(20)
        self.room.setSliderPosition(1)
        self.room.setStyleSheet'''

        self.room = QtWidgets.QLabel(Form)
        self.room.setGeometry(QtCore.QRect(443+320*elevator_id, 720, 62, 33))
        self.room.setPixmap(QtGui.QPixmap("icon/电梯.png"))
        self.room.setScaledContents(True)
        self.l_wall = QtWidgets.QFrame(Form)
        self.l_wall.setGeometry(QtCore.QRect(430+320*elevator_id, 20, 40, 720))
        self.l_wall.setFrameShape(QtWidgets.QFrame.VLine)
        self.l_wall.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.r_wall = QtWidgets.QFrame(Form)
        self.r_wall.setGeometry(QtCore.QRect(480+320*elevator_id, 20, 40, 720))
        self.r_wall.setFrameShape(QtWidgets.QFrame.VLine)
        self.r_wall.setFrameShadow(QtWidgets.QFrame.Sunken)

        # 按钮表
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(
            QtCore.QRect(240+320*elevator_id, 180, 202, 562))
        self.buttonLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        # 按钮
        self.roombutton = []
        for i in range(10):
            self.roombutton.append(
                QtWidgets.QPushButton(self.gridLayoutWidget))
            self.roombutton[i].setText(str(i+1))
            self.buttonLayout.addWidget(self.roombutton[i], 9-i, 0, 1, 1)
            self.roombutton[i].setCheckable(True)
            self.roombutton[i].setStyleSheet("QPushButton:checked{color:red}")
        for i in range(10):
            self.roombutton.append(
                QtWidgets.QPushButton(self.gridLayoutWidget))
            self.roombutton[i+10].setText(str(i+11))
            self.buttonLayout.addWidget(self.roombutton[i+10], 9-i, 1, 1, 1)
            self.roombutton[i+10].setCheckable(True)
            self.roombutton[i +
                            10].setStyleSheet("QPushButton:checked{color:red}")

        # 关门按钮
        self.closeButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(5)
        self.closeButton.setFont(font)
        self.closeButton.setText("><")
        self.buttonLayout.addWidget(self.closeButton, 10, 1, 1, 1)

        # 开门按钮
        self.openButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.openButton.setFont(font)
        self.openButton.setText("<>")
        self.buttonLayout.addWidget(self.openButton, 10, 0, 1, 1)

        # 报警按钮
        self.warn_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.buttonLayout.addWidget(self.warn_button, 11, 0, 1, 2)
        self.warn_button.setText("warn")

        # 电梯所在楼层以及行驶状态显示
        self.floorNum = QtWidgets.QLCDNumber(Form)
        self.floorNum.setGeometry(QtCore.QRect(
            240+320*elevator_id, 20, 102, 142))
        self.floorNum.setDigitCount(2)
        self.floorNum.setProperty("intValue", 1)
        self.inCondition = QtWidgets.QLabel(Form)
        self.inCondition.setGeometry(
            QtCore.QRect(340+320*elevator_id, 40, 102, 102))
        self.inCondition.setText("")
        self.inCondition.setPixmap(QtGui.QPixmap("icon/上.png"))
        self.inCondition.setScaledContents(True)

        # 电梯房间发出的请求 0有 1无
        self.room_request = [0 for i in range(20)]

        # 楼层发出的请求  0有 1无
        self.floor_request = [0 for i in range(20)]

        # 开门请求 0有 1无
        self.open_request = 0

        # 电梯运行方向 0空闲 1向上 -1向下
        self.direction = 0

        # 电梯目的地以及初始楼层
        self.current_floor = 1
        self.destination = 1

        # 轮转调度
        self.Rotate_Exist = 0  # 0不存在轮转 1存在轮转
        self.Rotate_Destination = 0  # 轮转楼层

    # 房间请求有效时将相应位置置为1
    def set_room_request(self, floor):
        self.room_request[int(floor-1)] = 1
    # 楼层请求有效时将相应位置置为1

    def set_floor_request(self, floor, direction):
        if direction == 1:
            self.floor_request[int(floor-1)] = 1
        elif direction == -1:
            self.floor_request[int(floor-1)] = -1

    # 更新电梯方向
    def update_direction(self):
        if self.destination == self.current_floor:
            self.direction = 0
            self.inCondition.setVisible(False)
        else:
            self.direction = (self.destination - self.current_floor) / \
                abs(self.destination - self.current_floor)
            self.inCondition.setVisible(True)
            if self.direction == 1:
                self.inCondition.setPixmap(
                    QtGui.QPixmap("icon/上.png"))  # 电梯向上运行
            else:
                self.inCondition.setPixmap(
                    QtGui.QPixmap("icon/下.png"))  # 电梯向下运行

    # 更新电梯最终目的地
    def update_destination(self, floor):
        if abs(floor - self.current_floor) > abs(self.destination - self.current_floor):
            self.destination = floor

    # 检查电梯房间请求是否有效
    def check_room_request(self, floor):

        if floor != self.current_floor:
            Direction = (floor - self.current_floor) / \
                abs(floor - self.current_floor)
        else:
            # 电梯已在请求位置
            self.set_room_request(floor)
            return False

        if Direction*self.direction < 0:
            # 请求方向与运行方向矛盾
            return False
        else:
            # 满足请求
            return True

    def check_open(self):
        if self.open_request == 1:

            # 检测到开门请求 显示屏显示开门动画2s
            self.inCondition.setPixmap(QtGui.QPixmap("icon/电梯开门.png"))
            self.inCondition.setVisible(True)
            time.sleep(2)
            self.open_request = 0
            self.inCondition.setVisible(False)

        if self.room_request[int(self.current_floor - 1)] == 1:

            # 检测到该层有电梯房间请求 还原房间按钮
            self.roombutton[int(self.current_floor-1)].setChecked(False)

            # 显示屏显示开门动画2s
            self.inCondition.setPixmap(QtGui.QPixmap("icon/电梯开门.png"))
            time.sleep(2)

            # 请求响应完毕 还原电梯房间请求状态为0
            self.room_request[int(self.current_floor - 1)] = 0

        if abs(self.floor_request[int(self.current_floor - 1)]) == 1:

            # 检测到该层有楼层请求 还原按钮
            self.form.floorButton[int(
                self.current_floor-1)][0].setChecked(False)
            self.form.floorButton[int(
                self.current_floor-1)][1].setChecked(False)

            # 显示屏显示开门动画2s
            self.inCondition.setPixmap(QtGui.QPixmap("icon/电梯开门.png"))
            time.sleep(2)  # 可加开门动画

            # 请求响应完毕 还原电梯房间请求状态为0
            self.floor_request[int(self.current_floor - 1)] = 0  # 更新内部按键请求状态为0

    def operate_ele(self):
        button = self.form.sender()
        for i in range(20):
            if button == self.roombutton[i]:
                # 检查请求是否有效（请求方向与运行方向相同）
                if self.check_room_request(i+1):

                    # 有效时更新请求列表
                    self.set_room_request(i+1)
                    # 更新目的地
                    self.update_destination(i+1)
                break
    
    # 开门函数

    def open_door(self):
        button = self.form.sender()
        if button == self.openButton:
            self.open_request = 1

    # 电梯循环运转函数
    def run(self):
        while True:

             # 检查是否存在请求
            self.check_open()
            # 不断更新电梯运行状态
            self.update_direction()

            if self.direction != 0:
                # 电梯在运行中
                self.current_floor += self.direction
                # self.check_open()

            elif not self.Rotate_Exist == 0:

                # 电梯空闲且存在轮转时，执行轮转调度
                self.destination = self.Rotate_Destination

                # 还原轮转标志
                self.Rotate_Exist = 0
            
             # 电梯所在楼层数显示
            self.floorNum.display(int(self.current_floor))

            # UI电梯更改位置
            x=int(self.room.x())
            y=int(self.form.floor[int(self.current_floor-1)].y())+17
            self.room.move(x,y)
            
            QtWidgets.QApplication.processEvents()
            # 电梯移动速度控制
            time.sleep(0.4)
