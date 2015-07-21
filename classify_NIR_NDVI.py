# ---------------------------------------------------------------------------------------------------
# Name: classify_NIR_NDVI.pyt
# Purpose: Determines fallowing by classifying images using NIR and NDVI images
# Author: Andy Bell (ambell@ucdavis.edu)
# Created: 7/20/2015
# ---------------------------------------------------------------------------------------------------

import arcpy, os, glob
from arcpy import env
from arcpy.sa import *

# make sure to checkout 'Spatial' extension license

# classified values
# 1: water
# 2: fallow
# 3: agriculture

def classify_nir_ndvi(NDVI_Raster, NDVI_threshold, NIR_Raster, NIR_threshold):
	"""
	:param NDVI_Raster: normalized difference vegetation index
	:param NDVI_threshold: NDVI threshold for determining fallow vs agriculture
	:param NIR_Raster: Near-infrared (band #5) reflectance band
	:param NIR_threshold: threshold for determining water
	:return: Classified raster with 3 classes: 1=water, 2=fallow, 3=agriculture
	"""

	# let's deal with the NDVI raster first
	# need to set null value for ndvi raster
	ndvi_null = SetNull(Raster(NDVI_Raster) == 0, Raster(NDVI_Raster))
	ndvi_out = Con(ndvi_null < NDVI_threshold, 2, 3)  # conditional statement

	# Now let's deal with the NIR
	nir_null = SetNull(Raster(NIR_Raster) == 0, Raster(NIR_Raster))
	nir_out = Con(nir_null < NIR_threshold, 1)  # conditional statement

	# combine both raster products
	out = Con(IsNull(nir_out), ndvi_out, nir_out)

	return out


def mosaic_classified(raster_list, output):
	"""
	:param raster_list: list of classified rasters to join
	:param output: path for the mosaic'ed raster
	:return:
	"""

	# split output destination
	location, name = os.path.split(output)

	# mosaic all rasters in raster list using the blend method.
	arcpy.MosaicToNewRaster_management(raster_list, location, name, "#", "#", "#", "1", "BLEND", "#")


def get_rasters(input_folder):
	"""
	:param input_folder: processed LANDSAT image folder path that contains NDVI and Reflectance Surface in products folder
	:return: NDVI and NIR paths as a list
	"""
	# find ndvi image path in folder
	ndvi_list = glob.glob(os.path.join(input_folder, 'products/ndvi_*.img'))
	# find reflectance surface image path in folder
	reflect_surf_list = glob.glob(os.path.join(input_folder, 'products/reflectance_surf_*.img'))

	if len(ndvi_list) == 1 and len(reflect_surf_list) == 1:  # check lengths of list
		ndvi = ndvi_list[0]
		reflect_surf = reflect_surf_list[0]
		# near infared is band # 5
		nir = os.path.join(reflect_surf, "Layer_5")

	else:
		raise ValueError("Bad match for NDVI and/or NIR raster in: %s . "
		                 "Make sure they are in the products folder." % input_folder)

	return ndvi, nir


def main(folderlist, output, ndvi_thresh, nir_thresh):

	try:
		if arcpy.CheckExtension("Spatial") == "Available":
			arcpy.CheckOutExtension("Spatial")
		else:
			# Raise a custom exception
			raise ValueError("license is unavailable")

		class_list =[]

		for folder in folderlist:
			arcpy.AddMessage("Processing: %s" % folder)
			rasters = get_rasters(folder)
			ndvi, nir = rasters[0], rasters[1]
			saver = classify_nir_ndvi(ndvi, ndvi_thresh, nir, nir_thresh)
			class_list.append(saver)

		#print class_list
		arcpy.AddMessage("Saving")
		mosaic_classified(class_list, output)

	except:
		print arcpy.GetMessages(2)
	finally:
		arcpy.CheckInExtension("Spatial")

	# try writing meta data
	try:
		import meta
		meta.write_metadata(output, folderlist, ndvi_thresh, nir_thresh)
	except:
		raise ValueError("Unable to automatically generate metadata for output file.")
		pass
