import os
import numpy as np
from osgeo import ogr, gdal
import subprocess

class ValiData(object):
    '''
    The target of this class is to validate the input data and see if they could satisfiy our requirement. 
    validation 1:  the input 1 is an raster file 
    validation 2: the input 2 is an shapefile

    '''
    def __init__(self):
        self.type = "jpg"
        self.type2 = "shp"

    def vadata(data1):
        '''
        if a function find the data doesn't satisfy our critirias, return FALSE, otherwise, return either shp or raster, and for raster, return the range of data (0:255, etc)
        '''
        input = A
        input = B

        
class Pop



class PopDistribution():
    '''
    The purpose of this class is to reassign values to each individual cells.  
    package: conda install GDAL
    
    '''

    
    def __init__ (InputVector = 'VectorName.shp',OutputImage = 'Result.tif',RefImage = 'Image_Name.tif',gdalformat = 'GTiff'):
        '''
        basic attributes of this image
        '''
        self.size = 100*100
        self.value = 1000    
        
        datatype = gdal.GDT_Byte
        burnVal = 1 #value for the output image pixels

    def prepareTIF(self, size <= 1000 ):
        '''
        turn a shape file to TIFF. Value of each pixcel representing the percentage of built-up area (0-1)
        '''
        # Get projection info from reference image
        Image = gdal.Open(self.RefImage, gdal.GA_ReadOnly)
        # Open Shapefile
        Shapefile = ogr.Open(self.InputVector)
        Shapefile_layer = Shapefile.GetLayer()

        # Rasterise
        print("Rasterising shapefile...")
        Output = gdal.GetDriverByName(gdalformat).Create(OutputImage, Image.RasterXSize, Image.RasterYSize, 1, datatype, options=['COMPRESS=DEFLATE']) 
        Output.SetProjection(Image.GetProjectionRef())
        Output.SetGeoTransform(Image.GetGeoTransform()) 

        # Write data to band 1
        Band = Output.GetRasterBand(1)
        Band.SetNoDataValue(0)
        gdal.RasterizeLayer(Output, [1], Shapefile_layer, burn_values=[burnVal])

        # Close datasets
        Band = None
        Output = None
        Image = None
        Shapefile = None

        # Build image overviews
        subprocess.call("gdaladdo --config COMPRESS_OVERVIEW DEFLATE "+OutputImage+" 2 4 8 16 32 64", shell=True)       
        
        
        return

        
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

    def prepareTIF(self, size <= 1000 ):
        '''
        turn a shape file to TIFF. Value of each pixcel representing the percentage of built-up area (0-1)
        '''
        # Get projection info from reference image
        Image = gdal.Open(self.RefImage, gdal.GA_ReadOnly)
        # Open Shapefile
        Shapefile = ogr.Open(self.InputVector)
        Shapefile_layer = Shapefile.GetLayer()

        # Rasterise
        print("Rasterising shapefile...")
        Output = gdal.GetDriverByName(gdalformat).Create(OutputImage, Image.RasterXSize, Image.RasterYSize, 1, datatype, options=['COMPRESS=DEFLATE']) 
        Output.SetProjection(Image.GetProjectionRef())
        Output.SetGeoTransform(Image.GetGeoTransform()) 

        # Write data to band 1
        Band = Output.GetRasterBand(1)
        Band.SetNoDataValue(0)
        gdal.RasterizeLayer(Output, [1], Shapefile_layer, burn_values=[burnVal])

        # Close datasets
        Band = None
        Output = None
        Image = None
        Shapefile = None

        # Build image overviews
        subprocess.call("gdaladdo --config COMPRESS_OVERVIEW DEFLATE "+OutputImage+" 2 4 8 16 32 64", shell=True)       
        
        
        return

        
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

   
    
class settlement():
    '''
    each human settlement is a object in this case.
    
    '''

    def __init__ ():
        '''
        basic attribute of each settlements
        '''
        self.pop61
        self.pop71
        self.pop80
        self.poploss
        
    def rltloc ():
        '''
        basic function detact its spaital relation with the other settlements surrounding
        '''
        return
    
