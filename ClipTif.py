from osgeo import gdal
import os
from ClipTif_Form import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
import os
import importlib,sys
importlib.reload(sys)



class MyClip_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyClip_Form, self).__init__()
        self.setupUi(self)
    def openPath_click(self):
        global inputPath
        inputPath = QFileDialog.getExistingDirectory(self, "选择源TIF所在文件夹", "./")
        self.lineEdit_inputpath.setText(inputPath)
        inputPath = self.lineEdit_inputpath.text() + "/"
        return inputPath
    def savePath_click(self):
        global outputPath
        outputPath = QFileDialog.getExistingDirectory(self, "保存文件", "./")
        print(outputPath)
        self.lineEdit_outputpath.setText(outputPath)
        outputPath = self.lineEdit_outputpath.text() + "/"
        return outputPath
    def openShp_click(self):
        global shp_clip
        shp_clip, filetype = QFileDialog.getOpenFileName(self, "选择裁剪文件", "./", "SHP文件(*.shp)")
        self.lineEdit_shpfile.setText(shp_clip)
        shp_clip = self.lineEdit_shpfile.text()
        return shp_clip
    def btn_clip_click(self):
        global band
        bandList = [band for band in os.listdir(inputPath) if band[-4:] == '.TIF']
        print(bandList)
        print(shp_clip)
        # outputPath
        for band in bandList:
            print(outputPath + band[:-4] + '_clip' + band[-4:])
            options = gdal.WarpOptions(cutlineDSName=shp_clip, cropToCutline=True)
            global outBand
            outBand = gdal.Warp(srcDSOrSrcDSTab=inputPath + band,
                                destNameOrDestDS=outputPath + band[:-4] + '_clip' + band[-4:],
                                options=options)

            outBand = None
        outbandlist = [band for band in os.listdir(outputPath) if band[-4:] == '.TIF']
        print(outbandlist)

        reply = QMessageBox.about(self, "提示", "裁剪完成")
        # self.btn_merge.setEnabled(True)


    # def btn_merge_click(self):
    #     outtif, filetype = QFileDialog.getSaveFileName(self, "保存文件", "./", "TIF文件(*.TIF);;DAT文件(*.DAT);;IMG文件(*.IMG)")
    #     NP2GDAL_CONVERSION = {
    #         "uint8": 1,
    #         "int8": 1,
    #         "uint16": 2,
    #         "int16": 3,
    #         "uint32": 4,
    #         "int32": 5,
    #         "float32": 6,
    #         "float64": 7,
    #         "complex64": 10,
    #         "complex128": 11,
    #     }
    #     tifs = [i for i in os.listdir(outputPath) if i.endswith(".TIF")]
    #     # 获取投影波段数等信息
    #     bandsNum = len(tifs)
    #     print(bandsNum)
    #     dataset = gdal.Open(os.path.join(outputPath, tifs[0]))
    #     projinfo = dataset.GetProjection()
    #     geotransform = dataset.GetGeoTransform()
    #     cols, rows = dataset.RasterXSize, dataset.RasterYSize
    #     datatype = dataset.GetRasterBand(1).ReadAsArray(0, 0, 1, 1).dtype.name
    #     gdaltype = NP2GDAL_CONVERSION[datatype]
    #     dataset = None
    #     # 创建目标文件
    #     format = "GTiff"  # tif格式
    #     format = "ENVI"  # ENVI格式
    #     driver = gdal.GetDriverByName(format)
    #     dst_ds = driver.Create(outtif, cols, rows, bandsNum, gdaltype)
    #     dst_ds.SetGeoTransform(geotransform)
    #     dst_ds.SetProjection(projinfo)
    #     # 写入文件
    #     info = set()
    #     for k in range(bandsNum):
    #         ds = gdal.Open(os.path.join(outputPath, tifs[k]))
    #         X, Y = ds.RasterXSize, ds.RasterYSize
    #         info.add("%s,%s" % (X, Y))
    #         if (len(info) != 1):
    #             dst_ds = None
    #             ds = None
    #             print("%s 列数行数不一样：%s,%s" % (tifs[k], X, Y))
    #             raise Exception("有影像行列数不一致")
    #         data = ds.GetRasterBand(1).ReadAsArray()  ##读取第一波段
    #         ds = None
    #         dst_ds.GetRasterBand(k + 1).WriteArray(data)
    #         dst_ds.GetRasterBand(k + 1).SetDescription("band_%s" % k)
    #         print("波段 %s ==> 文件 %s" % (k + 1, tifs[k]))
    #     dst_ds = None
    #     reply = QMessageBox.about(self, "提示", "合并完成")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = MyClip_Form()
    md.show()
    sys.exit(app.exec_())

# inputPath = '../Images_c1/'
# outputPath = '../Output/'
# bandList = [band for band in os.listdir(inputPath) if band[-4:]=='.TIF']
# print(bandList)
# #Shapefile of Area of Influence
# shp_clip = '../Shp/AOI_1.shp'
# for band in bandList:
#     print(outputPath + band[:-4]+'_c2'+band[-4:])
#     options = gdal.WarpOptions(cutlineDSName=shp_clip,cropToCutline=True)
#     outBand = gdal.Warp(srcDSOrSrcDSTab=inputPath + band,
#                         destNameOrDestDS=outputPath + band[:-4]+'_c2'+band[-4:],
#                         options=options)
#     outBand= None
