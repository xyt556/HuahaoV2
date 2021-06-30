# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import messagebox, filedialog,ttk
# import R_D_Image as rd
from osgeo import gdal
# import matplotlib.pyplot as plt

try:
    from skimage import filters
except ImportError:
    from skimage import filter as filters
from skimage import exposure
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
def Binarization():
    global val
    # print('wenjianlujing',img_RS)
    inpath = t1.get()
    # print(datapath)
    dataset = gdal.Open(inpath)  # rd.read_img(img_RS)
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
    # print(camera2)
    # camera_t = camera2
    # nanmean = np.nanmean(camera2)
    # camera_t[np.isnan(camera_t)] = nanmean
    # print(nanmean)
    i_min = np.nanmin(camera2)
    i_max = np.nanmax(camera2)
    print(i_max,i_min)
    camera2 = [i for i in camera2 if (i >= i_min and i <= i_max)] #i >= -1 and i <= 1
    camera2 = np.asarray(camera2)
    # plt.figure(figsize=(9, 4))
    # plt.subplot(131)
    # plt.imshow(camera, cmap='hot', interpolation='nearest')
    # plt.axis('off')

    val = filters.threshold_otsu(camera2)

    print(val)
    tval.delete(0, "end")
    tval.insert(0, val)
    return val
    # camera[camera <= val] = 0  # np.nan
    # camera[camera > val] = 1  # np.nan
    # print('二值化后最小值',np.nanmin(camera))
    # print('二值化后最大值', np.nanmax(camera))
    # # im = exposure.rescale_intensity(camera, out_range='float')
    # # im = img_as_float(im)
    # outpath = t2.get()
    # print('文件保存路径是：',outpath)
    # rd.write_img(outpath, im_proj, im_geotrans, camera)
    #
    # hist, bins_center = exposure.histogram(camera2)
    #
    # # image = [x for x in image if not pa.isnull(x)]
    #
    # # print(image)
    # # skimage OTSU算法-------------------------------
    # # thresh = threshold_otsu(image)
    # # thresh = 150
    # # image[mask] = 255
    # print(val)
    #
    # # binary = image > thresh  # >
    # # -------------------------------------------------
    # # # CV2OTSU算法
    # # thresh, binary = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
    # # # print(binary)
    # # self.Bin_Edit.setText(str(val))
    # # tval.insert('insert',val)
    #
    #
    #
    # # rd.write_img(Bin_img, im_proj, im_geotrans, binary)
    # # io.imsave("OTSU.tif",binary,plugin=None,check_contrast=True)
    # # io.show("OTSU.tif")
    # # io.imsave("OTSU.tif", binary)
    # # self.Cust_Button.setEnabled(True)
    #
    # plt.subplot(132)
    # plt.imshow(camera, cmap='gray', interpolation='nearest')
    # plt.axis('off')
    # plt.subplot(133)
    #
    # plt.plot(bins_center, hist, lw=2)
    # plt.axvline(val, color='k', ls='--')
    # plt.text(val + 0.02, 1000, 't* = ' + str(val), fontsize=12)
    # # plt.tight_layout()
    # plt.savefig("./otsu_image", dpi=600)
    # plt.show()
    #
    # # fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
    # # ax = axes.ravel()
    # # ax[0] = plt.subplot(1, 3, 1)
    # # ax[1] = plt.subplot(1, 3, 2)
    # # ax[2] = plt.subplot(1, 3, 3, sharex=ax[0], sharey=ax[0])
    # #
    # # ax[0].imshow(image, cmap=plt.cm.gray)
    # # ax[0].set_title('原始图像')
    # # ax[0].axis('off')
    # #
    # # ax[1].hist(image.ravel(), bins=256)
    # # ax[1].set_title('直方图')
    # # ax[1].axvline(thresh, color='r')
    # #
    # # ax[2].imshow(binary, cmap=plt.cm.gray)
    # # ax[2].set_title('二值化图')
    # # ax[2].axis('off')
    # #
    # # plt.show()
    # messagebox.showinfo('提示','二值化完成！')
    return
def Cust_Binarization():
    global val
    print(img_RS)
    inpath = t1.get()
    dataset = gdal.Open(inpath)  # rd.read_img(img_RS)
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
    i_min = np.nanmin(camera2)
    i_max = np.nanmax(camera2)
    print(i_max, i_min)
    camera2 = [i for i in camera2 if (i >= i_min and i <= i_max)]  # i >= -1 and i <= 1
    camera2 = np.asarray(camera2)


    # val = filters.threshold_otsu(camera2)
    # val 通过文本框获取，手动二值化
    # plt.figure(figsize=(9, 4))
    # plt.subplot(131)
    # plt.imshow(camera, cmap='hot', interpolation='nearest')
    # plt.axis('off')
    print(tval.get())

    val = float(tval.get())
    print('自定义阈值是：',val)
    # camera[camera <= val] = 0  # np.nan
    # camera[camera > val] = 1  # np.nan
    camera[camera<val]=np.nan
    camera[camera >= val] = 1
    # im = exposure.rescale_intensity(camera, out_range='float')
    # im = img_as_float(im)
    Bin_img = t2.get()
    write_img(Bin_img, im_proj, im_geotrans, camera)
    # path = t2.get()[:-4]

    # Bin_img_cust = path + '_Cust.tif'
    # print(Bin_img_cust)
    # rd.write_img(Bin_img, im_proj, im_geotrans, camera_c)

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


    # plt.subplot(132)
    # plt.imshow(camera, cmap='gray', interpolation='nearest')
    # plt.axis('off')
    # plt.subplot(133)
    #
    # plt.plot(bins_center, hist, lw=2)
    # plt.axvline(val, color='k', ls='--')
    # plt.text(val + 0.02, 1000, 't* = ' + str(val), fontsize=12)
    # # plt.tight_layout()
    # plt.savefig("./otsu_image", dpi=600)
    # plt.show()
    messagebox.showinfo('提示', '二值化完成！')


if __name__ == '__main__':
    root = tk.Tk()
    root.title('遥感指数图像二值化')
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
    l3 = tk.Label(root,text='计算阈值：',font=("宋体",10, "bold"))
    l3.grid(column=0,row=4)
    tval = tk.Entry(root)
    tval.grid(column=1,row=4)
    tval.insert(0, "0")
    b3 = tk.Button(root, text = '计算阈值',font=("宋体",10, "bold"),width = 8, height =2, command = Binarization)
    b3.grid(column=2,row=4)
    b4 = tk.Button(root, text = '二值化',font=("宋体",10, "bold"),width = 16, height =2,command = Cust_Binarization)
    b4.grid(column=1,row=6)
    root.mainloop()

