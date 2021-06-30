from tkinter import Tk ,filedialog, messagebox
from osgeo import gdal
import sys
root=Tk()
root.iconbitmap(default=r".\Earth.ico")
root.withdraw()
# 读入单波段TIF文件
tifs = filedialog.askopenfilenames(filetypes=[('TIF文件', '.tif'),('TIFF',('.py','.TIFF'))])
if tifs:
    print(type(tifs))
    print(tifs)
else:
    print('你没有选择任何文件')
    messagebox.showinfo('提示', '您未选择任何文件，程序将退出！')
    # tifs = filedialog.askopenfilenames(filetypes=[('TIF文件', '.tif'), ('TIFF', ('.py', '.TIFF'))])
    sys.exit()
# 保存多波段文件，返回一个元组数据类型，是文件列表
outtif = filedialog.asksaveasfilename(title="保存影像文件", defaultextension=".tif", filetypes=[("TIF", "TIF"),("DAT", "dat"),("TIFF", "TIFF"),("IMG", "img"),("所有文件", ".*")])
if outtif:
    print(type(outtif))
    print(outtif)
else:
    print('你没有选择任何文件')
    messagebox.showinfo('提示', '您未指定保存文件，程序将推出')
    # outtif = filedialog.asksaveasfilename(title="保存影像文件", defaultextension=".tif", filetypes=[("TIF", "TIF"),("DAT", "dat"),("TIFF", "TIFF"),("IMG", "img"),("所有文件", ".*")])
    sys.exit()

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
# tifs = [i for i in outtif] # if i.endswith(".TIF")
print(tifs[0])
# tifl = list(tifs)
# tifl = list(tifs,',')
# 获取投影波段数等信息
bandsNum = len(tifs)
print(bandsNum)
dataset = gdal.Open(tifs[0])
projinfo = dataset.GetProjection()
geotransform = dataset.GetGeoTransform()
cols, rows = dataset.RasterXSize, dataset.RasterYSize
datatype = dataset.GetRasterBand(1).ReadAsArray(0, 0, 1, 1).dtype.name
gdaltype = NP2GDAL_CONVERSION[datatype]
dataset = None
# 创建目标文件
format = "GTiff"  # tif格式
# format = "ENVI"  # ENVI格式
driver = gdal.GetDriverByName(format)
dst_ds = driver.Create(outtif, cols, rows, bandsNum, gdaltype)
dst_ds.SetGeoTransform(geotransform)
dst_ds.SetProjection(projinfo)
# 写入文件
info = set()
for k in range(bandsNum):
    ds = gdal.Open(tifs[k])
    X, Y = ds.RasterXSize, ds.RasterYSize
    info.add("%s,%s" % (X, Y))
    if (len(info) != 1):
        dst_ds = None
        ds = None
        print("%s 列数行数不一样：%s,%s" % (tifs[k], X, Y))
        raise Exception("有影像行列数不一致")
    data = ds.GetRasterBand(1).ReadAsArray()  ##读取第一波段
    ds = None
    dst_ds.GetRasterBand(k + 1).WriteArray(data)
    dst_ds.GetRasterBand(k + 1).SetDescription("band_%s" % k)
    print("波段 %s ==> 文件 %s" % (k + 1, tifs[k]))
dst_ds = None
messagebox.showinfo('提示','合成完成！')