# GDAL_QuickTricks
A repository that includes a python file that uses osgeo to create some quick  raster files. 

## Includes
1. GDAL_QuickTricks.py - A script that sets up 3 extremely useful + fast functions for everyday raster use
    Quick_clip - creates a clipped raster from either a single raster or a stack of rasters clipped to  a shapefile
   Quick_mosaic - rapidly mosaices overlapping raster taking the first observation that is not NA
   Quick_translate - rapidly translates a raster to a given CRS using bilinear interpolation
3. GDAL_QuickTricks_Test.ipynb - sets up a series to test raster files that are used to showcase the functions 
5. GDAL_4_LIFE.qmd - showcases how and why to use the GDAL_QuickTricks in R
7. GDAL_4_LIFE.html - the rendered version of the HTML
   
** note GDAL_QuickTricks_Test.ipynb makes a series of test rasters that are stored within the folder. The .gitignore will avoid these files. But these are necessary if you want to run GDAL_4_LIFE
