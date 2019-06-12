# 文件系统模拟

## 1. 项目目的

1. 熟悉文件存储空间的管理。
2. 熟悉文件的物理结构、目录结构和文件操作。
3. 熟悉文件系统管理实现。
4. 加深对文件系统内部功能和实现过程的理解。

## 2. 项目需求

1. 在内存中开辟一个空间作为文件存储器，在其上实现一个简单的文件系统。

2. 退出这个文件系统时，需要该文件系统的内容保存到磁盘上，以便下次可以将其恢复到内存中来。

3. 文件系统提供的操作：

   a. 格式化。

   b. 创建子目录。

   c. 删除子目录。

   d. 显示目录。

   e. 更改当前目录。

   f. 创建文件。

   g. 打开文件。

   h. 关闭文件。

   i.  写文件。

   k. 读文件。

   l.  删除文件。

## 3. 算法设计

### 3.1 文件存储空间管理

磁盘空间的分配方式采用了索引分配的方式，为每一个文件配备了一个索引表；并采用多层索引的方式，有两层索引。

### 3.2 空闲空间管理

磁盘空闲空间的管理方式采用了位图法。

### 3.3 文件控制块

为每个文件配备了唯一的FCB，便于进行管理。

### 3.4 文件目录设计

文件目录采用多级目录结构，文件项目包含文件名、文件类型、物理地址、长度。文件类型仅有文本文件与文件夹两种。

### 3.5 实现文件保存在磁盘上的方法

利用C#的*Serializable*特性，将需要保存的数据序列化后存储在磁盘上，在需要恢复时进行反序列化。代码如下：

```c#
//将根目录的FCB，位图以及目录进行序列化
        public void serialize()
        {
            FileStream fileStream1, fileStream2, fileStream3,fileStream4;
            BinaryFormatter b = new BinaryFormatter();

            fileStream1 = new FileStream(System.IO.Path.Combine(dir, "catalogTree.dat"), FileMode.Create);
            b.Serialize(fileStream1, root_fcb);
            fileStream1.Close();

            fileStream2 = new FileStream(System.IO.Path.Combine(dir, "catalogTable.dat"), FileMode.Create);
            b.Serialize(fileStream2, catalog);
            fileStream2.Close();

            fileStream3 = new FileStream(System.IO.Path.Combine(dir, "bitMap.dat"), FileMode.Create);
            b.Serialize(fileStream3, bitMap);
            fileStream3.Close();

            fileStream4 = new FileStream(System.IO.Path.Combine(dir, "filestore.dat"), FileMode.Create);
            b.Serialize(fileStream4, filestore);
            fileStream4.Close();
        }

        //利用序列化的文件进行反序列化
        public void deserialize()
        {
            FileStream fileStream1, fileStream2, fileStream3,fileStream4;
            BinaryFormatter b = new BinaryFormatter();

            fileStream1 = new FileStream(System.IO.Path.Combine(dir, "catalogTree.dat"), FileMode.Open, FileAccess.Read, FileShare.Read);
            root_fcb = b.Deserialize(fileStream1) as FCB;
            fileStream1.Close();

            fileStream2 = new FileStream(System.IO.Path.Combine(dir, "catalogTable.dat"), FileMode.Open, FileAccess.Read, FileShare.Read);
            catalog = b.Deserialize(fileStream2) as Catalog;
            fileStream2.Close();

            fileStream3 = new FileStream(System.IO.Path.Combine(dir, "bitMap.dat"), FileMode.Open, FileAccess.Read, FileShare.Read);
            bitMap = b.Deserialize(fileStream3) as BitMap;
            fileStream3.Close();

            fileStream4 = new FileStream(System.IO.Path.Combine(dir, "filestore.dat"), FileMode.Open, FileAccess.Read, FileShare.Read);
            filestore = b.Deserialize(fileStream4) as Stack<File>;
            fileStream3.Close();
        }
```



## 4. 界面设计

由于C#的winform程序设计界面非常方便，可以很容易地设计出类似Windows自带的文件管理系统，因此采用C#实现算法，基本界面如下。

### 4.1 主界面

