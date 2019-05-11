from Ui_elevator import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class myWindow(QMainWindow, Ui_Form):

    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)
        self.setupUi(self)

        # 五部电梯房间按钮连接自己的电梯操纵函数函数
        for i in range(5):
            for j in range(20):
                self.dispatcher.elevator[i].roombutton[j].clicked.connect(
                    self.dispatcher.elevator[i].operate_ele)

        # 五部电梯开门按钮连接函数
        for i in range(5):
            self.dispatcher.elevator[i].openButton.clicked.connect(
                self.dispatcher.elevator[i].open_door)

        # 每层楼召唤电梯按钮连接函数
        for i in range(20):
            for j in range(2):
                if not (j == 0 and i == 19)and not (j == 1 and i == 0):
                    self.floorButton[i][j].clicked.connect(self.dispatcher.call_ele)

 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywin = myWindow()
    mywin.show()

    sys.exit(app.exec_())
