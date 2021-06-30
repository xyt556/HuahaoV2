# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClipTif_Form.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(550, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(550, 150))
        Form.setMaximumSize(QtCore.QSize(550, 150))
        Form.setSizeIncrement(QtCore.QSize(400, 150))
        Form.setBaseSize(QtCore.QSize(400, 150))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Earth.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAutoFillBackground(False)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_inputpath = QtWidgets.QLineEdit(Form)
        self.lineEdit_inputpath.setObjectName("lineEdit_inputpath")
        self.horizontalLayout.addWidget(self.lineEdit_inputpath)
        self.btn_OpenPath = QtWidgets.QPushButton(Form)
        self.btn_OpenPath.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Directory incative.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_OpenPath.setIcon(icon1)
        self.btn_OpenPath.setObjectName("btn_OpenPath")
        self.horizontalLayout.addWidget(self.btn_OpenPath)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit_shpfile = QtWidgets.QLineEdit(Form)
        self.lineEdit_shpfile.setObjectName("lineEdit_shpfile")
        self.horizontalLayout_2.addWidget(self.lineEdit_shpfile)
        self.btn_OpenShp = QtWidgets.QPushButton(Form)
        self.btn_OpenShp.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("fileopen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_OpenShp.setIcon(icon2)
        self.btn_OpenShp.setObjectName("btn_OpenShp")
        self.horizontalLayout_2.addWidget(self.btn_OpenShp)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("AcadEref")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit_outputpath = QtWidgets.QLineEdit(Form)
        self.lineEdit_outputpath.setObjectName("lineEdit_outputpath")
        self.horizontalLayout_3.addWidget(self.lineEdit_outputpath)
        self.btn_SavePath = QtWidgets.QPushButton(Form)
        self.btn_SavePath.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("save11.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_SavePath.setIcon(icon3)
        self.btn_SavePath.setObjectName("btn_SavePath")
        self.horizontalLayout_3.addWidget(self.btn_SavePath)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.btn_Clip = QtWidgets.QPushButton(Form)
        self.btn_Clip.setObjectName("btn_Clip")
        self.horizontalLayout_4.addWidget(self.btn_Clip)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Form)
        self.btn_OpenPath.clicked.connect(Form.openPath_click)
        self.btn_SavePath.clicked.connect(Form.savePath_click)
        self.btn_OpenShp.clicked.connect(Form.openShp_click)
        self.btn_Clip.clicked.connect(Form.btn_clip_click)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "单波段TIF文件裁剪与合成"))
        self.label.setText(_translate("Form", "请指定TIF文件所在目录："))
        self.label_3.setText(_translate("Form", "请输入裁剪区域文件："))
        self.label_2.setText(_translate("Form", "请指裁剪后TIF文件保存目录："))
        self.btn_Clip.setText(_translate("Form", "裁剪"))