import geopandas
import rasterio
import matplotlib.pyplot as plt
import gdal
import numpy as np
from osgeo import gdal
from osgeo import ogr
from osgeo import gdalconst

class JavPopEnvi(object):
    '''
    The purpose of this class is supposed to preprocess and view the data. It has several main functions: 
        read or show the polygons
        generate the vector(shapefile) that we need
        rasterize polygons, which is the final unit of analysis
    note: I've stucked in the rasterization part for weeks, that's why I'm going to use an alternative methods in the next a couple of days
    '''
    def __init__ (self):
    '''
    Path of the files
    '''
        self.EjSpP = '.\Data\EastJava_Kec.shp'      
        self.BuiltUpSpP = '.\Data\Kec_buffer.shp'
        self.BuiltDataP = '.\Data\BuiltData.shp'
        self.BuiltRasterP = '.\Data\BuiltR.tif'
    
    def DfRead(self, file = self.EjSpP, show = True)
    '''
    use geopanda to read the file in data folder
    show the shape file is required
    return a GeoDataFrame  
    '''
        fileDf = geopandas.read_file(file)
        if show == True
            fileDf.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
        return fileDf
    
    def DataClean(self, path):
    '''
    cleaning the polygon data and delete unnessesary values
    return cleaned polygons, with 1 single col
    '''
        data = DfRead(path)
        data = data[['OBJECTID','geometry']]
        return data
    
    def JavInt(self,EjSp = self.EjSp, BuiltUpSp = self.BuiltUpSp ):
    '''
    intsect two shapefiles:
        EjSp is the 
        BuiltUpSp is the file 
    return the required
    '''
        BuiltUpSp = self.DataClean(BuiltUpSp)
        BuiltData = geopandas.overlay(EjSp, BuiltUpSp, how='intersection')
        return BuiltData
    
    def JavShow(self,bp):
        bp.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
        return
    
    def JavConcert():
        '''
        '''
        
    def ConvJavRaster(self, size = 100):
        
        raster_path = self.'BuiltData.tif'
        shapefile = self.BuiltData.shp'
        # 1) opening the shapefile    
        source_ds = ogr.Open(shapefile)
        source_layer = source_ds.GetLayer()

        # 2) Creating the destination raster data source
        pixelWidth = pixelHeight = size 
        x_min, x_max, y_min, y_max = source_layer.GetExtent()
        cols = int((x_max - x_min) / pixelHeight)
        rows = int((y_max - y_min) / pixelWidth)
        target_ds = gdal.GetDriverByName('GTiff').Create(raster_path, cols, rows, 1,  gdal.GDT_Float64) ##COMMENT 2
        target_ds.SetGeoTransform((x_min, pixelWidth, 0, y_max, 0, -pixelHeight))
        band = target_ds.GetRasterBand(1)
        NoData_value = -99
        burnVal = 0
        band.SetNoDataValue(NoData_value)
        band.FlushCache()
        gdal.RasterizeLayer(target_ds, [1], source_layer,burn_values=[burnVal] )#options=["ATTRIBUTE=POP_CHANGE"])
        return

    
    
class JavAnalysis(object):

    def vadata(self, data1):
        '''
        if a function find the data doesn't satisfy our critirias, return FALSE, otherwise, return either shp or raster, and for raster, return the range of data (0:255, etc)
        '''
        input = A
        input = B
    
    '''
    The purpose of this class is to reassign values to each individual cells.  
    package: conda install GDAL
    
    '''
        
    def getvalue (self, shape, method="easy" ):
        '''
        this function will make a shape file into raster
        '''
        return

    def ValueGen():
        '''
        generate random value that capable for our analysis
        '''
    
    def division (self, size ):
        '''
        the function could divide the images into different pixels, or settlements..
        '''
        return
    
    def analysis1 (self, size ):
    '''
    the function could divide the images into different pixels, or settlements..
    '''
        return

    
class Grid():
    '''
    The grid is for each individual village. 

    ''' 
    
    def __init__ (): 
        '''
        basic attributes of this image
        '''
        self.size = 100*100
        self.value = 1000    
        
        datatype = gdal.GDT_Byte
        burnVal = 1 #value for the output image pixels

        
    def getvalue (self, shape, method="easy" ):
        '''
        this function will make a shape file into raster
        '''
        return

    
    
    def division (self, size ):
        '''
        the function could divide the images into different pixels, or settlements..
        '''
        return

   
    

