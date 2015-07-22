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



##Tools

Tools are bundled together in an ArcGIS python toolbox.

1. Classify LANDSAT using NIR and NDVI
The classify landsat tool takes a list of image folders, an output name 
and threshold values for NDVI and NIR. The image folders need to have a 
results that have been processed by METRIC. Each image must have a folder 
called "products" that contains a raster for the NDVI and surface 
reflectance. The tool uses the NIR band (band 5) from the reflectance_surf 
raster since the product has been calibrated.  

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
