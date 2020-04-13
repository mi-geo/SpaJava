import sys
from SpaJava import allocpop
import pytest
import numpy as np 

JavaTest = allocpop.JavPopEnvi()

def test_file_load_good():
    # test if function returns numpy array for good input file.
    data = JavaTest.JavRead(file = ".\Data\Kec_buffer.shp", show=False)
    assert "geopandas" in str(type(data)) 

def test_file_load_bad():
    # Test if the function raises the exception if nonexisting file name is passed as parameter.
    with pytest.raises(ValueError) as excinfo:
        JavaTest.JavRead(file = '.\Data\PopBDtif.tif')

    assert "Input file should be a shapefile" in str(excinfo.value)

def test_file_load_missing_file():
    # Test if the function raises the exception if nonexisting file name is passed as parameter.
    with pytest.raises(ValueError) as excinfo:
        JavaTest.JavRead(file = ".\Data\non-existing_file.txt")

    assert "Input file does not exist" in str(excinfo.value)