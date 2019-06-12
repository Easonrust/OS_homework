using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Windows.Forms;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
namespace file_system
{
    
    public partial class FileSystem_Window : Form
    {
        //为根目录设置FCB（根目录可看做一个文件夹）
        FCB root_fcb = new FCB();

        //当前所在目录的FCB
        public FCB current_catalog_fcb;

        Stack<File> filestore = new Stack<File> { };
        Catalog catalog = new Catalog();
        public static BitMap bitMap = new BitMap();
        public string dir = System.IO.Path.GetDirectoryName(System.IO.Path.GetDirectoryName(Directory.GetCurrentDirectory()));

        //
        private Dictionary<int, ListViewItem> list_table = new Dictionary<int, ListViewItem>();
        TreeNode root_node;

        //初始化窗口
        public FileSystem_Window()
        {
            InitializeComponent();

            //初始化当前目录为根目录
            current_catalog_fcb = root_fcb;

            
            InitializeListView();
            InitializeTreeView();
            textBox1.Text = "root\\";
        }

        //初始化右侧文件列表
        public void InitializeListView()
        {
            listView1.Items.Clear();
        }

        //初始化左侧目录，同时将根目录结点加入
        public void InitializeTreeView()
        {
            treeView1.Nodes.Clear();
            root_node = new TreeNode("root");
            treeView1.Nodes.Add(root_node);
        }

        //更新右侧文件列表
        public void UpdateListView()
        {
            list_table = new Dictionary<int, ListViewItem>();

            //将之前文件列表的内容清空
            listView1.Items.Clear();


            if (current_catalog_fcb.son != null)
            {
                FCB son = current_catalog_fcb.son;
                do
                {
                    File temp = catalog.getFile(son);
                    ListViewItem file_item = new ListViewItem(new string[]
                    {
                        temp.name,
                        temp.type,
                        temp.size,
                        temp.path
                });
                    
                //建立内存指针与文件项之间的映射关系
                listMap(temp, file_item);

                //将该文件加入当前文件列表
                listView1.Items.Add(file_item);
                son = son.next;
                } while (son != null);
            }
        }

        //建立内存指针与文件项之间的映射关系
        public void listMap(File file, ListViewItem item)
        {
            list_table[file.filePointer] = item;
        }

        //更新左侧文件目录
        public void UpdateTreeView()
        {
            //将当前文件目录中的内容全部清除
            treeView1.Nodes.Clear();
            root_node = new TreeNode("root");
            nodeDFS(root_node, root_fcb);

            //将文件目录树加入到左侧文件目录
            treeView1.Nodes.Add(root_node);
        }

        //对根目录树进行深度优先遍历
        private void nodeDFS(TreeNode node, FCB dir)
        {
            if (dir.son != null)
            {
                FCB son = dir.son;
                do
                {
                    if (son.fileType == FCB.FileType.folder)
                    {
                        TreeNode new_node = new TreeNode(son.fileName);
                        nodeDFS(new_node, son);
                        node.Nodes.Add(new_node);
                    }
                    son = son.next;
                } while (son != null);
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            //当前在根目录下
            if (current_catalog_fcb == root_fcb)
                return;
            current_catalog_fcb = current_catalog_fcb.father;
            if (current_catalog_fcb == root_fcb)
                textBox1.Text = "root\\";
            else
                textBox1.Text = catalog.getFile(current_catalog_fcb).path;
            UpdateListView();
        }


        //与菜单栏的打开链接
        private void 打开ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ListViewItem selected_item = new ListViewItem();

            //如果选中文件个数不只一个，则选中的文件为第一个，否则提示用户选中一个文件
            if (listView1.SelectedItems.Count != 0)
            {
                selected_item = listView1.SelectedItems[0];
            }
            else
            {
                MessageBox.Show("请选择一个文件");
                return;
            }

            //通过内存指针找到该文件
            File selected_file = catalog.getFile(getPointer(selected_item));

            //获得该文件的PCB
            FCB selected_fcb = catalog.getFCB(selected_file);

            open(selected_fcb, selected_file);
        }

        //用于打开文件夹或打开文本文件
        private void open(FCB fcb, File file)
        {
            switch (fcb.fileType)
            {
                //如果打开的是文件夹的话
                case FCB.FileType.folder:

                    //将当前目录设为该文件夹
                    current_catalog_fcb = fcb;

                    //更新地址栏
                    textBox1.Text = catalog.getFile(current_catalog_fcb).path;

                    //更新右侧文件列表
                    UpdateListView();
                    break;

                //如果打开的是文本文件的话
                case FCB.FileType.txt:
                    TextEditor textEditor = new TextEditor(file);
                    textEditor.Show();
                    textEditor.CallBack = UpdateListView;
                    break;
                default:
                    break;
            }
        }

