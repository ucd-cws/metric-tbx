# ---------------------------------------------------------------------------------------------------
# Name: metric_tbx.pyt
# Purpose: ArcGIS python toolbox containing processing tools for measuring fallowing from Landsat
# Author: Andy Bell (ambell@ucdavis.edu)
# Created: 7/20/2015
# ---------------------------------------------------------------------------------------------------

import arcpy
import classify_NIR_NDVI
import os


class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "Toolbox"
		self.alias = ""

		# List of tool classes associated with this toolbox
		self.tools = [classify, tabulate, extract]


class classify(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Classify LANDSAT using NIR and NDVI"
		self.description = "Classify LANDSAT images using NIR and NDVI data products to determine water, agriculture or fallow."
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""

		folders = arcpy.Parameter(name='folders', displayName="Image Folders",
		                          datatype='DEWorkspace', multiValue='True')

		output = arcpy.Parameter(name='output', displayName="Location for classified output raster",
		                         datatype='DERasterDataset', direction='Output')

		ndvi_threshold = arcpy.Parameter(name='ndvi_threshold', displayName="NDVI threshold",datatype='Double')

		nir_threshold = arcpy.Parameter(name='nir_threshold', displayName="NIR threshold", datatype='Double')

		params = [folders, output, ndvi_threshold, nir_threshold]
		return params

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""

		# todo check if Spatial is available
		"""Allow the tool to execute, only if the ArcGIS Spatial Analyst extension is available."""
		try:
			if arcpy.CheckExtension("Spatial") != "Available":
				raise Exception
		except Exception:
			return False  # tool cannot be executed

		return True  # tool can be executed


	def updateParameters(self, parameters):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parameter
		has been changed."""
		return

	def updateMessages(self, parameters):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		return

	def execute(self, parameters, messages):
		"""The source code of the tool."""
		# get parameters
		folders = parameters[0].valueAsText.split(';')
		output = parameters[1].valueAsText
		ndvi_thresh = parameters[2].value
		nir_thresh = parameters[3].value

		arcpy.AddMessage("Starting Processing...")
		classify_NIR_NDVI.main(folders, output, ndvi_thresh, nir_thresh)

		return

class extract(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Extract by AG"
		self.description = "Masks classified raster to areas ID'ed as agriculture by DWR"
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""

		classified = arcpy.Parameter(name='classified', displayName="Classified Rasters",
		                             datatype='DERasterDataset', multiValue='True')

		output = arcpy.Parameter(name='output', displayName="Location for output",
		                         datatype='DEWorkspace', direction='Input')

		mask = arcpy.Parameter(name='mask', displayName="Agriculture Mask",
		                       datatype='GPFeatureLayer')

		# TODO set default
		# mask.value = r"?"

		params = [classified, output, mask]
		return params

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""

		# todo check if Spatial is available
		"""Allow the tool to execute, only if the ArcGIS Spatial Analyst extension is available."""
		try:
			if arcpy.CheckExtension("Spatial") != "Available":
				raise Exception
		except Exception:
			return False  # tool cannot be executed

		return True  # tool can be executed

	def execute(self, parameters, messages):
		"""The source code of the tool."""
		# get parameters
		classified_imgs = parameters[0].valueAsText.split(';')
		output_folder = parameters[1].valueAsText
		mask = parameters[2].valueAsText

		arcpy.AddMessage("Starting Processing...")

		for image in classified_imgs:
			arcpy.AddMessage(image)

			# extract by mask
			outmask = arcpy.sa.ExtractByMask(image, mask)

			#save
			base, name = os.path.split(image)
			output_name = os.path.join(output_folder, name)
			arcpy.AddMessage("Saving: %s" % output_name)
			outmask.save(output_name)

		return


class tabulate(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Tabulate by CVPM region"
		self.description = "Sums areas by class"
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""

		classified = arcpy.Parameter(name='classified', displayName="Masked Classified Rasters",
		                             datatype='DERasterDataset', multiValue='True')

		output = arcpy.Parameter(name='output', displayName="Location for output",
		                         datatype='DEWorkspace', direction='Output')

		regions = arcpy.Parameter(name='regions', displayName="CVPM regions",
		                       datatype='GPFeatureLayer')

		regions_field = arcpy.Parameter(name='regions_field', displayName="Region ID",
		                       datatype='Field', direction="Input")

		params = [classified, output, regions, regions_field]
		return params

	def updateParameters(self, parameters):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parameter
		has been changed."""

		return

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""

		# todo check if Spatial is available
		"""Allow the tool to execute, only if the ArcGIS Spatial Analyst extension is available."""
		try:
			if arcpy.CheckExtension("Spatial") != "Available":
				raise Exception
		except Exception:
			return False  # tool cannot be executed

		return True  # tool can be executed

	def execute(self, parameters, messages):
		"""The source code of the tool."""
		# get parameters
		masked_imgs = parameters[0].valueAsText.split(';')
		output_folder = parameters[1].valueAsText
		regions = parameters[2].valueAsText

		arcpy.AddMessage("Starting Processing...")

		for image in masked_imgs:
			arcpy.AddMessage(image)

			#save
			base, name = os.path.split(image)
			output_table = os.path.join(output_folder, name + ".dbf")
			arcpy.AddMessage("Saving: %s" % output_table)

			#Tabulate area
			arcpy.sa.TabulateArea(image, "Value", regions, region_zone_field, output_table)

		return