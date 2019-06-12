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
