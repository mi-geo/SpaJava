'''
The module is for data analysis in Java island.
'''
import os
from pathlib import Path
import geopandas
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
from osgeo import ogr
from scipy import ndimage

class JavaPolygonPrepare():
    '''
    Purpose: preprocess and view the data. It has several main functions:
        1. read or show the polygons
        2. generate the vector(shapefile) that we need
        3. rasterize polygons, which is the final unit of analysis
    note: I've stucked in the rasterization part for weeks, that's why I'm going
            to use an alternative methods in the next a couple of days
    '''

    def __init__(self):
        '''
        Path of the files
            java_shp:          # data based on administrative divisions
            builtup_shp:   # built-up area polygon,
                              the area should contain final data
            Built_DataP:   # allocated data, the polygon data that we are looking forward
            built_rs ： # allocated data, rasterized.   (malfunctioning)
        '''
        self.java_shp = Path(r'./Data/EastJava_Kec.shp')
        self.builtup_shp = Path(r'./Data/Kec_buffer.shp')
        self.built_rs = Path(r'./Data/BuiltR.tif')

    def shp_read(self, file=None, show=True):
        '''
        use geopanda to read the shapefile in ./data folder
        file:     path of the shp file
        show the shape file is required
        return       GeoDataFrame
        '''
        if file is None:
            file = self.java_shp # self is an argument only available at function call time.
            file_df = geopandas.read_file(file)
            if show is True:
                file_df.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
        elif not os.path.isfile(file):
            raise ValueError("Input not exist: {0}. I'll quit now.".format(file))
        elif str(file)[-3:] != 'shp':
            raise ValueError("Input should be shp, not a {0}. quit now.".format(str(file)[-3:]))
        else:
            file_df = geopandas.read_file(file)
            if show is True:
                file_df.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
        return file_df

    def data_clean(self, path, show=False):
        '''
        cleaning the polygon data and delete unnessesary values
        return cleaned polygons, with 1 single col
        '''
        data = self.shp_read(path, show=show)
        data = data[['OBJECTID', 'geometry']]
        return data

    def intersect(self, java_shp=None, builtup_shp=None):
        '''
        intsect two shapefiles:
            java_shp is the file 1
            builtup_shp is file 2
        return the required Spa file, our analysis shapefile
        '''
        if java_shp is None:
            java_shp = self.data_clean(self.java_shp, show=False)
        if builtup_shp is None:
            builtup_shp = self.data_clean(self.builtup_shp, show=False)
        builtup_shp = self.data_clean(builtup_shp)
        int_data = geopandas.overlay(java_shp, builtup_shp, how='intersection')
        return int_data

    def fig_show(self, figure_file, figsize=(10, 10), alpha=0.5, edgecolor='k'):
        '''
        plot the shapefile
        '''
        figure_file.plot(figsize=figsize, alpha=alpha, edgecolor=edgecolor)

    def conv_raster(self, psize=100, shapefile=None, rasterloc=None, no_value=-999):
        '''
        ### malfunctioning
        this fun is supposed to convert a shape file to raster, but somehow it failed.
        shapefile: the actual shp file that we want to convert
        rasterloc: path of the raster that we want to deposit
        psize:   size of cell, unit is meter

        return None
        '''
        if shapefile is None:
            shapefile = self.builtup_shp # self is an argument only available at function call time.
        if rasterloc is None:
            rasterloc = self.built_rs

        # 1. opening the shapefile
        source_layer = ogr.Open(shapefile).GetLayer()

        # 2. creating the format (empty) raster data source
        x_min, x_max, y_min, y_max = source_layer.GetExtent()
        cols = int((x_max - x_min) / psize)
        rows = int((y_max - y_min) / psize)
        target_ds = gdal.GetDriverByName('GTiff').Create(rasterloc,
                                                         cols, rows, 1, gdal.GDT_Float64)
        target_ds.SetGeoTransform((x_min, psize, 0, y_max, 0, -psize))
        band = target_ds.GetRasterBand(1)
        band.SetNoDataValue(no_value)
        band.FlushCache()
        raster = gdal.RasterizeLayer(target_ds, [1], source_layer,
                                     burn_values=[0])#options=["ATTRIBUTE=POP_CHANGE"])
        return raster


