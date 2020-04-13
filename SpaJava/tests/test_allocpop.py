'''
test the allocpop.py file with pytests
'''
import pytest
from SpaJava import allocpop

TEST = allocpop.JavaPolygonPrepare()

def test_file_load_good():
    '''
    test if function returns numpy array for good input file.
    '''
    data = TEST.shp_read(file=".\\Data\\Kec_buffer.shp", show=False)
    assert "geopandas" in str(type(data))

def test_file_load_bad():
    '''
    Test if the function raises the exception if a tif is passed
    '''
    with pytest.raises(ValueError) as excinfo:
        TEST.shp_read(file='.\\Data\\PopBDtif.tif')
    assert "should be shp" in str(excinfo.value)

def test_file_load_missing_file():
    '''
    Test if the function raises the exception if nonexisting file name is passed as parameter.
    '''
    with pytest.raises(ValueError) as excinfo:
        TEST.shp_read(file=".\\Data\\non-existing_file.txt")
    assert "not exist" in str(excinfo.value)
