# 请求调页存储管理方式的模拟

## 1.项目目的

1. 加深对页面、页表、地址转换概念的理解和掌握。
2. 加深对页面置换过程的理解和掌握。
3. 加深对请求调页系统的原理和实现过程的理解。

## 2. 项目需求

### 2.1 内容

假设每个页面可存放10条指令，分配给一个作业的内存块为4,。模拟一个作业的执行过程，该作业有320条指令，即它的地址空间为32页，目前所有页还没有调入内存。

### 2.2 模拟过程

1. 在模拟过程中，如果所访问指令在内存中，则显示其物理地址，并转到下一条指令；如果没有在内存中，则发生缺页，此时需要记录缺页次数，并将其调入内存。如果4个内存块中已装入作业，则需进行页面置换。
2. 所有320条指令执行完成后，计算并显示作业执行过程中发生的缺页率。
3. 置换算法可以选用**FIFO**或者**LRU**算法。

### 2.3 指令的访问次序及形成方法

#### 2.3.1 指令的访问次序

50%的指令是顺序执行的，25%是均匀分布在前地址部分，25%是均匀分布在后地址部分。

#### 2.3.2 形成方法

1. 在0-319条指令之间，随机选取一个起始执行指令，如序号为m。
2. 顺序执行下一条指令，即序号为m+1的指令。
3. 通过随机数，跳转到前地址部分0-m-1中的某个指令处，其序号为m1。
4. 顺序执行下一条指令，即序号为m1+1的指令。

## 3. 算法设计

### 3.1 模拟指令随机生成过程

按照项目需求中的方法进行生成，生成函数`rand_start()`函数与**startButton**连接，其核心代码如下：

```python
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
```

### 3.2 页面置换

模拟程序可选择**FIFO**与**LRU**两种调度算法进行页面调度

#### 3.2.1 FIFO算法

**FIFO**算法即先进算法，即当发生页面置换的时候，最先进入的页最先调出，为了实现该算法，我设置了一个大小为4的`Time[]`用于存储每个内存块内当前页面存在的时间，每次指令重新模拟生成时将该列表还原，进行页面调度时对该列表进行相应操作。

#### 3.2.2 LRU算法

**LRU**算法即最近最久未使用算法，即当发生页面置换的时候，将最长时间没有使用的页调出，为了实现该算法，我设置了一个大小为4的`Not_Use_Time[]`列表用来存储每个内存块内当前页面未被使用的时间，每次指令重新模拟生成时将该列表还原，进行页面调度时对该列表进行相应操作。

#### 3.2.3 请求调页流程

1. 随机选择一条指令。
2. 若该指令所在页面在内存块中，则所有内存块中页面的存在时间`Time[i]`加1；将该指令所在页面的未使用时间`Not_Use_Time[i]`设为0，其他页面加1。
3. 若该指令所在页面不在内存块中，则错页次数加1。
   1. 若存在空闲页，将该指令页面加入编号最小的内存块中。将该页面存在时间`Time[i]`变为1，其他页面存在时间`Time[i]`加1；该页面没有使用时间`Not_Use_Time[i]`设为0，其他页面加1.
   2. 若不存在空闲页，则采取页置换算法
      1. **FIFO**算法：选择页面存在时间最长的页面进行页面置换，同时将其页面存在时间`Time[i]`设为1，其他页面的页面存在时间`Time[i]`加1。
      2. **LRU**算法：选择未使用时间最长的页面进行页面置换，同时将其未使用时间`Not_Use_Time[i]`设为0，其他页面的为使用时间`Not_Use_Time[i]`加1。

#### 3.2.4 算法流程图

![未命名文件 (1)](C:\Users\yangl\Desktop\未命名文件 (1).png)

## 4. 核心代码

### 4.1 单步调度函数

```python
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
```

### 4.2 状态刷新函数

```python
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
```

## 5. 程序测试
### 5.1 使用说明

![face](C:\Users\yangl\Desktop\face.png)

1. 最上面四个方框显示相应内存块中当前页面的页号。当为-1时代表当前内存块中不存在任何页面。
2. **Current Instructions**下的方框显示当前指令的地址，**Page**下面的方框显示当前指令所在的页面。
3. **Page-replacement algorithm**下的选择框可以选择页置换的算法：**FIFO**或**LRU**。
4. **Rand start Address**按钮按下后，随机生成***第一条指令***的地址，并尝试将其指令页面装入内存。
5. **Single Step**按钮按下后，按指令序列生成原则执行下一条指令，并尝试将其指令页面装入内存（最开始一定要先按下**Rand start Address**按钮）。
6. **Execute to the End**按钮按下后，指令会一直向下进行，直到320条指令调度完毕（最开始一定要先按下**Rand start Address**按钮）。
7. **Page-Fault time**下的方框显示缺页次数，**Page-Fault Rate**下的方框显示缺页率。
8. 右下角的方框显示已经调度的指令条数（包括当前指令）。

### 5.2 首先随机生成第一条指令序列

![1](C:\Users\yangl\Desktop\1.png)

### 5.3 执行下一条指令

![2](C:\Users\yangl\Desktop\2.png)

## 6. 开发环境

Python3.7+Pyqt5