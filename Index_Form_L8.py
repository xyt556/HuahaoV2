# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Index_Form_L8.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        Form.setMinimumSize(QtCore.QSize(400, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Earth.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.Open_Button = QtWidgets.QPushButton(Form)
        self.Open_Button.setGeometry(QtCore.QRect(310, 20, 31, 21))
        self.Open_Button.setObjectName("Open_Button")
        self.Save_Button = QtWidgets.QPushButton(Form)
        self.Save_Button.setGeometry(QtCore.QRect(310, 60, 31, 21))
        self.Save_Button.setObjectName("Save_Button")
        self.Input_Edit = QtWidgets.QLineEdit(Form)
        self.Input_Edit.setEnabled(True)
        self.Input_Edit.setGeometry(QtCore.QRect(120, 20, 191, 20))
        self.Input_Edit.setObjectName("Input_Edit")
        self.Output_Edit = QtWidgets.QLineEdit(Form)
        self.Output_Edit.setGeometry(QtCore.QRect(120, 60, 191, 20))
        self.Output_Edit.setObjectName("Output_Edit")
        self.Cal_Button = QtWidgets.QPushButton(Form)
        self.Cal_Button.setGeometry(QtCore.QRect(180, 90, 75, 23))
        self.Cal_Button.setObjectName("Cal_Button")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 20, 101, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 140, 331, 121))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form)
        self.Open_Button.clicked.connect(Form.Open_img)
        self.Save_Button.clicked.connect(Form.Save_img)
        self.Cal_Button.clicked.connect(Form.Cal_index)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "遥感指数计算_L8"))
        self.Open_Button.setText(_translate("Form", "…"))
        self.Save_Button.setText(_translate("Form", "…"))
        self.Cal_Button.setText(_translate("Form", "计算"))
        self.label.setText(_translate("Form", "请选择遥感影像："))
        self.label_2.setText(_translate("Form", "保存指数图像："))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:10pt;\">    本模块利用Landsat8 OLI计算植被指数（NDVI）、水体指数（NDWI）、湿度指数及干度指数。</span></p><p><span style=\" font-size:10pt;\">1、选择多波段遥感影像（TIF格式，DAT格式）；</span></p><p><span style=\" font-size:10pt;\">2、设置指数保存路径；</span></p><p><span style=\" font-size:10pt;\">3、计算。</span></p></body></html>"))

