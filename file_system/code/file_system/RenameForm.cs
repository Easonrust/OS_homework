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
    public partial class RenameForm : Form
    {
        private File renaming_file;
        private FCB renaming_fcb;
        public DelegateMethod.delegateFunction CallBack;

        public RenameForm()
        {
            InitializeComponent();
        }

        public RenameForm(File file, FCB fcb)
        {
            InitializeComponent();
            renaming_file = file;
            renaming_fcb = fcb;
        }
        private void button1_Click(object sender, EventArgs e)
        {
            renaming_file.name = textBox1.Text;
            renaming_fcb.fileName = textBox1.Text;
            

            if(renaming_file.type=="txt")
            {
                renaming_file.name = textBox1.Text+".txt";
                renaming_fcb.fileName = textBox1.Text+ ".txt";
            }
            renaming_file.path = renaming_file.Fatherpath + '\\' + renaming_file.name;
            CallBack();
        }
    }
}
