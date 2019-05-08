# 处理机管理-电梯调度

## 项目简介

### 基本任务

某一层楼20层，有5部互联的电梯。基于线程思想，编写一个电梯调度程序。

### 功能描述

每个电梯里面设置必要功能键：如数字键、关门键、开门键、上行键、报警键、当前电梯的楼层数、上升及下降状态等。

每层楼的每部电梯门口，应该有上行和下行按钮和当前电梯状态的数码显示器。

### 项目需求

五部电梯门口的按钮是互联结的，即当一个电梯按钮按下去时，其他电梯的相应按钮也就同时点亮，表示也按下去了。

所有电梯初始状态都在第一层。每个电梯如果在它的上层或者下层没有相应请求情况下，则应该在原地保持不动。

## 设计方案

### 界面设计

界面左侧为每一层的楼梯按钮表，由于要求五部电梯门口的按钮互相联结，所以采取每层为上，下两个按钮，楼梯按钮表右侧为20层楼层标识；

界面右侧为5部电梯，每部电梯包含一套按钮表，其中数字1-20的按钮代表楼层按钮，开关按钮按下后，电梯可在所停楼层开门2秒钟；按钮表上方配备有状态显示栏，用来显示电梯的楼层和运行状态（开门，向上运行，向下运行）；按钮表右侧为电梯房间的图形显示。

![界面](C:\Users\yangl\Desktop\界面.png)

## 调度算法设计

程序中的按钮设计除去电梯房间内部按键主动开门的事件共分为两种，分别为楼层按钮事件和电梯房间按钮事件，两种事件均对电梯发出请求，分为楼层请求`floor_request`和房间请求`room_request`。本项目采取了轮转调度的算法思想，轮转调度是较为简单的一类调度算法。

### 楼层按钮事件

用户按下左侧按钮栏某一楼层上或下按钮后，电梯总控制器自动在5部电梯中寻找最合适的电梯，最合适的电梯响应请求后运行到该楼层，电梯总控制器的寻找顺序如下：

1. 从正在运行的电梯中进行寻找，找出运行会经过该楼层且离该楼层最近的电梯。若有此类电梯，向其发送请求；否则，进入下一步。
2. 从空闲状态的电梯中进行寻找，找出离该楼层最近的电梯。若有此类电梯，向其发送请求；否则，进入下一步。
3. 此时，所有电梯均为运行状态且不会经过该楼层，因此采用轮转算法，将该楼层记录到轮转目的地中，等到某一电梯空闲时，响应该轮转目的地的请求。

### 电梯房间按钮事件

用户在按下某一电梯的楼层按钮后分为以下两种情况进行考虑：

1. 该楼层符合电梯的运动方向：

   a. 该楼层比电梯目的地楼层要远，接受该楼层的请求，并将电梯目的地更新为该楼层。

   b. 该楼层比电梯目的地楼层要近，接受该楼层请求。

2. 该楼层不符合电梯运动方向：

   将该楼层记录到轮转目的地中，等到电梯空闲时响应该轮转目的地的请求。

3. 该楼层为电梯当前楼层：

   电梯房间发出开门请求。

### 程序结构设计

共包含4个文件：**elevator.py**, **controller.py**, **Ui_elevator.py**, **controller.py**。

#### elevator.py

包含`Elevator`类，封装了一部电梯的按钮，状态显示栏，电梯房间图形；具有电梯运行状态`direction`，目的地`destination`，接受到的楼层请求`floor_request`,接受到的房间按钮请求`room_request`,接受到的开门请求`open_request`,轮转属性等。其成员变量代码如下：

```python
class Elevator(object):
    def __init__(self, Form, elevator_id):
        # 对窗口进行引用
        self.form = Form

        # 电梯的房间
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

        # 电梯房间发出的请求 0无 1有
        self.room_request = [0 for i in range(20)]

        # 楼层发出的请求  0无 1上 -1 下
        self.floor_request = [0 for i in range(20)]

        # 开门请求 0无 1有
        self.open_request = 0

        # 电梯运行方向 0空闲 1向上 -1向下
        self.direction = 0

        # 电梯目的地以及初始楼层
        self.current_floor = 1
        self.destination = 1

        # 轮转调度
        self.Rotate_Exist = 0  # 0不存在轮转 1存在轮转
        self.Rotate_Destination = 0  # 轮转楼层
```

