# ---------------------------------------------------------------
# File: netCDF2Raster_TOOL.py
# Name: Batch netCDF to Raster
# Date: Aug 10, 2017
# Contact: develop.geoinformatics@gmail.com
# NASA DEVELOP, Pamela Kanu, GISP // Contact Info: http://pamelakanu.wixsite.com/gisportfolio
# -----------------
# Description: Batches netCDF files to rasters in ArcGIS
# Usage: This code is scripted to run as a basic tool for ArcMap
#        Requires arcpy and spatial analyst packages
# Parameters:
#   In: Workspace
#   In: Variable (Variable used in ACOLITE)
# ---------------------------------------------------------------


# Import system modules
import arcpy
import os
from os import walk

# Set workspace
arcpy.env.workspace = arcpy.GetParameterAsText(0)
dirs = os.listdir(arcpy.env.workspace)
netCDFs = []
arcpy.env.overwriteOutput = True

# Set local variables
variableList = [arcpy.GetParameterAsText(1)]

XDimension = "x"
YDimension = "y"
bandDimmension = ""
dimensionValues = ""
valueSelectionMethod = ""

# Finds netCDF files in a folder
for root, dirs, files in os.walk(arcpy.env.workspace):
    for name in files:
        if ".nc" in name:
            # Removes the RGB version of ACOLITE output
            if "RGB" not in name:
                netCDF = (os.path.join(root, name))
                netCDFs.append(name)
        
            for net in netCDFs:
                print net
                for var in variableList:
                    # Split the layer name from the extension
                    lyrName = (os.path.join(root, net))[:-3] + ".lyr"
                    
                    # Split the raster from extension 
                    RasterLayer = ((netCDF)[:-3] +"_"+var + ".tif")
                    # Make the netCDF Raster
                    arcpy.MakeNetCDFRasterLayer_md(netCDF, var, XDimension, YDimension,
                                                       lyrName, bandDimmension, dimensionValues, 
                                                       valueSelectionMethod)
                    # Copy the Raster Layer to a Raster file
                    arcpy.CopyRaster_management(lyrName,RasterLayer,"DEFAULTS","","","","","32_BIT_FLOAT")
