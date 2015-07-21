# ---------------------------------------------------------------------------------------------------
# Name: metric_tbx.pyt
# Purpose: ArcGIS python toolbox containing processing tools for measuring fallowing from Landsat
# Author: Andy Bell (ambell@ucdavis.edu)
# Created: 7/20/2015
# ---------------------------------------------------------------------------------------------------

import arcpy
import classify_NIR_NDVI

class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "Toolbox"
		self.alias = ""

		# List of tool classes associated with this toolbox
		self.tools = [classify]


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

		return True

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

