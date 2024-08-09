"""
This script demonstrates the use of GDAL to perform several common raster operations efficiently. The functions provided are optimized for use in an R environment and include:

    1. **Quick Clip**: Clips a raster to the extent of a shapefile.
    2. **Quick Mosaic**: Mosaics a set of rasters, taking the top value only.
    3. **Quick Translate**: Resamples a raster to a different CRS.
    4. **Quick Merge**: Merges two rasters into one file.
    ## Requirements
    - Python 3.x
    - GDAL library
    - osgeo 
    - glob
"""
### set libraries
import os
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal, osr, ogr
gdal.UseExceptions()
from glob import glob
import time

def quick_clip(rasters, shapefile, output_file, separate_bands=True):
    """
    Clips a raster to the specified bounding box.
       Parameters:
        - rasters (dir / file): Path to the input rasters
        - output_raster_path (str): Path to save the clipped raster file.
        - shapefile (str): Path to the shapefile to clip the raster with.
    
       Returns:
        - None
    """
    st = time.time()
    ## if rasters is a directory, get all the tifs in the directory
    if os.path.isdir(rasters):
        rasters = glob(os.path.join(rasters, "*.tif")) + glob(os.path.join(rasters, "*.tiff"))
    ## if rasters is still empty, return
    if len(rasters) == 0:
        print("No rasters found")
        return
    # if rasters is a list of files, do nothing
    if isinstance(rasters, list):
        pass
    ## else if rasters is a single file, make it a list
    elif os.path.isfile(rasters):
        rasters = [rasters]
    ## set up the output file names
    # if the output file has an extension, remove it
    if output_file.endswith(".*"):
        print("Output file should not have an extension")
        return
    output_file_vrt = output_file + ".vrt"
    output_file_tif = output_file + ".tif"
    ## set up vrt to virtual memory
    vrt_path = "/vsimem/cropped_vrt.vrt"
    ## set up the VRT options to place each in its own band
    vrt_options = gdal.BuildVRTOptions(separate=separate_bands)
    ## build a VRT from the rasters
    vrt = gdal.BuildVRT(vrt_path, rasters, options=vrt_options)
    ## save this to a file
    gdal.Translate(output_file_vrt, vrt)
    ## Open the cutline shapefile
    cutline_ds = gdal.OpenEx(shapefile, gdal.OF_VECTOR)
    ## Get the cutline layer
    cutline_layer = cutline_ds.GetLayer()
    ## Set the warp options with the croptoCutline feature
    warp_options = gdal.WarpOptions(format='GTiff', cutlineDSName=shapefile, cropToCutline=True)
    ## Warp the VRT file with the cutline
    gdal.Warp(output_file_tif, vrt, options=warp_options)
    print(f"Iter time: {time.time() - st}")
    print(f"Output file: {output_file_tif}")

def quick_mosaic(raster_paths, output_path):
    """
    Mosaics multiple rasters into a single raster.
    Parameters:
    - raster_paths (list of str): List of paths to the input raster files.
    - output_path (str): Path to save the mosaiced raster file.
    "
    Returns:
    - None
    """
    st = time.time()
    output_path_vrt = output_path + ".vrt"
    output_path_tif = output_path + ".tif"
    
    ## set up the VRT options to place each in is NOT in its own band (i.e. take the first)
    # Set up the VRT options to ignore NaN values
    # make vrt
    destName = output_path_vrt
    #kwargs = {'separate': True} ## I think this should be false?
    ds = gdal.BuildVRT(destName,raster_paths)
    #close and save ds
    ds = None
    # save vrt to tif with gdal translate
    kwargs = {'format': 'GTiff'}
    fn = output_path_vrt
    dst_fn = output_path_tif    
    ds = gdal.Translate(dst_fn, fn, **kwargs)
    ds = None
    ##
    print(f"Iter time: {time.time() - st}")
    print(f"Output file: {output_path_tif}")
    return(None)
def quick_translate(raster_path, output_path, target_crs):
    """
    Reprojects a raster to a specified coordinate reference system (CRS).
    "
    Parameters:
    - raster_path (str): Path to the input raster file.
    - output_path (str): Path to save the reprojected raster file.
    - target_crs (str): Target coordinate reference system (e.g., 'EPSG:4326').
    "
    Returns:
    - None
    """
    st = time.time()
    filename = raster_path
    input_raster = gdal.Open(filename)
    output_raster = output_path
    warp = gdal.Warp(output_raster,input_raster,dstSRS=target_crs)
    warp = None # Closes the files
    print(f"Iter time: {time.time() - st}")
    print("Raster has been reprojected and saved to: ", output_path)

