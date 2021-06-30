# import numpy as np
import matplotlib.pyplot as plt #abc
# import gdal
import R_D_Image as rd
# import cv2
# from multispectral import Indices
from spectral_indices import Indices

import tkinter as tk
from tkinter import messagebox, filedialog,ttk


index_name = ''
def read_file():
    global data,m_proj, im_geotrans, im_data
    data = tk.filedialog.askopenfilename(title="打开影像文件", filetypes=[("TIF", "tif"),("TIFF", "tiff"),("ENVI dat", "dat"),("所有文件", ".*")])
    m_proj, im_geotrans, im_data = rd.read_img(data)
    f, ax = plt.subplots(3, 3)
    ax[0][0].imshow(im_data[0])
    ax[0][0].set_title('波段1')
    ax[0][1].imshow(im_data[1])
    ax[0][1].set_title('波段2')
    ax[0][2].imshow(im_data[2])
    ax[0][2].set_title('波段3')
    ax[1][0].imshow(im_data[3])
    ax[1][0].set_title('波段4')
    ax[1][1].imshow(im_data[4])
    ax[1][1].set_title('波段5')
    ax[1][2].imshow(im_data[5])
    ax[1][2].set_title('波段6')
    ax[2][0].imshow(im_data[6])
    ax[2][0].set_title('波段7')
    ax[2][1].imshow(im_data[7])
    ax[2][1].set_title('波段8')
    ax[2][2].imshow(im_data[8])
    ax[2][2].set_title('波段9')
    plt.show()
    return data,m_proj, im_geotrans, im_data
def save_dir():
    global dir
    dir = tk.filedialog.askdirectory(title="保存路径")
    print(dir)
    return dir
def meg():
    r=messagebox('ss','ff')

'''
def cac_index():
    indices_dict = Indices(im_data)
    print(index_name)
    print(im_data)
    print(dir)

    # Get the Kaolinite index
    index = indices_dict.get(index_name)

    print(index)
    # vi_img =
    # Plot the Kaolinite map
    # plt.imshow(im_data[2],cmap= 'gray')
    # plt.imshow(vi[0], cmp = )
    # plt.subplot(1,3,1)

    # plt.imshow(im_data[8])
    # plt.colorbar(shrink=.3)
    # plt.title('原始影像')
    # plt.subplot(1,3,2)
    plt.imshow(index[0], cmap='hot')
    plt.colorbar(shrink=.3)
    plt.title('遥感指数')
    plt.show()

    rd.write_img(dir + index_name + '.tif', im_proj=m_proj, im_geotrans=im_geotrans, im_data=index[0])
    # The actual values in the dict are function objects
    # A particular index can alternatively be computed by
    # extracting the function from the dict and calling it
    get_kaolinite_idx = indices_dict["Kaolinite"]
    kaolinite = get_kaolinite_idx()
    print('计算完成！')
    r = messagebox.showinfo("提示", "计算完成")
'''
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串

# Simulate a 9-layer ASTER image with 3 VNIR bands and 6 SWIR bands
# img = np.random.randn(9, 1000, 1000) # (n_bands, height, width)
# img = gdal.Open(r'H:\Aster\index\ASTER_VNIR-SWIR_Atm_PCA.dat')
# m_proj, im_geotrans, im_data = rd.read_img(r'H:\Aster\aster1-9_clip.dat')
root = tk.Tk()
root.title('遥感指数计算_Aster')
root.iconbitmap(default=r"./Earth.ico")
sw = root.winfo_screenwidth()
#得到屏幕宽度
sh = root.winfo_screenheight()
#得到屏幕高度
ww = 500
wh = 200
#窗口宽高为100
x = (sw-ww) / 2
y = (sh-wh) / 2
root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
# root.geometry("500x200+10+20")
# root.withdraw() #主窗口隐藏
# 第6步，创建并放置两个按钮分别触发两种情况, command=insert_point  , width=6,
#                height=3

b1 = tk.Button(root, text='打开影像', command=read_file).grid(column=0,row=2)

# b1.pack(padx = 5,pady = 5)
b2 = tk.Button(root, text='保存目录', command=save_dir).grid(column=1,row=2)
# b2.pack(padx = 5,pady = 5)

w = tk.Label(root,text='请选择遥感指数：',font=("黑体",10, "bold"))
w.grid(column=0,row=3)

# 第一个复选框
cmb1 = ttk.Combobox(root)
# cmb1.pack(side = 'left',padx = 5,pady = 5)
# 设置下拉菜单中的值
cmb1['value'] = ('VI','NDVI','STVI','Ferric_iron','Ferrous_iron_1')
cmb1.grid(column = 0,row=4)
# 设置默认值，即默认下拉框中的内容
cmb1.current(1)
# 默认值中的内容为索引，从0开始
# 第二个复选框
cmb2 = ttk.Combobox(root)
# cmb2.pack(side = 'left',padx = 5,pady = 5)
# 设置下拉菜单中的值
cmb2['value'] = ('AlOH','Laterite','Alunite','CCE','Clay_1','Clay_2','Kaolinitic','Kaolin_group',
                 'Kaolinite','Muscovite','OH_1','OH_2','OH_3','PHI','AKP','Amphibole','Calcite'
                 'Dolomite','MgOH_group','MgOH_1','MgOH_2')
