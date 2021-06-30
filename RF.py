# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:46:09 2020

@author: Yantao XI
"""

# import sys
# import os
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QFileDialog # QApplication, QWidget,
from osgeo import gdal, ogr, gdal_array # I/O image data
import numpy as np # math and array handling
import matplotlib.pyplot as plt # plot figures
from sklearn.ensemble import RandomForestClassifier # classifier
import pandas as pd # handling large data as table sheets
from sklearn.metrics import classification_report, accuracy_score,confusion_matrix  # calculating measures for accuracy assessment
import seaborn as sn
import datetime
from RF_Form import Ui_Form
# from decimal import *

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# import os
# os.environ['PROJ_LIB'] = r'C:\ProgramData\Anaconda3\Lib\site-packages\osgeo\data\proj'

# import os
# import sys
#
# os.environ['PROJ_LIB'] = os.path.dirname(sys.argv[0])


# import os
# import sys
# os.environ['PROJ_LIB'] = os.path.dirname(sys.argv[0])

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串

results_txt = ""
re_accuracy = ""
img_RS = ""
training = ""
validation = ""
classification_image = ""
attribute = 'class'

# define a number of trees that should be used (default = 500)
est = 500

# how many cores should be used?
# -1 -> all available cores
n_cores = -1

class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):

    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)


    # 实现pushButton_click()函数，textEdit是我们放上去的文本框的id OpenValidation_Click()
    def OpenImage_Click(self):
        img_RS1, filetype = QFileDialog.getOpenFileName(self, "选择待分类影像", "./", "图像文件(*.TIF)")
        # fn=QFileDialog.getopenFileName()

        global img_RS
        img_RS = img_RS1
        print(img_RS)
        print(filetype)

        self.Text_img.setPlainText(img_RS)
        return img_RS

    def OpenTrain_Click(self):
        training1, filetype = QFileDialog.getOpenFileName(self, "选择训练数据", "。/", "shape文件(*.shp)")
        # fn=QFileDialog.getopenFileName()
        global training
        training = training1
        print(training)
        print(filetype)
        self.Text_train.setPlainText(training)
        return training

    def OpenValidation_Click(self):
        validation1, filetype = QFileDialog.getOpenFileName(self, "选择验证数据", "。/", "shape文件(*.shp)")
        # fn=QFileDialog.getopenFileName()
        global validation
        validation= validation1
        print(validation)
        print(filetype)
        self.Text_validation.setPlainText(validation)
        return validation

    def SaveImage_Click(self):
        classification_image1, filetype = QFileDialog.getSaveFileName(self, "保存分类图像", "。/", "TIF文件(*.TIF)")
        # fn=QFileDialog.getopenFileName()
        global  classification_image
        classification_image = classification_image1
        print(classification_image1)
        print(filetype)
        self.Text_img_class.setPlainText(classification_image)
        return classification_image

    def Result_Click(self):
        results_txt1, filetype = QFileDialog.getSaveFileName(self, "保存处理说明及精度评价", "。/", "TXT文件(*.TXT)")
        # fn=QFileDialog.getopenFileName()
        global results_txt
        results_txt = results_txt1
        print(results_txt)
        print(filetype)
        self.Text_result.setPlainText(results_txt)
        return results_txt

    def Class_Click(self):


        print(img_RS)

        self.ShowResult.setEnabled(False)
        print("开始")
        print(img_RS)
        global est
        est= int(self.text_tree.text())
        print(est)
        self.label_status.setText("")
        self.label_status.setText("解译进行中，请稍后……")
        print(self.label_status.text())
        # laod training data and show all shape attributes

        # model_dataset = gdal.Open(model_raster_fname)
        shape_dataset = ogr.Open(training)
        shape_layer = shape_dataset.GetLayer()

        # extract the names of all attributes (fieldnames) in the shape file
        attributes = []
        ldefn = shape_layer.GetLayerDefn()
        for n in range(ldefn.GetFieldCount()):
            fdefn = ldefn.GetFieldDefn(n)
            attributes.append(fdefn.name)

        # print the attributes
        print('训练集中所用属性: {}'.format(attributes))

        # ### Section - Data preparation



        # prepare results text file:
        start = datetime.datetime.now()

        print('决策树分类（随机森林树）', file=open(results_txt, "a"))
        print('开始处理时间：{}'.format(datetime.datetime.now()), file=open(results_txt, "a"))
        print('-------------------------------------------------', file=open(results_txt, "a"))
        print('文件路径：', file=open(results_txt, "a"))
        print('待分类影像：{}'.format(img_RS), file=open(results_txt, "a"))
        print('训练数据：{}'.format(training), file=open(results_txt, "a"))
        print('验证数据：{}'.format(validation), file=open(results_txt, "a"))
        print('      类别属性：{}'.format(attribute), file=open(results_txt, "a"))
        print('分类结果影像：{}'.format(classification_image), file=open(results_txt, "a"))
        print('分类过程说明文件：{}'.format(results_txt), file=open(results_txt, "a"))
        print('-------------------------------------------------', file=open(results_txt, "a"))



        # load image data

        img_ds = gdal.Open(img_RS, gdal.GA_ReadOnly)

        img = np.zeros((img_ds.RasterYSize, img_ds.RasterXSize, img_ds.RasterCount),
                       gdal_array.GDALTypeCodeToNumericTypeCode(img_ds.GetRasterBand(1).DataType))
        for b in range(img.shape[2]):
            img[:, :, b] = img_ds.GetRasterBand(b + 1).ReadAsArray()


        row = img_ds.RasterYSize
        col = img_ds.RasterXSize
        band_number = img_ds.RasterCount
        # Does the raster have a description or metadata?
        desc = img_ds.GetDescription()
        metadata = img_ds.GetMetadata()  # 得到的元数据

        print('影像范围：{} x {} (row x col)'.format(row, col))
        print('波段个数：{}'.format(band_number))

        print('影像范围：{} x {} （行 x 列)'.format(row, col), file=open(results_txt, "a"))
        print('波段个数：{}'.format(band_number), file=open(results_txt, "a"))
        print('---------------------------------------', file=open(results_txt, "a"))
        print('训练', file=open(results_txt, "a"))
        print('树的个数：{}'.format(est), file=open(results_txt, "a"))



        # laod training data from shape file

        # model_dataset = gdal.Open(model_raster_fname)
        shape_dataset = ogr.Open(training)
        shape_layer = shape_dataset.GetLayer()

        mem_drv = gdal.GetDriverByName('MEM')
        mem_raster = mem_drv.Create('', img_ds.RasterXSize, img_ds.RasterYSize, 1, gdal.GDT_UInt16)
        mem_raster.SetProjection(img_ds.GetProjection())
        mem_raster.SetGeoTransform(img_ds.GetGeoTransform())
        mem_band = mem_raster.GetRasterBand(1)
        mem_band.Fill(0)
        mem_band.SetNoDataValue(0)

        att_ = 'ATTRIBUTE=' + attribute
        # http://gdal.org/gdal__alg_8h.html#adfe5e5d287d6c184aab03acbfa567cb1
        # http://gis.stackexchange.com/questions/31568/gdal-rasterizelayer-doesnt-burn-all-polygons-to-raster
        err = gdal.RasterizeLayer(mem_raster, [1], shape_layer, None, None, [1], [att_, "ALL_TOUCHED=TRUE"])
        assert err == gdal.CE_None

        roi = mem_raster.ReadAsArray()



        # Display images
        plt.figure(num="图像波段1预览",
                   figsize=(5, 5),
                   dpi=100,
                   facecolor="#e9e7ef",
                   edgecolor='#827100')
        plt.subplot(121)
        plt.imshow(img[:, :, 0], cmap=plt.cm.Greys_r)
        plt.title('待分类影像 - 波段1')

        plt.subplot(122)
        plt.imshow(roi, cmap=plt.cm.Spectral)
        plt.title('训练影像')

        plt.show()

        # Number of training pixels:
        n_samples = (roi > 0).sum()
        print('{n} 训练样本'.format(n=n_samples))
        print('{n} 训练样本'.format(n=n_samples), file=open(results_txt, "a"))

        # What are our classification labels?
        labels = np.unique(roi[roi > 0])
        print('训练数据包括 {n} 类: {classes}'.format(n=labels.size, classes=labels))
        print('训练样本包括 {n} 类: {classes}'.format(n=labels.size, classes=labels),
              file=open(results_txt, "a"))

        # Subset the image dataset with the training image = X
        # Mask the classes on the training dataset = y
        # These will have n_samples rows
        X = img[roi > 0, :]
        y = roi[roi > 0]

        print('Our X matrix is sized: {sz}'.format(sz=X.shape))
        print('Our y array is sized: {sz}'.format(sz=y.shape))

        # ### Section - Train Random Forest



        rf = RandomForestClassifier(n_estimators=est, oob_score=True, verbose=1, n_jobs=n_cores)

        # verbose = 2 -> prints out every tree progression
        # rf = RandomForestClassifier(n_estimators=est, oob_score=True, verbose=2, n_jobs=n_cores)

        X = np.nan_to_num(X)
        rf2 = rf.fit(X, y)

        # ### Section - RF Model Diagnostics

        #

        # With our Random Forest model fit, we can check out the "Out-of-Bag" (OOB) prediction score:

        print('--------------------------------', file=open(results_txt, "a"))
        print('训练和模型诊断:', file=open(results_txt, "a"))
        print('OOB prediction of accuracy is: {oob}%'.format(oob=rf.oob_score_ * 100))
        print('OOB（Out of Bag）精度预测: {oob}%'.format(oob=rf.oob_score_ * 100), file=open(results_txt, "a"))

        # we can show the band importance:
        bands = range(1, img_ds.RasterCount + 1)

        for b, imp in zip(bands, rf2.feature_importances_):
            print('Band {b} importance: {imp}'.format(b=b, imp=imp))
            print('波段 {b} 重要性： {imp}'.format(b=b, imp=imp), file=open(results_txt, "a"))

        # Let's look at a crosstabulation to see the class confusion.
        # To do so, we will import the Pandas library for some help:
        # Setup a dataframe -- just like R
        # Exception Handling because of possible Memory Error

        try:
            df = pd.DataFrame()
            df['truth'] = y
            df['predict'] = rf.predict(X)

        except MemoryError:
            print('Crosstab not available ')

        else:
            # Cross-tabulate predictions
            print(pd.crosstab(df['truth'], df['predict'], margins=True))
            print(pd.crosstab(df['truth'], df['predict'], margins=True), file=open(results_txt, "a"))



        cm = confusion_matrix(y, rf.predict(X))
        plt.figure(num="混淆矩阵",
                   figsize=(5, 5),
                   dpi=100,
                   facecolor="#e9e7ef",
                   edgecolor='#827100')
        # plt.figure(figsize=(10, 7))
        sn.heatmap(cm, annot=True, fmt='g')
        plt.xlabel('类别 - 预测值')
        plt.ylabel('类别 - 真实值')
        plt.show()

        # ### Section - Prediction



        # Predicting the rest of the image

        # Take our full image and reshape into long 2d array (nrow * ncol, nband) for classification
        new_shape = (img.shape[0] * img.shape[1], img.shape[2])
        img_as_array = img[:, :, :np.int(img.shape[2])].reshape(new_shape)

        print('Reshaped from {o} to {n}'.format(o=img.shape, n=img_as_array.shape))

        img_as_array = np.nan_to_num(img_as_array)



        # Now predict for each pixel
        # first prediction will be tried on the entire image
        # if not enough RAM, the dataset will be sliced
        # slices = int(round(len(img_as_array)/2))
        try:
            class_prediction = rf.predict(img_as_array)
        except MemoryError:
            slices = int(round(len(img_as_array) / 2))

            test = True

            while test == True:
                try:
                    class_preds = list()

                    temp = rf.predict(img_as_array[0:slices + 1, :])
                    class_preds.append(temp)

                    for i in range(slices, len(img_as_array), slices):
                        print('{} %, derzeit: {}'.format((i * 100) / (len(img_as_array)), i))
                        temp = rf.predict(img_as_array[i + 1:i + (slices + 1), :])
                        class_preds.append(temp)

                except MemoryError as error:
                    slices = slices / 2
                    print('Not enought RAM, new slices = {}'.format(slices))

                else:
                    test = False
        else:
            print('Class prediction was successful without slicing!')



        # concatenate all slices and re-shape it to the original extend
        try:
            class_prediction = np.concatenate(class_preds, axis=0)
        except NameError:
            print('No slicing was necessary!')

        class_prediction = class_prediction.reshape(img[:, :, 0].shape)
        print('Reshaped back to {}'.format(class_prediction.shape))

        # ### Section - Masking
        #
        # - Mask classification image (black border = 0)
        #



        # generate mask image from red band
        mask = np.copy(img[:, :, 0])
        mask[mask > 0.0] = 1.0  # all actual pixels have a value of 1.0

        # plot mask

        # plt.imshow(mask)



        # mask classification an plot

        class_prediction.astype(np.float16)
        class_prediction_ = class_prediction * mask

        plt.figure(num="解译结果预览",
                   figsize=(5, 5),
                   dpi=100,
                   facecolor="#e9e7ef",
                   edgecolor='#827100')
        plt.subplot(121)
        plt.imshow(class_prediction, cmap=plt.cm.Spectral)
        plt.title('未掩膜分类影像')# classification unmasked

        plt.subplot(122)
        plt.imshow(class_prediction_, cmap=plt.cm.Spectral)
        plt.title('掩膜分类影像') #classification masked

        plt.show()

        # ### Section - Saving Classification Image to disk



        cols = img.shape[1]
        rows = img.shape[0]

        class_prediction_.astype(np.float16)

        driver = gdal.GetDriverByName("gtiff")
        outdata = driver.Create(classification_image, cols, rows, 1, gdal.GDT_UInt16)
        outdata.SetGeoTransform(img_ds.GetGeoTransform())  ##sets same geotransform as input
        outdata.SetProjection(img_ds.GetProjection())  ##sets same projection as input
        outdata.GetRasterBand(1).WriteArray(class_prediction_)
        outdata.FlushCache()  ##saves to disk!!
        print('Image saved to: {}'.format(classification_image))

        # ### Section - Accuracy Assessment



        # validation / accuracy assessment

        # preparing ttxt file

        print('------------------------------------', file=open(results_txt, "a"))
        print('验证', file=open(results_txt, "a"))

        # laod training data from shape file
        shape_dataset_v = ogr.Open(validation)
        shape_layer_v = shape_dataset_v.GetLayer()
        mem_drv_v = gdal.GetDriverByName('MEM')
        mem_raster_v = mem_drv_v.Create('', img_ds.RasterXSize, img_ds.RasterYSize, 1, gdal.GDT_UInt16)
        mem_raster_v.SetProjection(img_ds.GetProjection())
        mem_raster_v.SetGeoTransform(img_ds.GetGeoTransform())
        mem_band_v = mem_raster_v.GetRasterBand(1)
        mem_band_v.Fill(0)
        mem_band_v.SetNoDataValue(0)

        # http://gdal.org/gdal__alg_8h.html#adfe5e5d287d6c184aab03acbfa567cb1
        # http://gis.stackexchange.com/questions/31568/gdal-rasterizelayer-doesnt-burn-all-polygons-to-raster
        err_v = gdal.RasterizeLayer(mem_raster_v, [1], shape_layer_v, None, None, [1], [att_, "ALL_TOUCHED=TRUE"])
        assert err_v == gdal.CE_None

        roi_v = mem_raster_v.ReadAsArray()

        # vizualise
        plt.figure(num="解译结果&样本",
                   figsize=(5, 5),
                   dpi=100,
                   facecolor="#e9e7ef",
                   edgecolor='#827100')
        plt.subplot(221)
        plt.imshow(img[:, :, 0], cmap=plt.cm.Greys_r)
        plt.title('分类影像 - 波段1')

        plt.subplot(222)
        plt.imshow(class_prediction, cmap=plt.cm.Spectral)
        plt.title('分类结果')

        plt.subplot(223)
        plt.imshow(roi, cmap=plt.cm.Spectral)
        plt.title('训练数据')

        plt.subplot(224)
        plt.imshow(roi_v, cmap=plt.cm.Spectral)
        plt.title('验证数据')

        plt.show()

        # Find how many non-zero entries we have -- i.e. how many validation data samples?
        n_val = (roi_v > 0).sum()
        print('{n} validation pixels'.format(n=n_val))
        print('{n} 验证像素数'.format(n=n_val), file=open(results_txt, "a"))

        # What are our validation labels?
        labels_v = np.unique(roi_v[roi_v > 0])
        print('validation data include {n} classes: {classes}'.format(n=labels_v.size, classes=labels_v))
        print('验证数据包括 {n} 类： {classes}'.format(n=labels_v.size, classes=labels_v),
              file=open(results_txt, "a"))
        # Subset the classification image with the validation image = X
        # Mask the classes on the validation dataset = y
        # These will have n_samples rows
        X_v = class_prediction[roi_v > 0]
        y_v = roi_v[roi_v > 0]

        print('Our X matrix is sized: {sz_v}'.format(sz_v=X_v.shape))
        print('Our y array is sized: {sz_v}'.format(sz_v=y_v.shape))

        # Cross-tabulate predictions
        # confusion matrix
        convolution_mat = pd.crosstab(y_v, X_v, margins=True)
        print(convolution_mat)
        print(convolution_mat, file=open(results_txt, "a"))
        # if you want to save the confusion matrix as a CSV file:
        re_accuracy = results_txt.replace('TXT','CSV') # 'C:\\save\\to\\folder\\conf_matrix_' + str(est) + '.csv'
        print(re_accuracy)
        convolution_mat.to_csv(re_accuracy, sep=';', decimal = '.')


        # information about precision, recall, f1_score, and support:
        # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html
        # sklearn.metrics.precision_recall_fscore_support
        target_names = list()
        for name in range(1, (labels.size) + 1):
            target_names.append(str(name))
        sum_mat = classification_report(y_v, X_v, target_names=target_names)
        print(sum_mat)
        print(sum_mat, file=open(results_txt, "a"))


        # Overall Accuracy (OAA)
        print('OAA = {} %'.format(accuracy_score(y_v, X_v) * 100))
        print('OAA = {} %'.format(accuracy_score(y_v, X_v) * 100), file=open(results_txt, "a"))
        print('结束处理时间：{}'.format(datetime.datetime.now()), file=open(results_txt, "a"))
        end = datetime.datetime.now()
        use_time = (end - start).seconds / 60.0
        print('用时：{}分'.format(use_time), file=open(results_txt, "a"))
        self.label_status.setText("解译完成！用时：" + str(int(use_time))+ "分")


        cm_val = confusion_matrix(roi_v[roi_v > 0], class_prediction[roi_v > 0])
        plt.figure(num="验证结果预览",
                   figsize=(5, 5),
                   dpi=100,
                   facecolor="#e9e7ef",
                   edgecolor='#827100')
        # plt.figure(figsize=(10, 7))
        
        sn.heatmap(cm_val, annot=True, fmt='g')
        plt.xlabel('类别 - 预测')
        plt.ylabel('类别 - 实际')
        plt.show()
        self.ShowResult.setEnabled(True)

    def ShowResult_Click(self):
        global results_txt
        f = open(results_txt, 'r')
        with f:
            data = f.read()
            self.textEdit_2.setText(data)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
    input("any key")