        public int getPointer(ListViewItem item)
        {
            //遍历list_table字典，找到符合的文件返回其内存指针
            foreach (KeyValuePair<int, ListViewItem> kvp in list_table)
            {
               if (kvp.Value.Equals(item))
                   return kvp.Key;
            }
            return -1;
            
        }

        //创建文本文件的操作
        private void 文本文件ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //初始化文本文件名
            //string file_name = nameCheck("New file", ".txt");
            string file_name = "New file.txt";
            string fatherPath;

            //为文本文件创建自己的FCB，并设置其文件类型为文本文件
            FCB new_fcb = new FCB(file_name, FCB.FileType.txt);

            //将文件加到当前目录的子目录中
            current_catalog_fcb.addSonItem(new_fcb);

            //得到当前目录的路径
            File father = catalog.getFile(current_catalog_fcb);
            fatherPath = (father == null) ? "root" : father.path;

            //创建文件
            File new_file = new File(new_fcb, fatherPath);

            filestore.Push(new_file);

            //建立内存指针分别于FCB和文件之间的映射关系
            catalog.map(new_fcb, new_file);

            //更新右侧文件列表
            UpdateListView();
        }

        //创建文件夹的操作
        private void 文件目录ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            string file_name = "New folder";
            string fatherPath;

            //为文件夹创建自己的FCB，并设置其文件类型为文件夹
            FCB new_fcb = new FCB(file_name, FCB.FileType.folder);

            //将文件夹加到当前目录的子目录中
            current_catalog_fcb.addSonItem(new_fcb);

            //得到当前目录的路径
            File father = catalog.getFile(current_catalog_fcb);
            fatherPath = (father == null) ? "root" : father.path;


            File new_file = new File(new_fcb, fatherPath);

            filestore.Push(new_file);
            // 建立内存指针分别与FCB和文件夹之间的映射关系
            catalog.map(new_fcb, new_file);

            //更新左侧文件目录和右侧文件列表
            UpdateTreeView();
            UpdateListView();
        }

        private void 删除ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //如果选中文件个数不只一个，则选中的文件为第一个，否则提示用户选中一个文件
            ListViewItem current_item = new ListViewItem();
            if (listView1.SelectedItems.Count != 0)
            {
                current_item = listView1.SelectedItems[0];
            }
            else
            {
                MessageBox.Show("Please select a item");
                return;
            }

            //通过内存指针找到该文件
            File current_file = catalog.getFile(getPointer(current_item));

            //获得该文件的PCB
            FCB current_fcb = catalog.getFCB(current_file);

            //获得当前文件的所有内存块
            List<int> indexs = current_file.indexPointer.readTable();

            //将所有内存块均置为可用的状态
            bitMap.withdraw(indexs);

            current_fcb.remove();
            UpdateListView();
            UpdateTreeView();
            catalog.removeFile(current_fcb);

            UpdateListView();
            UpdateTreeView();
        }


        //格式化之后文件还在，记录删除，如果不被别的文件覆盖，文件内容可恢复
        private void 格式化ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            root_fcb = new FCB();
            catalog = new Catalog();
            bitMap = new BitMap();
            current_catalog_fcb = root_fcb;

            UpdateListView();
            UpdateTreeView();
        }

        private void 重命名ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //如果选中文件个数不只一个，则选中的文件为第一个，否则提示用户选中一个文件
            ListViewItem current_item = new ListViewItem();
            if (listView1.SelectedItems.Count != 0)
            {
                current_item = listView1.SelectedItems[0];
            }
            else
            {
                MessageBox.Show("Please select a item");
                return;
            }
            //通过内存指针找到该文件
            File current_file = catalog.getFile(getPointer(current_item));

            //获得该文件的PCB
            FCB current_fcb = catalog.getFCB(current_file);

            RenameForm renameForm = new RenameForm(current_file, current_fcb);
            renameForm.Show();
            renameForm.CallBack = UpdateListView;
        }


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

        private void 保存所有ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            serialize();
        }

        private void 访问磁盘上存储的数据ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            deserialize();
            current_catalog_fcb = root_fcb;
            FCB son = new FCB();
            son = root_fcb;
            while (son != null)
            {
                FCB brother = son;

                while (brother != null)
                {
                    foreach (File i in filestore)
                    {
                        if (i.filePointer == brother.filePointer)
                            catalog.map(brother, i);
                    }
                    brother = brother.next;
                }
                son = son.son;
            }
            UpdateListView();
            UpdateTreeView();
            
            

        }

        private void FileSystem_Window_Load(object sender, EventArgs e)
        {

        }

        private void listView1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void listView1_SelectedIndexChanged_1(object sender, EventArgs e)
        {

        }
    }




    //用于处理回调函数
    public class DelegateMethod
    {
        public delegate void delegateFunction();
    }
}