class JavaRasterPrepare():
    '''
    This class will initialize Raster analysis unit

    '''
    def __init__(self, JavPath=Path(r'./Data/popbdden.tif')):
        if JavPath is None:
            self.raster = Path(r'./Data/popbdden.tif')
        else:
            self.raster = JavPath       # the raster file that we adopt in this analysis
        self.img = gdal.Open(self.raster).ReadAsArray()     # get the nd array matrix
        self.img = np.where(self.img < 0, 0, self.img)
        self.size_y = self.img.shape[0]   # size on Y axis, which is num of rows
        self.size_x = self.img.shape[1]   # size on X axis, which is num of colss

    def total_pop(self, cellsize=100):
        '''
        Caculate total population
        return a int number  , which should be between 20m - 30m
        '''
        img = self.img/cellsize
        pop = img.sum()
        return pop

    def rectify_pop(self, pop):
        '''
        clean the raster data
        to be continued....
        '''
        self.img = (self.img/self.img.sum())* pop

    def raster_show(self, logarithm=True):
        '''
        Caculate total population
        return a int number  , which should be between 20m - 30m
        '''
        figure = self.img
        if logarithm is True:
            figure = np.where(np.isnan(figure), 0, figure)
            plt.imshow(np.log(figure+1))
        else:
            figure = np.where(figure == 0, np.NaN, figure)
            plt.imshow(figure)

    def neo_dilation(self, repeat=50):
        '''
        dilate the origin img without changing it into a binary one
        warning: it takes a while to execute this func
        return raster
        '''
        # binary_dilation with original value
        img = self.img
        img = np.where(np.isnan(img), 0, img)
        size_y = self.size_y
        size_x = self.size_x

        # binary_dilation with original value
        # img is a imgage where -9999 stand for NaN values
        imgbw = img > 0 # binary image
        #img =np.where(img == -9999, np.NaN, img)         # reorganize img
        imgbw_ex = ndimage.binary_dilation(imgbw, iterations=1)  # expansion first
        imgbw_ring = imgbw_ex > imgbw                   # detect the changes ....
        img = np.where(img == 0, np.NaN, img)

        for _ in range(repeat):
            index = np.where(imgbw_ring)
            length = len(index[0])
            for k in range(length):
                i = index[0][k]
                j = index[1][k]
                if i == size_y-1 or j == size_x-1:
                    if not np.isnan(img[i-1, j]):
                        img[i, j] = img[i-1, j]
                    elif not np.isnan(img[i, j-1]):
                        img[i, j] = img[i, j-1]
                elif   i == 0 or j == 0:
                    if not np.isnan(img[i+1, j]):
                        img[i, j] = img[i+1, j]
                    elif not np.isnan(img[i, j+1]):
                        img[i, j] = img[i, j+1]
                else:
                    if not np.isnan(img[i+1, j]):
                        img[i, j] = img[i+1, j]
                    elif not np.isnan(img[i, j+1]):
                        img[i, j] = img[i, j+1]
                    elif not np.isnan(img[i-1, j]):
                        img[i, j] = img[i-1, j]
                    elif not np.isnan(img[i, j-1]):
                        img[i, j] = img[i, j-1]
            imgbw = np.where(np.isnan(img), 0, img) > 0
            imgbw_ex = ndimage.binary_dilation(imgbw, iterations=1)  # expansion first
            imgbw_ring = imgbw_ex > imgbw

        self.img = np.where(np.isnan(img), 0, img)
        return img

    def block_split(self):
        '''
        split the raster, create a boundary (0) between too adjcent rasters blocks,
        it provides a base binary map for future uses
        do this step after neo_dilation
        warning: it takes a while to run

        return binary raster
        '''
        img = self.img.copy()
        size_y = self.size_y
        size_x = self.size_x
        img_boundary_base = self.img.copy()   # the base map for future analysis....
        for i in range(size_y-1):
            for j in range(size_x-1):
                if img[i, j] == 0:
                    pass
                elif img[i, j] != img[i+1, j]:
                    img_boundary_base[i, j] = 0
                elif img[i, j] != img[i, j+1]:
                    img_boundary_base[i, j] = 0
        img_boundary_bw = img_boundary_base > 0
        return img_boundary_bw

    def smoothen_raster(self, img_boundary_bw, coresize=55, method_smooth='low'):
        '''
        create a smoothened border between contigenous raster blocks
        warning: it takes about 1 min to run
        coresize: the heterogineous core in each block
        method_smooth: two methods to smoothen the border:
                       'slow' is slower, 'fast' is more radical
        img_boundary_bw: the binary map depict the boundaries, generated by  self.JavaSplit

        return np.array
        '''
        # smoothing the value
        img_s = self.img.copy()
        img_boundary_t = img_boundary_bw   # the foundation of borders
        img_binary = img_s > 0

        if coresize < 50:
            print("dangerous, super slow. The program will stop")
            return img_s

        for _ in range(60 - coresize):

            img_boundary_t = ndimage.binary_erosion(img_boundary_t > 0, iterations=1)
            img_index = img_binary > img_boundary_t
            index = np.where(img_index)
            length = len(index[0])
            print(length)

            for k in range(length):
                i = index[0][k]
                j = index[1][k]
                if i <= 0 or j <= 0:
                    pass
                elif i >= self.size_y-1 or j >= self.size_x-1:
                    pass
                else:
                    temp_9 = img_s[i-1:i+2, j-1:j+2]    #img_s[i, j],
                    if img_s[i, j] - temp_9.mean() < 5:
                        pass
                    elif method_smooth == 'slow':
                        img_s[i, j] = temp_9.mean()
                    elif method_smooth == 'fast':
                        img_s[i, j] = img_s[i, j] + ((temp_9.max() - img_s[i, j])*0.4 +
                                                     (temp_9.min() - img_s[i, j])*0.4)
        return img_s

    def neo_erosion_raster(self, img_boundary, coresize=55, show=True):
        '''
        to create the erosion unit of analysis
        return the final raster that we want
        '''
        binary_boundary_base = img_boundary > 0
        img_core = ndimage.binary_erosion(binary_boundary_base, iterations=60-coresize)
        if show is True:
            plt.imshow(img_core)
        img = self.img
        img = np.where(np.isnan(img), 0, img)
        img = img_core*img
        return img


class JavaRasterAnalysis():
    '''
    this case is on-hold. for doing raster analysis
    '''
    def __init__(self):
        '''
        if a function find the data doesn't satisfy our critirias,
        return FALSE, otherwise, return either shp or raster, and
        for raster, return the range of data (0:255, etc)
        '''

    def derivate(self):
        '''
        potential spatial ODE model
        '''

    def spatial_stats(self):
        '''
        potential spatial statistics
        '''

if __name__ == "__main__":
    print('it is on')
