# -*- coding:utf-8 -*-
import numpy as np
# import gdal
# from osgeo import gdal
import gdal
import os
import sys
# import importlib,sys
# importlib.reload(sys)
import tkinter as tk
from tkinter import messagebox, filedialog
root = tk.Tk()
root.iconbitmap(default=".\Earth.ico")
root.withdraw() #主窗口隐藏
#修改路径
# tifDir = "H:/RS"  #tif路径 单波段
# outtif = "H:/RS/out11.dat"
tifDir = tk.filedialog.askdirectory(title='选择单波段影像所在目录')
if tifDir:
    print(type(tifDir))
    print(tifDir)
else:
    print('你没有选择任何文件夹')
    messagebox.showinfo('提示', '您未选择任何文件，程序将退出！')
    # tifs = filedialog.askopenfilenames(filetypes=[('TIF文件', '.tif'), ('TIFF', ('.py', '.TIFF'))])
    sys.exit()
outtif = tk.filedialog.asksaveasfilename(title="保存影像文件", defaultextension=".tif", filetypes=[("TIF", "TIF"),("DAT", "dat"),("TIFF", "TIFF"),("IMG", "img"),("所有文件", ".*")])
if outtif:
    print(type(outtif))
    print(outtif)
else:
    print('你没有选择任何文件')
    messagebox.showinfo('提示', '您未指定保存文件，程序将推出')
    # outtif = filedialog.asksaveasfilename(title="保存影像文件", defaultextension=".tif", filetypes=[("TIF", "TIF"),("DAT", "dat"),("TIFF", "TIFF"),("IMG", "img"),("所有文件", ".*")])
    sys.exit()
print(tifDir)
print(outtif)
NP2GDAL_CONVERSION = {
  "uint8": 1,
  "int8": 1,
  "uint16": 2,
  "int16": 3,
  "uint32": 4,
  "int32": 5,
  "float32": 6,
  "float64": 7,
  "complex64": 10,
  "complex128": 11,
}
print(os.listdir(tifDir))
tifs = [i for i in os.listdir(tifDir) if i.endswith(".TIF") or i.endswith(".tif") or i.endswith(".TIFF")]
print(tifs)
#获取投影波段数等信息
bandsNum = len(tifs)
print(bandsNum)
dataset = gdal.Open(os.path.join(tifDir,tifs[0]))
projinfo = dataset.GetProjection()
geotransform = dataset.GetGeoTransform()
cols,rows=dataset.RasterXSize,dataset.RasterYSize
datatype=dataset.GetRasterBand(1).ReadAsArray(0,0,1,1).dtype.name
gdaltype=NP2GDAL_CONVERSION[datatype]
dataset=None
#创建目标文件
format = "GTiff" #tif格式
# format = "ENVI"  # ENVI格式
# format = "TIF" # TIF格式
driver = gdal.GetDriverByName(format)
dst_ds = driver.Create(outtif,cols, rows,bandsNum, gdaltype)
dst_ds.SetGeoTransform(geotransform)
dst_ds.SetProjection(projinfo)
#写入文件
info = set()
# k = 1
for k in range(bandsNum):
    ds = gdal.Open(os.path.join(tifDir,tifs[k]))
    X,Y = ds.RasterXSize,ds.RasterYSize
    info.add("%s,%s"%(X,Y))
    if(len(info) != 1):
        dst_ds = None
        ds = None
        print("%s 列数行数不一样：%s,%s"%(tifs[k],X,Y))
        r1 = messagebox.showinfo("提示", "有影像行列数不一致")
        raise Exception("有影像行列数不一致")

    data = ds.GetRasterBand(1).ReadAsArray()    ##读取第一波段
    ds = None
    dst_ds.GetRasterBand(k+1).WriteArray(data)
    # dst_ds.GetRasterBand(k+1).SetDescription("band_%s"%k)
    dst_ds.GetRasterBand(k + 1).SetDescription(tifs[k])
    print("波段 %s ==> 文件 %s"%(k+1,tifs[k]))
dst_ds = None
r2 = messagebox.showinfo("提示", "完成")