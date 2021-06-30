# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import messagebox, filedialog,ttk
# import R_D_Image as rd
from osgeo import gdal
# import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy as np
# import sys
# Write file
def write_img(filename, im_proj, im_geotrans, im_data):
    # filename-创建的新影像
    # im_geotrans,im_proj该影像的参数，im_data，被写的影像
    # 写文件，以写成tiff为例
    # gdal数据类型包括
    # gdal.GDT_Byte,
    # gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
    # gdal.GDT_Float32, gdal.GDT_Float64

    # 判断栅格数据的类型
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:  # len(im_data.shape)表示矩阵的维数
        im_bands, im_height, im_width = im_data.shape  # （维数，行数，列数）
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape  # 一维矩阵

    #         创建文件
    driver = gdal.GetDriverByName('GTiff')  # 数据类型必须有，因为要计算需要多大内存空间
    data = driver.Create(filename, im_width, im_height, im_bands, datatype)
    data.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
    data.SetProjection(im_proj)  # 写入投影
    if im_bands == 1:
        data.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
    else:
        for i in range(im_bands):
            data.GetRasterBand(i + 1).WriteArray(im_data[i])
    del data


def OpenData():
    global img_RS
    img_RS = filedialog.askopenfilename(title="打开遥感指数图像", defaultextension=".tif",
                                                filetypes=[("TIF", "TIF"), ("TIFF", "TIFF"), ("DAT", "dat"),
                                                           ("IMG", "img"), ("所有文件", ".*")])
    if img_RS:
        print(type(img_RS))
        print(img_RS)
    else:
        print('你没有选择任何文件')
        messagebox.showinfo('提示', '请选择文件')
        img_RS = filedialog.askopenfilename(title="保存二值化图像", defaultextension=".tif",
                                                filetypes=[("TIF", "TIF"), ("TIFF", "TIFF"), ("DAT", "dat"),
                                                           ("IMG", "img"), ("所有文件", ".*")])
    # t1.insert('insert',img_RS)
    # t1.textvariable = img_RS
    t1.insert(0, "请选择文件")
    t1.delete(0, "end")
    t1.insert(0, img_RS)

    return img_RS
def SaveData():
    global Bin_img
    Bin_img = tk.filedialog.asksaveasfilename(title="保存二值化图像", defaultextension=".tif",
                                                filetypes=[("TIF", "TIF"), ("TIFF", "TIFF"), ("DAT", "dat"),
                                                           ("IMG", "img"), ("所有文件", ".*")])
    if Bin_img:
        print(type(Bin_img))
        print(Bin_img)
    else:
        print('你没有选择任何文件')
        messagebox.showinfo('提示', '请选择文件')
        img_RS = filedialog.asksaveasfilename(title="保存二值化图像", defaultextension=".tif",
                                                filetypes=[("TIF", "TIF"), ("TIFF", "TIFF"), ("DAT", "dat"),
                                                           ("IMG", "img"), ("所有文件", ".*")])
    # t2.insert('insert',Bin_img)
    t2.delete(0, "end")
    t2.insert(0, Bin_img)
    return Bin_img
# 归一化处理
def normlize(img):
    arr = np.array(img)
    arr = np.array(arr, dtype=float)
    arr[arr == -9999] = np.nan

    return preprocessing.MaxAbsScaler().fit_transform(arr) #归一化【-1,1】

    # # 归一化【0,1】
    # scaler = preprocessing.MinMaxScaler()
    # scaler.fit(arr)
    # scaler.data_max_
    # return scaler.transform(arr)
    # return (arr - arr.min()) / (arr.max() - arr.min())
def normlize1():
    inpath = t1.get()
    dataset = gdal.Open(inpath)  # rd.read_img(img_RS)
    # image = io.imread("./data/ndwi.tif" ,as_gray= False)#data.camera()
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数

    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息
    arr = np.array(dataset.GetRasterBand(1).ReadAsArray())

    arr = np.array(arr, dtype=float)
    arr[arr == -9999] = np.nan
    # arr[arr == -9999] = np.nan
    # return preprocessing.MaxAbsScaler().fit_transform(arr) #归一化【-1,1】

    # 归一化【0,1】
    # Method 1
    # scaler = preprocessing.MinMaxScaler()
    # scaler.fit(arr)
    # scaler.data_max_
    # Bin_img = t2.get()
    # write_img(Bin_img, im_proj, im_geotrans, scaler.transform(arr))
    # # return scaler.transform(arr)

    # Method 2
    min = np.nanmin(arr)
    print(min)
    print(arr.min())
    max = np.nanmax(arr)
    Bin_img = t2.get()
    write_img(Bin_img, im_proj, im_geotrans, (arr - min) / (max - min))

    # return (arr - min) / (max - min)
    messagebox.showinfo('提示', '二值化完成！')


if __name__ == '__main__':
    root = tk.Tk()
    root.title('指标因子（灰度图像）归一化')
    root.iconbitmap(default=r"./Earth.ico")
    sw = root.winfo_screenwidth()
    # 得到屏幕宽度
    sh = root.winfo_screenheight()
    # 得到屏幕高度
    ww = 580
    wh = 150
    # 窗口宽高为100
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    # root.geometry("600x180+10+20")
    l1 = tk.Label(root,text='请选择遥感指数图像：',font=("宋体",10, "bold"))
    l1.grid(column=0,row=3)
    t1 = tk.Entry(root, width = 50)
    t1.grid(column=1,row=3)
    t1.insert(0, "请选择文件")
    b1 = tk.Button(root, text = '打开',font=("宋体",10, "bold"),width = 8, height =2, command = OpenData)
    b1.grid(column=2,row=3)

    l2 = tk.Label(root,text='请保存二值化图像：',font=("宋体",10, "bold"))
    l2.grid(column=0,row=5)
    t2 = tk.Entry(root, width = 50)
    t2.grid(column=1,row=5)
    t2.insert(0, "请保存文件")
    b2 = tk.Button(root, text = '保存',font=("宋体",10, "bold"),width = 8, height =2, command = SaveData)
    b2.grid(column=2,row=5)

    b4 = tk.Button(root, text = '归一化',font=("宋体",10, "bold"),width = 16, height =2,command = normlize1)
    b4.grid(column=1,row=6)
    root.mainloop()

