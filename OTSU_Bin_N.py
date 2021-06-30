# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:46:09 2020

@author: Yantao XI
"""

import matplotlib.pyplot as plt
# from skimage import data, io
# from skimage.filters import threshold_otsu
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
import R_D_Image as rd
from osgeo import gdal
import matplotlib.pyplot as plt

try:
    from skimage import filters
except ImportError:
    from skimage import filter as filters
from skimage import io, exposure, img_as_uint, img_as_float


import sys
from OTSU_Form import Ui_Form
from PyQt5 import QtWidgets
import numpy as np
# import pandas as pa
# import cv2
# import numpy as np
# from osgeo import gdal
# import os
# image = "ndvi.tif"
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串
class MyIndex_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyIndex_Form, self).__init__()
        self.setupUi(self)
    def Open_img(self):
        global img_RS
        img_RS, filetype = QFileDialog.getOpenFileName(self, "选择遥感影像", "./", "All Files (*);;TIF文件 (*.tif);;Envi文件(*.dat)")
        # global prj
        # global geotrans
        # global data
        self.Input_Edit.setText(img_RS)
    def Save_img(self):
        global Bin_img

        Bin_img, filetype = QFileDialog.getSaveFileName(self, "保存二值化图像", "./", "TIF文件(*.tif)")

        # Index_img_path = QFileDialog.getExistingDirectory(self, "请选择指数保存路径")
        self.Output_Edit.setText(Bin_img)

    def Binarization(self):
        print(img_RS)
        dataset = gdal.Open(img_RS) #rd.read_img(img_RS)
        # image = io.imread("./data/ndwi.tif" ,as_gray= False)#data.camera()
        im_width = dataset.RasterXSize  # 栅格矩阵的列数
        im_height = dataset.RasterYSize  # 栅格矩阵的行数

        im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
        im_proj = dataset.GetProjection()  # 地图投影信息
        # im_data = dataset.ReadAsArray(0, 0, im_width, im_height


        print(type(dataset))
        # mask = image <=0
        # image[mask] = 255
        print(dataset)

        #去除NaN？？？？
        camera = np.array(dataset.GetRasterBand(1).ReadAsArray())

        camera2 = camera.flatten()
        camera2 = [i for i in camera2 if (i >= -1 and i <= 1)]
        camera2 = np.asarray(camera2)
        plt.figure(figsize=(9, 4))
        plt.subplot(131)
        plt.imshow(camera, cmap='hot', interpolation='nearest')
        plt.axis('off')

        val = filters.threshold_otsu(camera2)
        print(val)
        camera[camera < val] = 0#np.nan
        camera[camera > val] = 1  # np.nan
        # im = exposure.rescale_intensity(camera, out_range='float')
        # im = img_as_float(im)
        rd.write_img(Bin_img, im_proj, im_geotrans, camera)

        hist, bins_center = exposure.histogram(camera2)


        # image = [x for x in image if not pa.isnull(x)]

        # print(image)
        # skimage OTSU算法-------------------------------
        # thresh = threshold_otsu(image)
        # thresh = 150
        # image[mask] = 255
        print(val)

        # binary = image > thresh  # >
        # -------------------------------------------------
        # # CV2OTSU算法
        # thresh, binary = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
        # # print(binary)
        self.Bin_Edit.setText(str(val))

        # rd.write_img(Bin_img, im_proj, im_geotrans, binary)
        # io.imsave("OTSU.tif",binary,plugin=None,check_contrast=True)
        # io.show("OTSU.tif")
        # io.imsave("OTSU.tif", binary)
        self.Cust_Button.setEnabled(True)


        plt.subplot(132)
        plt.imshow(camera, cmap='gray', interpolation='nearest')
        plt.axis('off')
        plt.subplot(133)

        plt.plot(bins_center, hist, lw=2)
        plt.axvline(val, color='k', ls='--')
        plt.text(val + 0.02, 1000, 't* = ' + str(val), fontsize=12)
        # plt.tight_layout()
        plt.savefig("./otsu_image", dpi=600)
        plt.show()


        # fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
        # ax = axes.ravel()
        # ax[0] = plt.subplot(1, 3, 1)
        # ax[1] = plt.subplot(1, 3, 2)
        # ax[2] = plt.subplot(1, 3, 3, sharex=ax[0], sharey=ax[0])
        #
        # ax[0].imshow(image, cmap=plt.cm.gray)
        # ax[0].set_title('原始图像')
        # ax[0].axis('off')
        #
        # ax[1].hist(image.ravel(), bins=256)
        # ax[1].set_title('直方图')
        # ax[1].axvline(thresh, color='r')
        #
        # ax[2].imshow(binary, cmap=plt.cm.gray)
        # ax[2].set_title('二值化图')
        # ax[2].axis('off')
        #
        # plt.show()
        reply = QMessageBox.about(self, "提示", "二值化完成")

    def Cust_Binarization(self):
        print(img_RS)
        dataset = gdal.Open(img_RS)  # rd.read_img(img_RS)
        # image = io.imread("./data/ndwi.tif" ,as_gray= False)#data.camera()
        im_width = dataset.RasterXSize  # 栅格矩阵的列数
        im_height = dataset.RasterYSize  # 栅格矩阵的行数

        im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
        im_proj = dataset.GetProjection()  # 地图投影信息
        # im_data = dataset.ReadAsArray(0, 0, im_width, im_height

        print(type(dataset))
        # mask = image <=0
        # image[mask] = 255
        print(dataset)

        # 去除NaN？？？？
        camera = np.array(dataset.GetRasterBand(1).ReadAsArray())

        camera2 = camera.flatten()
        camera2 = [i for i in camera2 if (i >= -1 and i <= 1)]
        camera2 = np.asarray(camera2)

        # val = filters.threshold_otsu(camera2)
        # val 通过文本框获取，手动二值化
        plt.figure(figsize=(9, 4))
        plt.subplot(131)
        plt.imshow(camera, cmap='hot', interpolation='nearest')
        plt.axis('off')
        val = float(self.Bin_Edit.text())
        print(val)
        camera[camera < val] = 0  # np.nan
        camera[camera > val] = 1  # np.nan
        # im = exposure.rescale_intensity(camera, out_range='float')
        # im = img_as_float(im)
        rd.write_img(Bin_img, im_proj, im_geotrans, camera)
        path = self.Output_Edit.text()[:-4]

        Bin_img_cust = path + '_Cust.tif'
        print(Bin_img_cust)


        rd.write_img(Bin_img_cust, im_proj, im_geotrans, camera)

        hist, bins_center = exposure.histogram(camera2)

        # image = [x for x in image if not pa.isnull(x)]

        # print(image)
        # skimage OTSU算法-------------------------------
        # thresh = threshold_otsu(image)
        # thresh = 150
        # image[mask] = 255
        print(val)

        # binary = image > thresh  # >
        # -------------------------------------------------
        # # CV2OTSU算法
        # thresh, binary = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
        # # print(binary)
        # self.Bin_Edit.setText(str(val))

        # rd.write_img(Bin_img, im_proj, im_geotrans, binary)
        # io.imsave("OTSU.tif",binary,plugin=None,check_contrast=True)
        # io.show("OTSU.tif")
        # io.imsave("OTSU.tif", binary)
        # self.Cust_Button.setEnabled(True)


        plt.subplot(132)
        plt.imshow(camera, cmap='gray', interpolation='nearest')
        plt.axis('off')
        plt.subplot(133)

        plt.plot(bins_center, hist, lw=2)
        plt.axvline(val, color='k', ls='--')
        plt.text(val + 0.02, 1000, 't* = ' + str(val), fontsize=12)
        # plt.tight_layout()
        plt.savefig("./otsu_image", dpi=600)
        plt.show()
        # im_proj, im_geotrans, image = rd.read_img(img_RS)
        # # image = io.imread("./data/ndwi.tif" ,as_gray= False)#data.camera()
        # print(image)
        #
        # # mask = image <=0
        # # image[mask] = 255
        #
        # # print(image)
        # # thresh = threshold_otsu(image)
        # # thresh = 150
        # # image[mask] = 255
        # # self.Bin_Edit.setText(str(thresh))
        #
        # thresh = float(self.Bin_Edit.text())
        # print(thresh)
        #
        # binary = image > thresh  # >
        # # print(binary)
        # path = self.Output_Edit.text()[:-4]
        #
        # Bin_img_cust = path + '_Cust.tif'
        # print(Bin_img_cust)
        #
        #
        # rd.write_img(Bin_img_cust, im_proj, im_geotrans, binary)
        # # io.imsave("OTSU.tif",binary,plugin=None,check_contrast=True)
        # # io.show("OTSU.tif")
        # # io.imsave("OTSU.tif", binary)
        #
        # fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
        # ax = axes.ravel()
        # ax[0] = plt.subplot(1, 3, 1)
        # ax[1] = plt.subplot(1, 3, 2)
        # ax[2] = plt.subplot(1, 3, 3, sharex=ax[0], sharey=ax[0])
        #
        # ax[0].imshow(image, cmap=plt.cm.gray)
        # ax[0].set_title('原始图像')
        # ax[0].axis('off')
        #
        # ax[1].hist(image.ravel(), bins=256)
        # ax[1].set_title('直方图')
        # ax[1].axvline(thresh, color='r')
        #
        # ax[2].imshow(binary, cmap=plt.cm.gray)
        # ax[2].set_title('二值化图')
        # ax[2].axis('off')
        #
        # plt.show()
        reply = QMessageBox.about(self, "提示", "二值化完成")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = MyIndex_Form()
    md.show()
    sys.exit(app.exec_())

