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
