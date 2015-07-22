# Fallow Classification

## About
Classify water, agriculture or fallow fields using LANDSAT imagery 
during the summer months for the Central Valley. 

##Landsat images
The project used LANDSAT 7 (pre-2012) and LANDSAT 8 images. Images that 
had cloud cover were elimated from the processing list. The Central 
Valley is covered by three main landsat image paths: P42_R35, P43_R34, 
P44_R33. Due to the orbit of the satellites, each image is from seperate dates. The tiles were mosaiced together using the closest Julian date (time spread between 
all images ~9 days). 

##Methods
Steps
- Group images by Julian Date
- Classify each image in group seperately using processed NDVI and NIR (for surface reflectance raster). Sets classified raster value based on set threshold for 
determining fallow, ag or water from value. 
- The individual classified rasters are then mosaiced together.
- The mosaiced raster is then masked by the known agriculture extent (DWR landuse)
- Area in each class is tabulated by CVPM regions (Central Valley proeduction management?)

##Notes

- The extent of the landsat images varies slightly. Not all CVPM regions 
in the Central Valley are covered by the extent of the three LANDSAT 
tiles. Each image is slightly different. 
- The tools require ArcGIS's Spatial Analyst liscense
- Optional: install Nick's arcpy_metadata (via pip) if you want metadata 
to be added to the output from the classify tool. 


##Tools

Tools are bundled together in an ArcGIS python toolbox.

1. Classify LANDSAT using NIR and NDVI
The classify landsat tool takes a list of image folders, an output name 
and threshold values for NDVI and NIR. The image folders need to have a 
results that have been processed by METRIC. Each image must have a folder 
called "products" that contains a raster for the NDVI and surface 
reflectance. The tool uses the NIR band (band 5) from the reflectance_surf 
raster since the product has been calibrated. The tool can take any number 
of image folder, it deals with each classification seperately and then 
merges the result. Optional (if arcpy_metadata installed): will 
automatically add metadata (source images, date, thresholds) to the 
classified rasters. The metadata included can be changed in meta.py.

Note: See batch_classify.py for classifying a bunch of images at once. 
The tool can also be run in batch mode via the ArcGIS interface.


2. Extract by Agriculture
Masks classifed rasters by a polygon feature class that represents the 
areas that are classified as agriculture. Typically the mask used was a 
composite of the individual counties DWR landuse shapefiles with only 
agriculture selected. THis remove all natural or urban areas from the 
classified raster. 


3. Tabulate by CVPM region
Tabulates the total area by a region. The tool calculates the total area 
(in square meters) in each class and returns the result as a result 
table (.dbf). The tool is designed to be used with the results from the 
extract by agriculture tool and the CVPM regions.


##Scripts

###batch_classify.py
This script reads in the paths from a csv file and passes them to the classify raster function. The csv file should have four columns and header. The first three 
columns should be the name of the image folder you want included (note: only will work for three image tiles, need to customize in other situations). The final 
column will be the output name with desired raster extension. The input, output and thresholds are all hardcoded in the file and should be modified as fit. 

###read_result.r
R function to read all .dbfs in a folder and add colums with metadata that is parsed from the file name. The files should be of the format 'xx_year_start_end' where 
start and end are the Julian dates for the first and last image dates for the rasters included in the combined product. The script appends all of the tables into a 
single result for analysis and sharing.

###rename_df.r
Renames and sorts the columns of the final data table and exports it to a csv file. 




