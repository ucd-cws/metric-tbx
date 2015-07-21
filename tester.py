__author__ = 'Andy'
from classify_NIR_NDVI import *
import arcpy

#examples

# temp local variables.... to be filled in by tool or cmd line
folder1 = r"C:\Users\Andy\Desktop\examples\P42_R35_2015_194"
folder2 = r"C:\Users\Andy\Desktop\examples\P43_R34_2015_185"
folder3 = r"C:\Users\Andy\Desktop\examples\P44_R33_2015_192"

folderlist = [folder2, folder1, folder3] # note output takes the projection of the first image in list

output = r"C:\Users\Andy\Desktop\examples\test\output_meta.tif"

# thresholds
nir_thresh = 0.1
ndvi_thresh = 0.15
# checkout license

try:
	if arcpy.CheckExtension("Spatial") == "Available":
		arcpy.CheckOutExtension("Spatial")
	else:
		# Raise a custom exception
		raise ValueError("license is unavailable")

	class_list =[]

	for folder in folderlist:
		print folder
		arcpy.AddMessage("Processing")
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