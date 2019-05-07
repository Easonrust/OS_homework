from elevator_controller import ElevatorController


# 总控制器类，负责调度5部电梯
class Controller(object):
    def __init__(self, Form):

        # 将5个电梯控制器加入到总控中
        self.elevatorController = []
        for i in range(5):
            self.elevatorController.append(ElevatorController(Form, i))

    # 调度函数

    def dispatch(self, floor, direction):
        # 首先找最近电梯
        if not self.find_nearest_running(floor, direction):

                # 其次找空闲电梯
            if not self.find_nearest_vacant(floor, direction):

                # 二者都没有的情况下执行轮转
                self.check_rotate(floor, direction)

    # 寻找最近电梯的函数
    def find_nearest_running(self, floor, direction):
        floor_distance = [0 for i in range(5)]
        # Calculate the distance between each elevator and destination,100 means
        # the elevator is not running closer to destination
        for i in range(5):

            # 如果该电梯当前行驶会路过该楼层
            if (min(self.elevatorController[i].current_floor, self.elevatorController[i].destination) < floor) and (floor < max(self.elevatorController[i].current_floor, self.elevatorController[i].destination)) and (self.elevatorController[i].direction == direction):

                # 设置该楼层与该电梯之间距离楼层数
                floor_distance[i] = abs(
                    self.elevatorController[i].current_floor - floor)

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
                    self.elevatorController[i].set_floor_request(
                        floor, direction)
                    break

            return True  # 找到合适电梯

    # 寻找空闲电梯
    def find_nearest_vacant(self, floor, direction):
        # Based on numerical order,find the first vacant elevator
        floor_distance = [0 for i in range(5)]
        for i in range(5):

            # 判断当前电梯是否空闲
            if self.elevatorController[i].direction == 0:
                floor_distance[i] = abs(
                    self.elevatorController[i].current_floor - floor)
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
                    self.elevatorController[i].set_floor_request(
                        floor, direction)
                    self.elevatorController[i].destination = floor
                    break

            return True  # 找到合适电梯

    # 如果不存在合适的运行电梯且无空闲电梯，设置该请求进入轮转
    def check_rotate(self, floor, direction):
        for i in range(5):
            if self.elevatorController[i].Rotate_Exist == 0:
                self.elevatorController[i].Rotate_Exist = 1
                self.elevatorController[i].Rotate_Destination = floor
                self.elevatorController[i].floor_request[int(
                    floor - 1)] = direction
                break
