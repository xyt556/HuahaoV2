# 读遥感数据
# import gdal
from sklearn import preprocessing
from osgeo import gdal, gdal_array
import numpy as np

def __init__(img_path): # , res_save_dir
    img_width, img_height, img = read_img(img_path)
    global deno_bias
    deno_bias = 0.00001  # 分母偏置，防止除0
    # self.res_save_dir = res_save_dir
# 读取图像文件
def read_img(filename):
    data = gdal.Open(filename)  # 打开文件
    # Does the raster have a description or metadata?
    desc = data.GetDescription()
    metadata = data.GetMetadata()  # 得到的元数据
    print('Raster description: {desc}'.format(desc=desc))
    print('Raster metadata:')
    print(metadata)  # {'AREA_OR_POINT': 'Area'}
    num_bands = data.RasterCount  # 波段数
    print("波段个数：", num_bands)
    im_width = data.RasterXSize  # 读取图像列数
    im_height = data.RasterYSize  # 读取图像行数
    print('Image size is: {r} rows x {c} columns\n'.format(r=im_height, c=im_width))
    im_geotrans = data.GetGeoTransform()


    # 仿射矩阵，左上角像素的大地坐标和像素分辨率。
    # 共有六个参数，分表代表左上角x坐标；东西方向上图像的分辨率；如果北边朝上，地图的旋转角度，0表示图像的行与x轴平行；左上角y坐标；
    # 如果北边朝上，地图的旋转角度，0表示图像的列与y轴平行；南北方向上地图的分辨率。
    im_proj = data.GetProjection()  # 地图投影信息
    im_data = data.ReadAsArray(0, 0, im_width, im_height)  # 此处读取整张图像
    # print(type(im_data))
    # ReadAsArray(<xoff>, <yoff>, <xsize>, <ysize>)
    # 读出从(xoff,yoff)开始，大小为(xsize,ysize)的矩阵。


    # del data  # 释放内存，如果不释放，在arcgis，envi中打开该图像时会显示文件被占用
    return im_proj, im_geotrans, im_data
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
def normlize1(img):
    arr = np.array(img)

    arr = np.array(arr, dtype=float)
    arr[arr == -9999] = np.nan



    # arr[arr == -9999] = np.nan
    # return preprocessing.MaxAbsScaler().fit_transform(arr) #归一化【-1,1】

    # 归一化【0,1】
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(arr)
    scaler.data_max_
    return scaler.transform(arr)
    # min = np.nanmin(arr)
    # print(min)
    # print(arr.min())
    # max = np.nanmax(arr)
    #
    # return (arr - min) / (max - min)
def get_ndvi(img):
    ndvi = (img[4] - img[3])/(img[4] + img[3])
    return ndvi
# 高分数据计算指数
def get_ndvi_gf(img):
    ndvi_gf = (img[3] - img[2]) / (img[3] + img[2])
    return ndvi_gf
def get_ndwi(img):
    ndwi = (img[2] - img[4]) / (img[2] + img[4])
    return ndwi
# 高分数据计算指数
def get_ndwi_gf(img):
    ndwi_gf = (img[1] - img[3]) / (img[1] + img[3])
    return ndwi_gf

def get_temperature(self):
    """获取热度指标"""
    gain = 3.20107  # landsat5 第6波段的增益值
    bias = 0.25994  # 第6波段的偏置值

    K1 = 606.09
    K2 = 1282.71
    _lambda = 11.45
    _rho = 1.438e10 - 2
    _epsilon = 0.96  # 比辐射率

    DN = self.img[4] * 299 / 1000 + self.img[3] * 587 / 1000 + self.img[2] * 114 / 1000  # 获取象元灰度值

    L6 = gain * DN + bias
    T = K2 / np.log(K1 / L6 + 1)
    LST = T / (1 + (_lambda * T / _rho) * np.log(_epsilon))

    return LST


def get_wet_degree(img):
    """获取湿度指标"""
    wet = 0.2626 * img[0] + 0.2141 * img[1] + 0.0926 * img[2] + \
          0.0656 * img[3] - 0.7629 * img[4] - 0.5388 * img[5]
    # wet = 0.1511 * img[1] + 0.193 * img[2] + 0.3283 * img[3] + \
    #     0.3407 * img[4]  - 0.7117 * img[5] - 0.4559 * img[6]

    return wet
def get_green_degree(img):
    """获取绿度指标"""
    return (img[3] - img[2]) / (img[3] + img[2] + deno_bias)

def get_dryness_degree(img):
    """获取干度指标"""
    # for Landsat 8
    deno_bias = 0.00001  # 分母偏置，防止除0
    band6_plus_band4 = img[5] + img[3]
    band5_plus_band2 = img[4] + img[1]

    SI = (band6_plus_band4 - band5_plus_band2) / (band6_plus_band4 + band5_plus_band2 + deno_bias)
    left_expr = 2 * img[5] / (img[5] + img[4] + deno_bias)
    right_expr = img[4] / (img[4] + img[3] + deno_bias) + \
                 img[2] / (img[2] + img[5] + deno_bias)
    IBI = (left_expr - right_expr) / (left_expr + right_expr + deno_bias)
    NDBSI = (IBI + SI) / 2
    return NDBSI
