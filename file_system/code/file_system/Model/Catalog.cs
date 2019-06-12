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
