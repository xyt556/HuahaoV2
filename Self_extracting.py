# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 14:10:21 2020

@author: Yantao XI
"""

import tarfile    #网上下的Landsat数据都是压缩包(.tar.gz)，因此需调用tarfile包（其他类似的解压缩包也可以）
import tkinter as tk
from tkinter import messagebox, filedialog
import sys
root = tk.Tk()
root.iconbitmap(default=r"./Earth.ico")
root.withdraw() #主窗口隐藏
data = tk.filedialog.askopenfilename(title="打开压缩文件", filetypes=[("gz", "gz"),("所有文件", ".*")])
if data:
    print(type(data))
    print(data)
else:
    print('你没有选择任何文件')
    messagebox.showinfo('提示', '您未选择任何文件，程序将退出!')
    # tifs = filedialog.askopenfilenames(filetypes=[('TIF文件', '.tif'), ('TIFF', ('.py', '.TIFF'))])
    sys.exit()
dir = tk.filedialog.askdirectory(title="保存路径")
if dir:
    print(type(dir))
    print(dir)
else:
    print('你没有选择任何文件夹')
    messagebox.showinfo('提示', '您未指定任何文件夹，程序将退出!')
    # tifs = filedialog.askopenfilenames(filetypes=[('TIF文件', '.tif'), ('TIFF', ('.py', '.TIFF'))])
    sys.exit()

print(data)
# folder = 'F:/RS/'    #存放数据的文件夹
# indata = 'LC08_L1TP_127041_20190407_20190422_01_T1.tar.gz'    #需被解压的影像压缩包
tar = tarfile.open(data) # 打开影像压缩包
names = tar.getnames()    #获取影像压缩包里包含的文件名
print(names)
for name in names:
   tar.extract(name,path=dir) #开始解压（这里解压的是所有文件，也可以只解压其中的某一个文件，指定文件名就好）
tar.close()
print("OK")
# reply = QMessageBox.about("提示", "合并完成")
r = messagebox.showinfo("提示", "解压缩完成")