`Elevator`类的核心成员函数为`run(self)`，该函数每隔0.4秒更新一次电梯的状态，并控制电梯房间图形配合电梯状态的改变发生变化，代码如下：

```python
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
```

`Elevator`类的另一关键函数为`operate_ele`，该函数通过和电梯按钮相连接，以响应用户按键动作，代码如下：

``` python
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
```

#### controller.py

包含`Controller`类，为5部电梯的总控制器。包含成员函数`call_ele(self)`用于连接楼层按键并处理请求;成员函数`find_nearest_running(self,floor,direction)`在运行中电梯中寻找最合适电梯;成员函数`find_nearest_vacant(self,floor,direction)`在空闲电梯中寻找最近电梯；成员函数`set_rotate(self,floor,direction)`用于设置轮转目的地；成员函数`dispatch(self,floor,direction)`负责响应楼层请求后对5部电梯进行调度。

其核心代码如下：

```python
class Controller(object):
    def __init__(self, Form):
        self.form=Form
        # 将5个电梯加入到控制器中
        self.elevator = []
        for i in range(5):
            self.elevator.append(Elevator(self.form, i))

    # 每层楼的召唤电梯函数
    def call_ele(self):
        button = self.form.sender()
        for i in range(20):
            for j in range(2):
                if button == self.form.floorButton[i][j]:
                    if j == 1:
                        dir = -1
                    elif j == 0:
                        dir = 1
                    self.dispatch(i+1, dir)
                    break

    # 调度函数

    def dispatch(self, floor, direction):
        # 首先找最近电梯
        if not self.find_nearest_running(floor, direction):

                # 其次找空闲电梯
            if not self.find_nearest_vacant(floor, direction):

                # 二者都没有的情况下执行轮转
                self.set_rotate(floor, direction)

    # 寻找最近电梯的函数
    def find_nearest_running(self, floor, direction):
        floor_distance = [0 for i in range(5)]
        # Calculate the distance between each elevator and destination,100 means
        # the elevator is not running closer to destination
        for i in range(5):

            # 如果该电梯当前行驶会路过该楼层
            if (min(self.elevator[i].current_floor, self.elevator[i].destination) < floor) and (floor < max(self.elevator[i].current_floor, self.elevator[i].destination)) and (self.elevator[i].direction == direction):

                # 设置该楼层与该电梯之间距离楼层数
                floor_distance[i] = abs(
                    self.elevator[i].current_floor - floor)

            # 否则距离楼层数为一大值
            else:
                floor_distance[i] = 13

        # 寻找5部电梯距离楼层最小值
        min_floor_distance = min(floor_distance)

        # 5部电梯运行途中不会经过该层
        if min_floor_distance == 13:
            return False

        # 存在运行时经过该层的电梯
        else:
            min_index = floor_distance.index(min_floor_distance) + 1
            for i in range(5):
                if min_index == i:

                    # 找到最小距离的运行电梯，更新其楼层请求
                    self.elevator[i].set_floor_request(
                        floor, direction)
                    break

            return True  # 找到合适电梯

    # 寻找空闲电梯
    def find_nearest_vacant(self, floor, direction):
        # Based on numerical order,find the first vacant elevator
        floor_distance = [0 for i in range(5)]
        for i in range(5):

            # 判断当前电梯是否空闲
            if self.elevator[i].direction == 0:
                floor_distance[i] = abs(
                    self.elevator[i].current_floor - floor)
            else:
                floor_distance[i] = 13
         # 寻找5部电梯距离楼层最小值
        min_floor_distance = min(floor_distance)

        if min_floor_distance == 13:
            return False
        else:
            min_index = floor_distance.index(min_floor_distance)
            for i in range(5):
                if min_index == i:

                    # 找到最小距离的空闲电梯，更新其楼层请求
                    self.elevator[i].set_floor_request(
                        floor, direction)
                    self.elevator[i].destination = floor
                    break

            return True  # 找到合适电梯

    # 如果不存在合适的运行电梯且无空闲电梯，设置该请求进入轮转
    def set_rotate(self, floor, direction):
        for i in range(5):
            if self.elevator[i].Rotate_Exist == 0:
                self.elevator[i].Rotate_Exist = 1
                self.elevator[i].Rotate_Destination = floor
                self.elevator[i].floor_request[int(floor - 1)] = direction
                break
```

#### Ui_elevator.py

用于绘制电梯系统界面，采用*qtdesigner*和循环算法相配合的方式。

#### elevator_system.py

用于设置界面上所有按钮与函数的连接。





