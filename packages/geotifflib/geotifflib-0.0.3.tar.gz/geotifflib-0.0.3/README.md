# geotifflib

基于GDAL，对GeoTiff文件进行读写等操作。
GeoTiffLib primarily offers a set of utility functions for reading, saving, and processing GeoTIFF image files.

## 安装

由于使用pip安装GDAL报错，因此安装此包之前需要**使用conda安装GDAL**：

```sh
conda install GDAL
```

安装GDAL完成之后再安装本包：

```sh
pip install geotifflib
```

## 使用

主要包含了读、写两类函数。

### read()

根据文件路径读取GeoTiff数据、地理变换和投影。

输入：

1. 文件路径（Path or str）

返回：

1. tiff的数据矩阵（np.array）：shape = [波段，宽，长]

### read_geo()

根据文件路径读取GeoTiff数据形状、地理变换和投影。

输入：

1. 文件路径（Path or str）

返回：

1. tiff的数据矩阵（np.array）：shape = [波段，宽，长]
2. geotransform: tuple
3. projection: str

### save()

保存GeoTiff数据、地理变换和投影。

输入：

1. 保存路径（Path or str）
2. tiff的数据矩阵（np.array）：shape = [波段，宽，长]
3. geotransform: tuple, tif file geotransform
4. projection: str, tif file projection
5. output dtype: gdal.GDT_Float32, tif file data type

### save_array()

保存GeoTiff数据。

输入：

1. 保存路径（Path or str）
2. tiff的数据矩阵（np.array）：shape = [波段，宽，长]
3. output dtype: gdal.GDT_Float32, tif file data type

### hsi_to_rgb()

将光谱数据转化到RGB（做了$\gamma$矫正和归一化）

输入：

1. 光谱数据（np.ndarray）:The hyperspectral image data, default shape is **[bands, width, height]**.
2. 红光波段索引（int）:The index of the red band.
3. 绿光波段索引（int）:The index of the green band.
4. 蓝光波段索引（int）:The index of the blue band.

返回：

1. The RGB image data, shape is **[width, height, 3(r, g, b)]**.

### merge()

合并多个GeoTiff

输入：

1. 输入的tif图像路径列表（list[Path, Path...]）
2. 输出的tif图像路径（Path）
