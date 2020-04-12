import geopandas
import rasterio
import matplotlib.pyplot as plt
import gdal
import numpy as np
from osgeo import gdal
from osgeo import ogr
from osgeo import gdalconst
import os
from scipy import ndimage

class JavPopEnvi():
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
            EjSpP:          # path of      data based on administrative divisions 
            BuiltUpSpP :    # path of      built up area polygon, which we want to allocate data above to 
            BuiltDataP :    # path of      allocated data, the polygon data that we are looking forward
            BuiltRasterP ： # path of      allocated data, rasterized.   (malfunctioning)
        '''
        self.EjSpP = '.\Data\EastJava_Kec.shp'            #  data based on administrative divisions 
        self.BuiltUpSpP = '.\Data\Kec_buffer.shp'         #  built up area polygon, which we want to allocate data above to 
        self.BuiltDataP = '.\Data\BuiltData.shp'          #  allocated data, the polygon data that we are looking forward
        self.BuiltRasterP = '.\Data\BuiltR.tif'
        self.BDtif = '.\Data\PopBDtif.tif'
    
    def DfRead(self, file = None, show = True):
        '''
        use geopanda to read the shapefile in ./data folder
        file:     path of the shp file
        show the shape file is required
        return       GeoDataFrame  
        '''
        if file is None:
            file =self.EjSpP # self is an argument only available at function call time.
        
        if not os.path.isfile(file):
            raise ValueError("Input file does not exist: {0}. I'll quit now.".format(file))
        elif str(file)[-3:] != 'shp':
            raise ValueError("Input file should be a shapefile, not a {0}. I'll quit now.".format(file[-3:]))        

           
        fileDf = geopandas.read_file(file)
        if show == True:
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
    
    def JavInt(self,EjSp = None, BuiltUpSp = None ):
        '''
        intsect two shapefiles:
            EjSp is the 
            BuiltUpSp is the file 
        return the required Spa file, our analysis shapefile
        '''
        if EjSp == None:
            EjSp = self.EjSp
        if BuiltUpSp == None:
            BuiltUpSp = self.BuiltUpSp
        BuiltUpSp = self.DataClean(BuiltUpSp)
        BuiltData = geopandas.overlay(EjSp, BuiltUpSp, how='intersection')
        return BuiltData
    
    def JavShow(self,bp):
        bp.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
        return
    
       
    def ConvJavRaster(self, size = 100, shapefile = None, rasterloc = None):
        '''
        ### malfunctioning
        this fun is supposed to convert a shape file to raster, but somehow it failed.
        shapefile  :  the actual shp file that we want to convert
        rasterloc  :  path of the raster that we want to deposit
        size:   size of cell,  unit is meter
        
        return None
        '''
        if shapefile is None:
            shapefile = self.BuiltUpSpP # self is an argument only available at function call time.
        if rasterloc == None:
            rasterloc = self.BuiltRasterP

        # a. Open 1) opening the shapefile    
        source_ds = ogr.Open(shapefile)
        source_layer = source_ds.GetLayer()

        # b. creating the format (empty) raster data source
        pixelWidth = pixelHeight = size 
        x_min, x_max, y_min, y_max = source_layer.GetExtent()
        cols = int((x_max - x_min) / pixelHeight)
        rows = int((y_max - y_min) / pixelWidth)
        target_ds = gdal.GetDriverByName('GTiff').Create(raster_path, cols, rows, 1,  gdal.GDT_Float64) ##COMMENT 2
        target_ds.SetGeoTransform((x_min, pixelWidth, 0, y_max, 0, -pixelHeight))
        band = target_ds.GetRasterBand(1)
        NoData_value = -999
        burnVal = 0
        band.SetNoDataValue(NoData_value)
        band.FlushCache()
        gdal.RasterizeLayer(target_ds, [1], source_layer,burn_values=[burnVal] )#options=["ATTRIBUTE=POP_CHANGE"])
        return

    
    
class JavRasterAnalysis(object):
    '''
    This class will initialize Raster analysis unit
    
    '''
    def __init(self, JavPath = '.\Data\popbdden.tif' ):
        self.BDtif = '.\Data\PopBDtif.tif'
        self.rs = gdal.Open(JavPath)       
        
    def JavaResize(self):
        '''
        clean the raster data
        '''
        
        
        
        
    def JavaPop(self):
        '''
        Caculate total population
        return a int number  , which should be between 20m - 30m
        '''
        img = rs.ReadAsArray()/100  
        
    def JavaShow(self, log = True):
        '''
        Caculate total population
        return a int number  , which should be between 20m - 30m
        '''
        figure = self.rs
        figure = np.where(figure ==0, np.NaN, figure)
        plt.imshow(log(figure))
        return
    
    def JavaDilation(self ): 
        '''
        Make the raster file looks nicer
        return raster
        '''
        # binary_dilation with original value
        for m in range(60):
            index = np.where(imgbw_ring)
            length = len(index[0])
            index[0][100]
            for u in range(length):
                    i = index[0][u]
                    j = index[1][u]
                    if i == sizeY-1 or j == sizeX-1:
                        if not np.isnan(img[i-1,j]):
                            img[i,j] = img[i-1,j]
                        elif not np.isnan(img[i,j-1]):
                            img[i,j] = img[i,j-1]
                    elif   i== 0 or j == 0:
                        if not np.isnan(img[i+1,j]): 
                            img[i,j] = img[i+1,j] 
                        elif not np.isnan(img[i,j+1]):
                            img[i,j] = img[i,j+1]             
                    else:
                        if not np.isnan(img[i+1,j]): 
                            img[i,j] = img[i+1,j] 
                        elif not np.isnan(img[i,j+1]):
                            img[i,j] = img[i,j+1] 
                        elif not np.isnan(img[i-1,j]):
                            img[i,j] = img[i-1,j]
                        elif not np.isnan(img[i,j-1]):
                            img[i,j] = img[i,j-1] 
            imgbw =  np.where(np.isnan(img),0, img)  > 0
            imgbw_ex = ndimage.binary_dilation(imgbw, iterations = 1)  # expansion first
            imgbw_ring = imgbw_ex > imgbw         
        
        
    def JavPopAdj():
        imgt= img / img.sum()*totalp
        imgt = np.where(img==0, np.NaN, img)
        plt.imshow(imgt)
    
    def JavaSplit():
        '''
        split the raster, create a boundary between to blocks, if they have different values
        it provides a base binary map for future uses
        return binary raster
        '''
        
        img_boundary_base = img.copy()   # the base map for future analysis....
        for i in range(sizeY-1):
            for j in range(sizeX-1):
                if img[i,j] == 0:
                    continue
                elif   img[i,j] != img[i+1,j]:
                    img_boundary_base[i,j] = 0
                elif img[i,j] != img[i,j+1]:
                    img_boundary_base[i,j] = 0
    def JavaRasterClean():
        '''
        clean the raster data
        '''
    
    def JavaSmoothValue():
        '''
        This one is largely a failed project
        return np.array with smoother values
        '''
        # smoothing the value
        img_smooth = img.copy()
        method_smooth = 'slow'
        img_boundary_t = img_boundary_base
        img_binary = img>0
        coresize = 55 # the heterogineous core that have a same population density
        img_core = ndimage.binary_erosion(img_boundary>0, iterations= 60 - coresize)

        if coresize <50:
            raise("dangerous, super slow")

        for m in range(60 - coresize):

            img_boundary_t = ndimage.binary_erosion(img_boundary_t>0, iterations=1)
            img_index = img_binary>img_boundary_t
            index = np.where(img_index)
            length = len(index[0])
            print(length)

            for u in range(length):
                i = index[0][u]
                j = index[1][u]
                if i <= 0 or j <= 0:
                    continue
                elif i >= sizeY-1 or j >= sizeX-1:
                    continue
                else:
                    temp_9 =  img_smooth[i-1:i+2,j-1:j+2]    #img_smooth[i,  j],
                    if img_smooth[i,j] - temp_9.mean() < 5:
                        continue
                    elif method_smooth == 'slow':
                        img_smooth[i,j] = temp_9.mean()
                    elif method_smooth == 'fast':
                        img_smooth[i,j] = img_smooth[i,j]    + ((temp_9.max() - img_smooth[i,j])*0.4  
                                                             + (temp_9.min() - img_smooth[i,j])*0.4   )



    
    
    
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

   
if __main__ = "main"

