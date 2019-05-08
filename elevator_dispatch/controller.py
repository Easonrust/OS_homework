from elevator import Elevator


# 总控制器类，负责调度5部电梯
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
