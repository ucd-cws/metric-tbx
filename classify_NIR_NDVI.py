# ---------------------------------------------------------------------------------------------------
# Name: classify_NIR_NDVI.pyt
# Purpose: Determines fallowing by classifying images using NIR and NDVI images
# Author: Andy Bell (ambell@ucdavis.edu)
# Created: 7/20/2015
# ---------------------------------------------------------------------------------------------------

import arcpy
import os
from arcpy import env
from arcpy.sa import *


# classified values
# 1: water
# 2: fallow
# 3: agriculture


def classify_nir_ndvi(NDVI_Raster, NDVI_threshold, NIR_Raster, NIR_threshold, output):
	# let's deal with the NDVI raster first
	# need to set null value for ndvi raster
	ndvi_null = SetNull(Raster(NDVI_Raster) == 0, Raster(NDVI_Raster))
	ndvi_out = Con(ndvi_null < NDVI_threshold, 2, 3)  # conditional

	# Now let's deal with the NIR
	nir_null = SetNull(Raster(NIR_Raster) == 0, Raster(NIR_Raster))
	nir_out = Con(nir_null < NIR_threshold, 1)  # conditional

	# combine both raster products and save
	out = Con(IsNull(nir_out), ndvi_out, nir_out)

	#save
	out.save(output)
	return


#####
#examples

# temp local variables.... to be filled in by tool or cmd line
folder = r"C:\Users\Andy\Desktop\examples\P43_R34_2015_185"
NIR = r"images\LC80430342015185LGN00_B5.TIF"
NDVI = r"products\ndvi_07042015_P43R34_L8_F15.img"


# thresholds
nir_thresh = 0.3
ndvi_thresh = 0.15
# checkout license

try:
	if arcpy.CheckExtension("Spatial") == "Available":
		arcpy.CheckOutExtension("Spatial")
	else:
		# Raise a custom exception
		raise ValueError("license is unavailable")

	arcpy.AddMessage("Processing")
	classify_nir_ndvi(os.path.join(folder, NDVI), ndvi_thresh, os.path.join(folder, NIR), nir_thresh, os.path.join(folder, "test.tif"))
	arcpy.AddMessage("Saving")

except:
	print arcpy.GetMessages(2)
finally:
	arcpy.CheckInExtension("Spatial")
