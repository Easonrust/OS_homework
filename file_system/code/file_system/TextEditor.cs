using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace file_system
{
   

    public partial class TextEditor : Form
    {
        private File textFile;
        private BitMap bitMap = FileSystem_Window.bitMap;
        public DelegateMethod.delegateFunction CallBack;

        public TextEditor()
        {
            InitializeComponent();
        }

        
        public TextEditor(File file)
        {
            InitializeComponent();
            textFile = file;
            showContent();
        }

        private void showContent()
        {
            //取出文件所有内存块的数据，合并后显示
            List<int> indexs = textFile.indexPointer.readTable();
            string content = "";
            foreach (int i in indexs)
            {
                content += bitMap.getBlock(i);
            }
            richTextBox1.Text = content;
        }

     
        private void writeDisk()
        {
            string content = richTextBox1.Text;

            //设置文件大小与文件内容
            textFile.size = (content.Length).ToString() + "B";

            //更新内容时先把磁盘上的块全部置为可用
            releaseBlock();

            //更新文件指针并写入内容
            textFile.indexPointer = bitMap.write(content);
        }


        private void releaseBlock()
        {
            List<int> indexs = textFile.indexPointer.readTable();
            bitMap.withdraw(indexs);
        }

        private void TextEditor_Load(object sender, EventArgs e)
        {

        }

        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            writeDisk();
            CallBack();
        }
    }
}
