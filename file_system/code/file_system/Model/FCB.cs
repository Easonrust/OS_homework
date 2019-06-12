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
                newItem.father = this;
            }
        }


        //将改文件移除时考虑两种情况
        public void remove()
        {
            if(father != null&& pre == null)
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
