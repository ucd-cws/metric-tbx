__author__ = 'Andy'

import arcpy_metadata as md
import datetime
import os

def write_metadata(raster, sources, ndvi_threshold, nir_threshold):
	images = []
	for source in sources:
		base, img = os.path.split(source)
		images.append(img)

	metadata = md.MetadataEditor(raster)
	metadata.title.set("Classified Raster: fallow, agriculture or water")
	metadata.purpose.set("Raster layer represents a classified raster with 3 classes: 1 = water, 2 = fallow,"
	                     " 3 = agriculture.")

	metadata.abstract.append('Classified raster generated for METRIC project studying fallowing in CV. Processing finished at {0:}. The '
	                         'classified raster combines the following LANDSAT images: {1}. The thresholds used for '
	                         'the classification are NDVI = {2} and NIR = {3}.'.format(datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p"), images, ndvi_threshold, nir_threshold))
	metadata.finish()
