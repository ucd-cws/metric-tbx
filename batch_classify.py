__author__ = 'Andy'

import classify_NIR_NDVI
import csv
import os
import arcpy

# csv file
csv_file = r"Z:\metric\batch_images.csv"

# path to image folder
image_folder = r"X:\metric\Images"

# path to output folder for classified images
output_folder = r"X:\metric\Fallowing2015"


# ndvi
ndvi = 0.25

# nir
nir = 0.1

# parameter stack
classify_inputs = []

with open(csv_file, "rb") as f:
	reader = csv.reader(f)
	next(f) # skip first line
	for line in reader:
		print line
		landpaths = [os.path.join(image_folder, line[0]), os.path.join(image_folder, line[1]), os.path.join(image_folder, line[2])]
		output = os.path.join(output_folder, line[3])
		classify_inputs.append([landpaths, output])

try:
	for img_set in classify_inputs:
		folders = img_set[0]
		output = img_set[1]

		# set env to coordinate sys
		arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984 UTM Zone 10N")

		print "classify_NIR_NDVI.main({0}, {1}, {2}, {3})".format(folders, output, ndvi, nir)
		classify_NIR_NDVI.main(folders, output, ndvi, nir)
except:
	raise ValueError("Something went wrong. Try again.")