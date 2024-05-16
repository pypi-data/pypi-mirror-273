#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/04/23 15:10:20
@Author  :   Flemyng 
@Desc    :   GeoTiff kit for reading ,writing tiff file and ect.
'''

import os
from pathlib import Path
from typing import Tuple, Optional, Union

from osgeo import gdal
import numpy as np


def read_geo(
    file_path: Union[Path, str]
) -> Tuple[Optional[np.ndarray], Optional[tuple], Optional[str]]:
    '''
    Read tif file

    param: file_path: Path or str, tif file path
    return: data: np.ndarray [band, width, height], geotransform: tuple, projection: str
    '''
    # 如果输入是 Path，将其转换为 str 对象
    if isinstance(file_path, Path):
        file_path = str(file_path)

    ds = gdal.Open(file_path)
    if ds is None:
        print(f"Cannot open {file_path}")
        return None, None, None

    width = ds.RasterXSize
    height = ds.RasterYSize
    data = ds.ReadAsArray(0, 0, width, height)
    geotransform = ds.GetGeoTransform()
    projection = ds.GetProjection()

    return data, geotransform, projection


def read(
    file_path: Union[Path, str]
) -> Optional[np.ndarray]:
    '''
    Read tif file as array

    param: file: Path, tif file path
    return: data: np.ndarray
    '''
    # 如果输入是 Path，将其转换为 str 对象
    if isinstance(file_path, Path):
        file_path = str(file_path)

    data_set = gdal.Open(file_path, gdal.GA_ReadOnly)
    if data_set is None:
        print(f"Cannot open {file_path}")
        return None

    img_width = data_set.RasterXSize
    img_height = data_set.RasterYSize
    img_data = data_set.ReadAsArray(0, 0, img_width, img_height)

    return img_data


def save_without_memory_mapping(
    save_path: Union[Path, str],
    data: np.ndarray,
    geotransform: tuple,
    projection: str,
    output_dtype = gdal.GDT_Float32,
) -> None:
    '''
    Save tif file without memory mapping

    param: save_path: Path, tif file save path
    param: data: np.ndarray, tif file data
    param: geotransform: tuple, tif file geotransform
    param: projection: str, tif file projection
    param: output_dtype: gdal.GDT_Float32, tif file data type
    '''
    # 如果输入是 Path，将其转换为 str 对象
    if isinstance(save_path, Path):
        save_path = str(save_path)

    im_bands = 1 if len(data.shape) == 2 else data.shape[0]
    im_height, im_width = data.shape[-2:]

    options = ["COMPRESS=LZW"]  # 使用LZW压缩
    driver = gdal.GetDriverByName("GTiff")
    new_dataset = driver.Create(
        save_path,
        im_width, im_height, im_bands,
        output_dtype, options=options
    )
    new_dataset.SetGeoTransform(geotransform)
    new_dataset.SetProjection(projection)

    if im_bands == 1:
        new_dataset.GetRasterBand(1).WriteArray(data)
    else:
        for i in range(im_bands):
            new_dataset.GetRasterBand(i + 1).WriteArray(data[i])

    new_dataset = None  # 确保数据被写入并释放资源
    driver = None


def save(
    save_path: Union[Path, str],
    data: np.ndarray,
    geotransform: tuple,
    projection: str,
    output_dtype=gdal.GDT_Float32
) -> None:
    '''
    Save tif file with memory mapping

    param: save_path: Path, tif file save path
    param: data: np.ndarray, tif file data
    param: geotransform: tuple, tif file geotransform
    param: projection: str, tif file projection
    param: output_dtype: gdal.GDT_Float32, tif file data type
    '''
    # 如果输入是 Path，将其转换为 str 对象
    if isinstance(save_path, Path):
        save_path = str(save_path)

    im_bands = 1 if len(data.shape) == 2 else data.shape[0]
    im_height, im_width = data.shape[-2:]

    # 创建内存数据集
    mem_driver = gdal.GetDriverByName('MEM')
    mem_dataset = mem_driver.Create('', im_width, im_height, im_bands, output_dtype)

    # 设置地理变换和投影
    mem_dataset.SetGeoTransform(geotransform)
    mem_dataset.SetProjection(projection)

    # 写入数据到内存数据集
    for i in range(im_bands):
        mem_dataset.GetRasterBand(i + 1).WriteArray(data[i])

    # 将内存数据集保存到文件
    file_driver = gdal.GetDriverByName('GTiff')
    file_driver.CreateCopy(save_path, mem_dataset, 0, ["COMPRESS=LZW"])

    mem_dataset = None  # 释放内存数据集资源


def save_array(
    save_path: Union[Path, str],
    data: np.ndarray,
    output_dtype = gdal.GDT_Float32,
) -> None:
    '''
    Save tif file from array

    param: save_path: Path, tif file save path
    param: data: np.ndarray, tif file data
    param: output_dtype: gdal.GDT_Float32, tif file data type
    '''
    # 如果输入是 Path，将其转换为 str 对象
    if isinstance(save_path, Path):
        save_path = str(save_path)

    im_bands = 1 if len(data.shape) == 2 else data.shape[0]
    im_height, im_width = data.shape[-2:]

    driver = gdal.GetDriverByName("GTiff")
    new_dataset = driver.Create(save_path, im_width, im_height, im_bands, output_dtype)

    if im_bands == 1:
        new_dataset.GetRasterBand(1).WriteArray(data)
    else:
        for i in range(im_bands):
            new_dataset.GetRasterBand(i + 1).WriteArray(data[i])

    new_dataset = None
    driver = None


def hsi_to_rgb(
    hsi_data: np.ndarray,
    r_band_index: int,
    g_band_index: int,
    b_band_index: int,
) -> np.ndarray:
    """
    Convert hyperspectral image data to RGB image data.

    param: hsi_data: np.ndarray: The hyperspectral image data, default shape is [band, width, height].
    param: r_band_index: int: The index of the red band.
    param: g_band_index: int: The index of the green band.
    param: b_band_index: int: The index of the blue band.
    return: np.ndarray: The RGB image data, shape is [width, height, 3(r, g, b)].
    """
    # Extract the RGB bands
    rgb_ = hsi_data[[r_band_index, g_band_index, b_band_index], :, :]

    # Clean data
    rgb_ = np.nan_to_num(rgb_)
    rgb_[rgb_ < 0] = 0

    # Normalize data
    max_value = (np.mean(rgb_[1]) + 3 * np.std(rgb_[1])) * 1.5
    min_value = np.min(rgb_)
    print(f'max: {max_value:.2f}, min: {min_value:.2f}')
    rgb_ = (rgb_ - min_value) / (max_value - min_value)
    rgb_ = np.clip(rgb_, 0, 1)

    # Gamma correction (default gamma is 1/2.2)
    rgb_ = rgb_ ** 0.6

    # Turn background to white
    rgb_[rgb_ == 0] = 1

    return np.moveaxis(rgb_, 0, -1)


def make_format_coord(
    geotransform_: tuple
) -> callable(str):
    '''
    Make format_coord function

    param: geotransform_: tuple, geotransform of geotiff
    return: format_coord: callable(str), format_coord function
    '''
    def format_coord(x, y):
        x_origin = geotransform_[0]
        y_origin = geotransform_[3]
        x_pixel = geotransform_[1]
        y_pixel = geotransform_[5]

        lon = x_pixel * x + x_origin
        lat = y_pixel * y + y_origin
        return f'x={lon:.3f}, y={lat:.3f}'

    return format_coord


def set_background_to_zero(
    data: np.ndarray,
    start_band: int,
    end_band: int,
):
    """
    将在指定波段范围内数值之和小于0的像素点在所有波段设置为0值。

    Param: data: np.ndarray, 输入的多波段数据
    Param: start_band: int, 起始波段索引
    Param: end_band: int, 结束波段索引
    Return: np.ndarray, 处理后的多波段数据
    """
    # 检查波段索引是否有效
    if start_band < 0 or end_band >= data.shape[0]:
        raise ValueError("波段索引超出数组范围。")

    # 选择指定的波段范围
    selected_bands = data[start_band:end_band + 1]

    # 计算这些波段的数值之和
    sum_over_bands = np.sum(selected_bands, axis=0)

    # 判断哪些像素点的和小于0
    mask = sum_over_bands < 0

    # 对于和小于0的像素点，将所有波段的值设置为0
    data[:, mask] = 0

    return data

# 使用示例：
# data = ... # 您的NumPy数组
# modified_data = set_background_to_zero(data, 90, 100)


def set_nodata(input_file: list, number: int=0) -> None:
    """
    将图像中的某个number值设置为nodata。

    Param: input_file: str, 输入的tif图像路径
    Param: number: int, 需要设置为nodata的数值
    """
    # 打开输入文件
    ds = gdal.Open(input_file, gdal.GA_Update)
    if ds is None:
        print(f"无法打开文件: {input_file}")
        return

    # 对于每个波段，设置指定数值为nodata值
    try:
        for i in range(1, ds.RasterCount + 1):
            band = ds.GetRasterBand(i)
            band.SetNoDataValue(number)
            band.FlushCache()
    finally:
        ds = None  # 确保关闭数据集


def merge(
    input_files: list,
    output_file: Path,
) -> None:
    """
    将多个tif图像合并为一个tif图像。(这个图像的背景必须是nodata, set_nodata)
    
    Param: input_files: list, 输入的tif图像路径列表
    Param: output_file: Path, 输出的tif图像路径
    """
    # 处理每一个输入图像，将指定值设置为nodata
    for input_file in input_files:
        set_nodata(input_file, 0)

    # 创建一个虚拟数据集（VRT）
    vrt_filename = str(output_file.parent / 'temp.vrt')
    vrt = gdal.BuildVRT(vrt_filename, input_files)
    if vrt is None:
        print("无法创建虚拟数据集 (VRT)")
        return

    try:
        # 使用Translate方法将VRT转换为TIFF格式
        gdal.Translate(str(output_file), vrt, format='GTiff')
    finally:
        # 清理资源
        vrt = None

    # 删除VRT文件
    os.remove(vrt_filename)
    print(f"合并完成: {output_file}")


if __name__ == '__main__':
    # 测试
    # input_files_pathes = [
    #     '/Volumes/2023HSI/raw/2023_07_17/5ref/1_corr_elm.tif',
    #     '/Volumes/2023HSI/raw/2023_07_17/5ref/3_corr_elm.tif'
    # ]
    # output_path = Path('/Volumes/2023HSI/raw/2023_07_17/5ref/1and3_corr_elm.tif')

    # # 合并图像
    # merge(input_files_pathes, output_path)

    tif_path = Path('/Volumes/2023HSI/raw/2023_07_17/5ref/1and3_corr_elm.tif')
    data, geotransform, projection = read(tif_path)
    save(tif_path.parent / 'test.tif', data, geotransform, projection)
