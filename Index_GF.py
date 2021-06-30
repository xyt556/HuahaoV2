# -*- coding: utf-8 -*-


from Index_Form_GF import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
import R_D_Image as rd
import sys
from osgeo import gdal, gdal_array
import numpy as np


class MyIndex_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyIndex_Form, self).__init__()
        self.setupUi(self)
    def Open_img(self):
        global img_RS
        img_RS, filetype = QFileDialog.getOpenFileName(self, "选择遥感影像", "./", "TIF文件 (*.tif);;TIFF文件 (*.tiff);;Envi文件(*.dat);;All Files (*)")
        # global prj
        # global geotrans
        # global data
        self.Input_Edit.setText(img_RS)

        # prj, geotrans, data = rd.read_img(img_RS)
        # gdal_array.numpy.seterr(all="ignore")
        # data = data.astype(np.float)  # 强制类型转换为float
        # return prj, geotrans, data

    def Save_img(self):
        global Index_img_path

        # Index_img, filetype = QFileDialog.getSaveFileName(self, "保存指数图像", "。/", "TIF文件(*.tif)")

        Index_img_path = QFileDialog.getExistingDirectory(self, "请选择指数保存路径")
        self.Output_Edit.setText(Index_img_path)



    def Cal_index(self):
        # global prj
        # global geotrans
        # global data
        # 文本框获取文件路径及文件名
        data_name = self.Input_Edit.text()
        prj, geotrans, data = rd.read_img(data_name)
        gdal_array.numpy.seterr(all="ignore")
        data = data.astype(np.float)  # 强制类型转换为float
        # global ndvi
        ndvi = rd.get_ndvi_gf(data)
        ndwi = rd.get_ndwi_gf(data)
        # 文本框获取文件路径及文件名
        Index_img_path = self.Output_Edit.text()
        print(Index_img_path)
        rd.write_img(Index_img_path + "/NDVI.TIF", prj, geotrans, ndvi)
        print("ndvi保存完成")
        rd.write_img(Index_img_path + "/NDWI.TIF", prj, geotrans, ndwi)
        print("ndwi保存完成")
        reply = QMessageBox.about(self, "提示", "计算完成")
        # return ndvi


if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = MyIndex_Form()
    md.show()
    sys.exit(app.exec_())
