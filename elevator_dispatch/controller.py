from PyQt5 import QtCore, QtGui, QtWidgets
import time

# 电梯控制器类包括单个电梯的房间、按钮、状态显示、以及控制单个电梯的函数


class ElevatorController(object):
    def __init__(self, Form, elevator_id):
        # 对窗口进行引用
        self.form = Form

        # 电梯的房间
        self.room = QtWidgets.QSlider(Form)
        self.room.setGeometry(QtCore.QRect(460+320*elevator_id, 20, 60, 720))
        self.room.setStyleSheet("background-color:rgb(255, 255, 127)")
        self.room.setMinimum(1)
        self.room.setMaximum(20)
        self.room.setSliderPosition(1)
        self.room.setStyleSheet

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
    def set_room_request(self, f):
        self.room_request[int(f-1)] = 1
    # 楼层请求有效时将相应位置置为1

    def set_floor_request(self, f, direction):
        if direction == 1:
            self.floor_request[int(f-1)] = 1
        elif direction == -1:
            self.floor_request[int(f-1)] = -1

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
            i_direction = (floor - self.current_floor) / \
                abs(floor - self.current_floor)
        else:
            # 电梯已在请求位置
            self.set_room_request(floor)
            return False

        if i_direction*self.direction < 0:
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

            # 电梯移动速度控制
            time.sleep(0.5)


# 总控制器类，负责调度5部电梯
class Controller(object):
    def __init__(self, Form):

        # 将5个电梯控制器加入到总控中
        self.elevatorController = []
        for i in range(5):
            self.elevatorController.append(ElevatorController(Form, i))
    # 捕捉房间请求的函数

    def catch_room_quest(self, ele_num, floor):
        for i in range(5):
            if ele_num == i+1:
                # 如果为第i+1个电梯发出请求，i从0开始

                # 检查请求是否有效（请求方向与运行方向相同）
                if self.elevatorController[i].check_room_request(floor):

                    # 有效时更新请求列表
                    self.elevatorController[i].set_room_request(floor)
                    # 更新目的地
                    self.elevatorController[i].update_destination(floor)
                break
    # 调度函数

    def dispatch(self, floor, direction):
        # 首先找最近电梯
        if not self.find_nearest(floor, direction):

                # 其次找空闲电梯
            if not self.find_vacant(floor, direction):

                # 二者都没有的情况下执行轮转
                self.find_rotate(floor, direction)

    # 寻找最近电梯的函数
    def find_nearest(self, floor, direction):
        distance = [0 for _ in range(5)]
        # Calculate the distance between each elevator and destination,100 means
        # the elevator is not running closer to destination
        for i in range(5):

            # 如果该电梯当前行驶会路过该楼层
            if min(self.elevatorController[i].current_floor, self.elevatorController[i].destination) < floor \
                    < max(self.elevatorController[i].current_floor, self.elevatorController[i].destination) and \
                    self.elevatorController[i].direction == direction:

                # 设置该楼层与该电梯之间距离楼层数
                distance[i] = abs(
                    self.elevatorController[i].current_floor - floor)

            # 否则距离楼层数为一大值
            else:
                distance[i] = 100

        # 寻找5部电梯距离楼层最小值
        min_distance = min(distance)

        # 5部电梯运行途中不会经过该层
        if min_distance == 100:
            return False

        # 存在运行时经过该层的电梯
        else:
            min_index = distance.index(min_distance) + 1
            for i in range(5):
                if min_index == i:

                    # 找到最小距离的运行电梯，更新其楼层请求
                    self.elevatorController[i].set_floor_request(
                        floor, direction)
                    break

            return True  # 找到合适电梯

    # 寻找空闲电梯
    def find_vacant(self, floor, direction):
        # Based on numerical order,find the first vacant elevator
        distance = [0 for _ in range(5)]
        for i in range(5):

            # 判断当前电梯是否空闲
            if self.elevatorController[i].direction == 0:
                distance[i] = abs(
                    self.elevatorController[i].current_floor - floor)
            else:
                distance[i] = 100
         # 寻找5部电梯距离楼层最小值
        min_distance = min(distance)

        if min_distance == 100:
            return False
        else:
            min_index = distance.index(min_distance)
            for i in range(5):
                if min_index == i:

                    # 找到最小距离的空闲电梯，更新其楼层请求
                    self.elevatorController[i].set_floor_request(
                        floor, direction)
                    self.elevatorController[i].destination = floor
                    break

            return True  # 找到合适电梯

    # 如果不存在合适的运行电梯且无空闲电梯，设置该请求进入轮转
    def find_rotate(self, floor, direction):
        for i in range(5):
            if self.elevatorController[i].Rotate_Exist == 0:
                self.elevatorController[i].Rotate_Exist = 1
                self.elevatorController[i].Rotate_Destination = floor
                self.elevatorController[i].floor_request[int(
                    floor - 1)] = direction