cmb2.grid(column = 1,row=4)
# 设置默认值，即默认下拉框中的内容
cmb2.current(1)
# 默认值中的内容为索引，从0开始
# 第3个复选框
cmb3 = ttk.Combobox(root)
# cmb3.pack(side = 'left',padx = 5,pady = 5)
# 设置下拉菜单中的值
cmb3['value'] = ('RDB6','RDB8','Ferrous_iron_2','Ferric_oxide','Gossan',
                 'Opaque_index','Silicates','Burn_index','Salinity')
cmb3.grid(column = 2,row=4)
# 设置默认值，即默认下拉框中的内容
cmb3.current(2)
# 默认值中的内容为索引，从0开始

label1 = tk.Label(root,
                 text = '操作说明：请首先打开合成后的9个波段的Aster（包括可见光、近红外及中红外波段。'
                        '共计9个波段，然后设定遥感指数保存的路径。分别通过下拉框选择指数，即可计算完成并保存。',
                 # bg = 'red',
                 width = 50,
                 height = 3,
                 # relief = 'SUNKEN'
                 wraplength = 420,
                 anchor = 'w'
                 # singleLine = 'false'

                 # justify = 'LEFT'
                 )
label1.wraplength = 50
label1.grid(columnspan = 4,row=10)


# text = tk.Text(root, width=20, height=5)
# # text.insert('操作说明：请首先打开合成后的9个波段的Aster（包括可见光、近红外及中红外波段。共计9个波段，然后设定遥感指数保存的路径。分别通过下拉框选择指数，即可计算完成并保存。')
# cmb3.grid(columnspan = 2,row=5)
def func1(event):
    # print(cmb1.get())
    plt.cla()
    index_name = cmb1.get()
    indices_dict = Indices(im_data)
    print(index_name)
    print(im_data)
    print(dir)

    # Get the Kaolinite index
    index = indices_dict.get(index_name)

    print(index)
    print('计算完成！')
    rd.write_img(dir + '/' + index_name + '.tif', im_proj=m_proj, im_geotrans=im_geotrans, im_data=index[0])
    r = messagebox.showinfo("提示", "计算完成")

    plt.imshow(index[0], cmap='hot')
    plt.colorbar(shrink=.3)
    plt.title('遥感指数:' + index_name)
    plt.show()

    # The actual values in the dict are function objects
    # A particular index can alternatively be computed by
    # extracting the function from the dict and calling it
    # get_kaolinite_idx = indices_dict["Kaolinite"]
    # kaolinite = get_kaolinite_idx()

    return index_name
    # cac_index()
cmb1.bind("<<ComboboxSelected>>",func1)

def func2(event):
    plt.cla()
    print(cmb2.get())
    index_name = cmb2.get()

    indices_dict = Indices(im_data)

    print(index_name)
    print(im_data)
    print(dir)

    # Get the Kaolinite index
    index = indices_dict.get(index_name)

    print(index)
    print('计算完成！')
    rd.write_img(dir + '/' + index_name + '.tif', im_proj=m_proj, im_geotrans=im_geotrans, im_data=index[0])
    r = messagebox.showinfo("提示", "计算完成")
    plt.imshow(index[0], cmap='hot')
    plt.colorbar(shrink=.3)
    plt.title('遥感指数:' + index_name)
    plt.show()


    # The actual values in the dict are function objects
    # A particular index can alternatively be computed by
    # extracting the function from the dict and calling it
    # get_kaolinite_idx = indices_dict["Kaolinite"]
    # kaolinite = get_kaolinite_idx()


    return index_name
    # cac_index()
cmb2.bind("<<ComboboxSelected>>",func2)

def func3(event):
    plt.cla()
    print(cmb3.get())
    index_name = cmb3.get()
    indices_dict = Indices(im_data)
    print(index_name)
    print(im_data)
    print(dir)

    # Get the Kaolinite index
    index = indices_dict.get(index_name)

    print(index)
    print('计算完成！')
    rd.write_img(dir + '/' + index_name + '.tif', im_proj=m_proj, im_geotrans=im_geotrans, im_data=index[0])
    r = messagebox.showinfo("提示", "计算完成")

    plt.imshow(index[0], cmap='hot')
    plt.colorbar(shrink=.3)
    plt.title('遥感指数:' + index_name)
    plt.show()


    # The actual values in the dict are function objects
    # A particular index can alternatively be computed by
    # extracting the function from the dict and calling it
    # get_kaolinite_idx = indices_dict["Kaolinite"]
    # kaolinite = get_kaolinite_idx()

    return index_name
    # cac_index()
cmb3.bind("<<ComboboxSelected>>",func3)

# b3 = tk.Button(root, text='计算', command=cac_index)
# b3.pack()

root.mainloop()