![interface](https://github.com/Easonrust/OS_homework/blob/master/file_system/img/interface.png)

其中最上一栏为菜单栏，模仿windows自带文件系统：

1. 点击**文件**选项后，可选择创建文本文件或文件夹；可打开选中的文本文件或文件夹；可重命名选中的文本文件或文件夹；可删除选中的文本文件或文件夹。
2. 点击**格式化**选项后，系统将删除本文件系统中所有由用户创建的数据。
3. 点击**保存所有**选项后，系统可将当前文件系统中所有数据保存在磁盘中。
4. 点击**访问磁盘上存储的数据选项**，系统会读出之前保存在磁盘中的数据。

接下来一栏为地址栏，显示当前文件目录，按下向上箭头按钮后可返回上一级目录。

下面的两个方框：

1. 第一个方框显示当前文件系统的目录树。
2. 第二个方框显示当前目录下所有的文件，以及它们的文件名、文件类型、文件长度、物理地址。

### 4.2 重命名输入框

![renameface](https://github.com/Easonrust/OS_homework/blob/master/file_system/img/renameface.png)

用户在为选中文件重命名时只需在文本框中输入名称，再点击确定键，最后关闭窗口，即可实现重命名。

### 4.3 文本编辑器

![text](https://github.com/Easonrust/OS_homework/blob/master/file_system/img/text.png)

用户打开选中的文本文件后，会出现简易的文本编辑器，用户在输入框中输入内容后，点击保存键，在关闭窗口，即可写入文本文件。

## 5. 核心代码

BitMap.cs

```c#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace file_system
{
    //使用位图来进行空闲空间管理


    //Serializable序列化可以保证该类型可以存储到文件中
    [Serializable]
    public class BitMap
    {
        //磁盘上块的个数
        public static int Capacity = 100 * 100 * 100;

        //磁盘上的块
        private Block[] blocks = new Block[Capacity];

        //位图
        private bool[] bitMap = new bool[Capacity];

        
        private int bitPointer = 0;

        public BitMap()
        {
            //初始化类图，使每一块均为空闲
            for (int i = 0; i < Capacity; i++)
            {
                bitMap[i] = true;
            }
        }

        //获得每个块中的数据
        public string getBlock(int i)
        {
            return blocks[i].getInfo();
        }

        //Find the first empty block and set data on it
        public int allocateBlock(string data)
        {
            bitPointer = bitPointer % Capacity;
            int tempPointer = bitPointer;
            while (true)
            {
                //该内存块为空闲的话
                if (bitMap[tempPointer])
                {
                   //从磁盘中选择一个新的内存块
                    blocks[tempPointer] = new Block();
                    blocks[tempPointer].setInfo(data);
                    bitPointer = tempPointer + 1;

                    //返回占用的内存块的指针
                    return tempPointer;
                }

                //否则向下寻找空闲的内存块
                else
                    tempPointer = (tempPointer + 1) % Capacity;

               //已经寻找一圈还没找到空闲内存块，说明磁盘已满，此时跳出循环
                if (tempPointer == bitPointer)
                    break;
            }

            //磁盘已满
            return -1;
        }

        //删除一个内存块
        public void withdraw(int index)
        {
            bitMap[index] = true;
        }

        //删除一堆内存块
        public void withdraw(List<int> indexs)
        {
            foreach(int i in indexs)
            {
                bitMap[i] = true;
            }
        }

        //设置一个索引表存储该文件占用的块，并将数据写入到内存中
        public IndexTable write(string data)
        {
            IndexTable table = new IndexTable();

            while (data.Count() > 16)
            {
                table.addIndex(allocateBlock(data.Substring(0, 15)));
                data = data.Remove(0, 15);
            }
            table.addIndex(allocateBlock(data));

            return table;
        }
    }
}

```

Block.cs

```c#
//内存块设计完毕


using System;

namespace file_system
{
    //内存中最基本的存储单元
    [Serializable]
    public class Block
    {
        //该内存块的内容
        private char[] info;

        //该内存块中内容的长度
        private int length;


        //每个内存块最多可存储16个char类型的数据
        public Block()
        {
            info = new char[16];
         }

        //为该内存块分配数据
        public void setInfo(string new_info)
        {
            length = (new_info.Length > 16) ? 16 : new_info.Length;
            for(int i = 0; i < length; i++)
            {
                info[i] = new_info[i];
            }
        }

        //获得当前内存块中存储的内容
        public string getInfo()
        {
            string temp = new string(info);
            return temp;
        }
    }
}

```

Catalog.cs

```c#
//文件管理目录设计完毕


using System;
using System.Collections.Generic;


namespace file_system
{
    // 文件目录：主要利用FCB文件控制块来管理文件

    //利用序列化特性可将该目录存储在磁盘中
    [Serializable]
    public class Catalog
    {
        //文件字典，用于建立文件与内存指针之间的映射关系
        public Dictionary<int, File> file_table = new Dictionary<int, File>();
        public Dictionary<int, FCB> fcb_table = new Dictionary<int, FCB>();

        public void map(FCB item,File file)
        {
            //建立内存指针与file之间的映射关系
            file_table[item.filePointer] = file;

            //建立内存指针与FCB之间的映射关系
            fcb_table[item.filePointer] = item;
        }

        //通过FCB获取文件
        public File getFile(FCB item)
        {
            if (fcb_table.ContainsKey(item.filePointer))
            {
                return file_table[item.filePointer];
            }
            else
                return null;
        }

        //通过文件指针获得文件
        public File getFile(int filePointer)
        {
            if (fcb_table.ContainsKey(filePointer))
            {
                return file_table[filePointer];
            }
            else
                return null;
        }

        //通过文件获得PCB
        public FCB getFCB(File file)
        {
            if (file_table.ContainsKey(file.filePointer))
            {
                return fcb_table[file.filePointer];
            }
            else
                return null;
        }

        //移除该文件
        public void removeFile(FCB item)
        {
            //将磁盘块中该文件的指针删除
            file_table.Remove(item.filePointer);
        }

        //移除PCB
        public void removeFCB(File file)
        {
            fcb_table.Remove(file.filePointer);
        }
    }
}

```

FCB.cs

```c#
//文件控制块设计完成



using System;


namespace file_system
{
     //序列化特性，确保FCB能存储在磁盘中
    [Serializable]
    public class FCB
    {
        //指定文件的两种类型，文件夹和txt
        public enum FileType { folder, txt };

        public string fileName;

        //文件的基本信息
        public string size,path;

        //创建文件的时间，DateTime类型
        public DateTime createTime;


        //每个文件的指针，相当于文件的序号
        public int filePointer;
        public FileType fileType;
        public FCB father = null, son = null, next = null, pre = null;

        //所有的文件数量
        public static int file_counter = 0;

        public FCB()
        {
            this.fileType = FileType.folder;
            this.filePointer = file_counter++;
        }

        public FCB(string fileName,FileType fileType)
        {
            this.fileName = fileName;
            this.fileType = fileType;

            //为该文件分配下一块内存
            this.filePointer = file_counter++;
        }


        //增加子类
        public void addSonItem(FCB newItem)
        {
            //如果没有儿子，则直接添加
            if(this.son == null)
            {
                this.son = newItem;
                newItem.father = this;
            }
            else
            {
            //如果有儿子，添加到最后一个儿子的兄弟后面
                FCB temp = this.son;
                while(temp.next != null)
                {
                    temp = temp.next;
                }
                temp.next = newItem;
                newItem.pre = temp;
            }
        }


        //将改文件移除时考虑两种情况
        public void remove()
        {
            if(father != null)
            {
                father.son = next;
            }
            else if (pre != null)
            {
                pre.next = next;
            }
        }
    }
}

```

File.cs

```c#
//文件大概设计完毕



using System;

namespace file_system
{
    //Serializable序列化可以保证该类型可以存储到文件中
    [Serializable]
    public class File
    {
        //文件的基本信息
        public string name, size, type, path;

        //创建文件的时间，DateTime类型
        public DateTime createTime;

        //文件指针
        public int filePointer;
        public IndexTable indexPointer;


        //文件的构造函数
        public File(string name,string size)
        {
            this.name = name;
            this.size = size;
            this.createTime = DateTime.Now;
            indexPointer = new IndexTable(); 
        }

        //用PCB创建文件
        public File(FCB item,string fatherPath = "")
        {
            name = item.fileName;
            size = "0";
            type = item.fileType.ToString();
            path = fatherPath + '\\' + name;
            filePointer = item.filePointer;
            indexPointer = new IndexTable();
            createTime = DateTime.Now;

            item.size = size;
            item.path = path;
            item.createTime = createTime;
        }
    }
}

```

IndexTable.cs

```C#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace file_system
{
    //Use muti-level index table to manage the physical structure
    [Serializable]
    public class IndexTable
    {
        private int[] index;
        private int indexPointer;
        private PrimaryIndex primaryIndex;
        private SecondaryIndex secondaryIndex;

        //初始化索引表
        public IndexTable()
        {
            index = new int[100];
            for (int i = 0; i < 100; i++)
            {
                index[i] = -1;
            }
            indexPointer = 0;
        }

        public bool full()
        {
            return indexPointer >= 100;
        }

        public bool addIndex(int data)
        {
            if (!full())
            {
                index[indexPointer] = data;
                indexPointer++;
                if(indexPointer == 100)
                {
                    primaryIndex = new PrimaryIndex();
                }
            }
            else if (!primaryIndex.full())
            {
                primaryIndex.addIndex(data);
                if (primaryIndex.full())
                {
                    secondaryIndex = new SecondaryIndex();
                }
            }
            else if(!secondaryIndex.full())
            {
                secondaryIndex.addIndex(data);
            }
            else
            {
                return false;
            }
            return true;
        }

        public List<int> readTable()
        {
            List<int> content = new List<int>();

            for(int i = 0; i < indexPointer; i++)
            {
                content.Add(index[i]);
            }
            if(indexPointer == 100)
            {
                for(int j = 0;j < primaryIndex.indexPointer; j++)
                {
                    content.Add(primaryIndex.index[j]);
                }
            }
            if (primaryIndex != null && primaryIndex.full())
            {
                foreach (PrimaryIndex temp in secondaryIndex.index)
                {
                    for(int k = 0; k < temp.indexPointer; k++)
                    {
                        content.Add(temp.index[k]);
                    }
                }
            }

            return content;
        }
    }

    [Serializable]
    public class PrimaryIndex
    {
        public int[] index;
        public int indexPointer;

        public PrimaryIndex()
        {
            index = new int[100];
            indexPointer = 0;
        }

        public void addIndex(int data)
        {
            index[indexPointer] = data;
            indexPointer++;
        }
        
        public bool full()
        {
            return indexPointer >= 100;
        }
    }

    [Serializable]
    public class SecondaryIndex
    {
        public List<PrimaryIndex> index;
        public int indexPointer;

        public SecondaryIndex()
        {
            index = new List<PrimaryIndex>();
            index.Add(new PrimaryIndex());
            indexPointer = 0;
        }

        public bool full()
        {
            return indexPointer >= 100;
        }

        public void addIndex(int data)
        {
            PrimaryIndex temp = index[indexPointer];
            if(temp.full())
            {
                index.Add(new PrimaryIndex());
                indexPointer++;
                temp = index[indexPointer];
            }
            temp.addIndex(data);
            indexPointer++;
        }
    }
}

```

## 6. 程序测试

### 6.1 创建文件

![createFile](https://github.com/Easonrust/OS_homework/blob/master/file_system/img/createFile.png)

### 6.2 写入文本文件

![writeFile](https://github.com/Easonrust/OS_homework/blob/master/file_system/img/writeFile.png)

![effect1](https://github.com/Easonrust/OS_homework/blob/master/file_system/img/effect1.png)

### 6.3 重命名文件

![Rename](https://github.com/Easonrust/OS_homework/blob/master/file_system/img/Rename.png)

![effect2](https://github.com/Easonrust/OS_homework/blob/master/file_system/img/effect2.png)

### 6.4 更改当前目录

![changecatalog](https://github.com/Easonrust/OS_homework/blob/master/file_system/img/changecatalog.png)

### 6.5 删除目录

![erase](https://github.com/Easonrust/OS_homework/blob/master/file_system/img/erase.png)

## 7. 运行环境

VS2017+C#
