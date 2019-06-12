//文件大概设计完毕



using System;

namespace file_system
{
    //Serializable序列化可以保证该类型可以存储到文件中
    [Serializable]
    public class File
    {
        //文件的基本信息
        public string name, size, type, path,Fatherpath;

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
            Fatherpath = fatherPath;
            filePointer = item.filePointer;
            indexPointer = new IndexTable();
            createTime = DateTime.Now;

            item.size = size;
            item.path = path;
            item.createTime = createTime;
        }
    }
}
