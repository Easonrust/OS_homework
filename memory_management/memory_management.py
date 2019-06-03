from Ui_memory_management import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow,QLCDNumber
from PyQt5 import QtCore
import sys
import random
import time
from threading import Thread

class myWindow(QMainWindow, Ui_Form):
    
    def __init__(self,parent=None):
        super(myWindow,self).__init__(parent)
        self.setupUi(self)

        #每个块中存在的页面
        self.Block=[]

        #每个块中的当前页面在内存中存在的时间
        self.Time=[]

        #每个块中的当前页面未被使用的时间
        self.Not_Use_Time=[]

        #存储当前生成的320条指令序列
        self.instructions=[]
        
        #320条指令所对应的页面
        self.pages=[]
        
        #当前程序运行到的步数
        self.step=0

        #当前错页次数
        self.f_pages=0

        #当前总共已经运行的指令条数
        self.sum_instructions = QLCDNumber(self)
        self.sum_instructions.setGeometry(QtCore.QRect(550, 340, 82, 42))
        self.sum_instructions.display(self.step)

        #随机开始按钮
        self.startButton.clicked.connect(self.rand_start)

        #单步执行按钮
        self.SingleButton.clicked.connect(self.single_step)

        #执行到底按钮
        self.ToEndButton.clicked.connect(self.to_end)

        #算法的选择
        self.algorithm=0

        #初始化内存块显示器
        for i in range(4):
            self.Block.append(-1)
            self.Block_Page[i].display(int(self.Block[i]))

        #状态刷新显示进程
        self.t1 = Thread(target=self.display_condition,args=())
        self.t1.start()

    #随机开始函数
    def rand_start(self):
        if(self.algo.currentText=="FIFO"):

            #算法为FIFO
            self.algorithm=0
        else:

            #算法为LRU
            self.algorithm=1

        #重置
        self.step=1
        self.f_pages=0
        self.sum_instructions.display(self.step)
        self.Block.clear()
        self.Time.clear()
        self.Not_Use_Time.clear()
        self.pages.clear()
        self.instructions.clear()
        m=random.randint(0,319)

        #初始化显示器
        #刚开始块内均未装页，每个块内当前页面存在时间均为0,每个块内当前页面被使用的次数均为0
        for i in range(4):
            self.Block.append(-1)
            self.Block_Page[i].display(int(self.Block[i]))

            self.Time.append(0)

            self.Not_Use_Time.append(-1)

        

        
        #随机生成320条指令
        self.instructions.append(m)
        self.pages.append(int(m/10))
        self.instructions.append(m+1)
        self.pages.append(int((m+1)/10))

        while True:
            m1=random.randint(0,m-1)
            self.instructions.append(m1)
            self.pages.append(int(m1/10))
            self.instructions.append(m1+1)
            self.pages.append(int((m1+1)/10))
            if len(self.instructions)==320:
                break

            
            m2=random.randint(m1+2,318)
            self.instructions.append(m2)
            self.pages.append(int(m2/10))
            self.instructions.append(m2+1)
            self.pages.append(int((m2+1)/10))
            m=m2
            if len(self.instructions)==320:
                break


        #刚开始内存未装入页面，所以随机生成指令序列后，存在缺页
        self.f_pages+=1

        #将第一条指令装入,该页面存在时间为1,该页面使用次数为1
        self.Block[0]=self.pages[self.step-1]
        self.Time[0]=1
        self.Not_Use_Time[0]=0
                
            
       
    #刷新页面状态的函数    
    def display_condition(self):
        while True:
            if self.step>=1:
                self.sum_instructions.display(self.step)
                self.current_instruction.display(int(self.instructions[self.step-1]))
                self.current_page.display(int(self.pages[self.step-1]))
                self.fault_times.display(int(self.f_pages))
                self.fault_rate.display(self.f_pages/self.step*100)
                for i in range(4):
                    self.Block_Page[i].display(int(self.Block[i]))

    #单步执行函数
    def single_step(self):
    
        #单步执行到该指令
        self.step+=1

        #查看是否有相同的页
        has_same_page=-1
        for i in range(4):
            if self.Block[i]==self.pages[self.step-1]:
                has_same_page=i
                break

        #如果存在相同的页
        if has_same_page != -1:
      

            
            #如果当前块内存在页面，则页面存在时间加1
            for i in range(4):
                if self.Block[i]!=-1:
                    self.Time[i]+=1
                
            #该页面没有使用时间设为0，其他页面加1
            self.Not_Use_Time[has_same_page]=0
            for i in range(4):
                if i != has_same_page and self.Block[i]!=-1:
                    self.Not_Use_Time[i]+=1

            return

        
        #如果不存在相同的页
        else:
            #错页次数加一
            self.f_pages+=1

            #查看是否有空闲页
            has_free_page=-1
            for i in range(4):
                if(self.Block[i]==-1):
                    has_free_page=i
                    break

            #如果存在空闲页
            if has_free_page != -1:
                self.Block[has_free_page]=self.pages[self.step-1]

                #页面存在时间变为1
                self.Time[has_free_page]=1

                #其他页面时间加1
                for i in range(4):
                    if i!=has_free_page:
                        self.Time[i]+=1

                #该页面没有使用时间设为0
                self.Not_Use_Time[has_free_page]=0

                #其他非空页面加1
                for i in range(4):
                    if i != has_free_page and self.Block[i]!=-1:
                        self.Not_Use_Time[i]+=1
                
                return

            #如果不存在空闲页，采取页置换算法
            else:
                
                if self.algorithm==0:
                    #寻找存在时间最长的页面
                    max_time=max(self.Time)
                    max_index=self.Time.index(max_time)

                    #页面存在时间变为1
                    self.Time[max_index]=1

                    #其他页面存在时间加1
                    for i in range(4):
                        if i!=max_index:
                            self.Time[i]+=1
                    self.Block[max_index]=self.pages[self.step-1]
                    return
                elif self.algorithm==1:
                    #寻找未使用时间最长的页面
                    max_not_use_time=max(self.Not_Use_Time)
                    max_index=self.Not_Use_Time.index(max_not_use_time)

                    #该页面没有使用时间设为0，其他页面加1
                    self.Not_Use_Time[max_index]=0
                    for i in range(4):
                        if i != max_index:
                            self.Not_Use_Time[i]+=1 
                    self.Block[max_index]=self.pages[self.step-1]
                    return


    def run_to_end(self):
        while self.step <= 319:
            self.single_step()
            QApplication.processEvents()
            time.sleep(0.1)

    def to_end(self):
        t0 = Thread(target=self.run_to_end,args=())
        t0.start()
                
                






if __name__=="__main__":

    app=QApplication(sys.argv)
    mywin=myWindow()
    mywin.show()
    


    sys.exit(app.exec_())