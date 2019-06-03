# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\yangl\Desktop\OS_memory\memory_management.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(720, 430)
        self.Block_Page=[]
        for i in range(4):
            self.Block_Page.append(QtWidgets.QLCDNumber(Form))
            self.Block_Page[i].setGeometry(QtCore.QRect(20+180*i, 40, 128, 46))
       
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 20, 82, 18))

        
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(220, 20, 82, 18))

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(420, 20, 82, 18))
        

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(600, 20, 82, 18))
        

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(20, 120, 182, 32))
        self.current_instruction = QtWidgets.QLCDNumber(Form)
        self.current_instruction.setGeometry(QtCore.QRect(20, 160, 182, 46))

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(300, 120, 42, 32))
        self.current_page = QtWidgets.QLCDNumber(Form)
        self.current_page.setGeometry(QtCore.QRect(240, 160, 182, 46))
        
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(440, 120, 242, 32))
        self.algo = QtWidgets.QComboBox(Form)
        self.algo.setGeometry(QtCore.QRect(440, 160, 242, 44))
        self.algo.addItem("FIFO")
        self.algo.addItem("LRU")
        
        self.startButton = QtWidgets.QPushButton(Form)
        self.startButton.setGeometry(QtCore.QRect(20, 240, 182, 34))
        
        self.SingleButton = QtWidgets.QPushButton(Form)
        self.SingleButton.setGeometry(QtCore.QRect(240, 240, 162, 34))
        
        self.ToEndButton = QtWidgets.QPushButton(Form)
        self.ToEndButton.setGeometry(QtCore.QRect(440, 240, 242, 34))
        
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(20, 300, 182, 32))
        self.fault_times = QtWidgets.QLCDNumber(Form)
        self.fault_times.setGeometry(QtCore.QRect(20, 340, 182, 46))
        
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(240, 296, 142, 42))
        self.label_9.setObjectName("label_9")
        self.fault_rate = QtWidgets.QLCDNumber(Form)
        self.fault_rate.setGeometry(QtCore.QRect(240, 340, 182, 46))
        
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(440, 340, 82, 42))

        
        
        

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Block1"))
        self.label_2.setText(_translate("Form", "Block2"))
        self.label_3.setText(_translate("Form", "Block3"))
        self.label_4.setText(_translate("Form", "Block4"))
        self.label_5.setText(_translate("Form", "Current Instructions"))
        self.label_6.setText(_translate("Form", "Page"))
        self.label_7.setText(_translate("Form", "Page-replacement algorithm"))
        self.startButton.setText(_translate("Form", "Rand start Address"))
        self.SingleButton.setText(_translate("Form", "Single Step"))
        self.ToEndButton.setText(_translate("Form", "Execute to the End"))
        self.label_8.setText(_translate("Form", "Page-Fault times"))
        self.label_9.setText(_translate("Form", "Page-Fault Rate"))
        self.label_10.setText(_translate("Form", "%"))

