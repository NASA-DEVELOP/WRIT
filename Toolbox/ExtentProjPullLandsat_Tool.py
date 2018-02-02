## This code describes the original raster, sets the coordinate system of the original
## to the ACOLITE version, and uses snapraster to georeference the ACOLITE version
## to the original in the process. This version of the code is meant to be run as a tool in ArcMap.

import arcpy
import os
from arcpy.sa import *
import datetime
arcpy.env.overwriteOutput = True

pathLandsat = arcpy.GetParameterAsText(0) # Input a band (not Band 8) from original landsat data
acoPath = arcpy.GetParameterAsText(1)  # Input geodatabase containing the Acolite raster, will be workspace
rotateYN = 0
rotateYN = (arcpy.GetParameterAsText(2)) # Need to rotate ACOLITE image? 1 if yes, anything else will read as no.
flipYN = 0
flipYN = (arcpy.GetParameterAsText(3)) # Need to flip ACOLITE image? 1 if yes, anything else will read as no.
acoRaster = arcpy.GetParameterAsText(4) # Input ACOLITE raster image

#sets current workspace to landsat rasters folder
arcpy.env.workspace = acoPath


# This section is a function that returns the projection and
# extent of the landsat raster

# Create the spatial reference object
spatial_ref = arcpy.Describe(pathLandsat).spatialReference
# Get the extent of raster
satRaster = arcpy.sa.Raster(pathLandsat)
myExtent = satRaster.extent

# If the spatial reference is unknown
if spatial_ref.name == "Unknown":
    print("{0} has an unknown spatial reference".format(raster))

    # Otherwise, print out the feature class name and
    # spatial reference
else:
    print("{0} : {1}".format(pathLandsat, spatial_ref.name))
    proj=str(("{1}".format(pathLandsat, spatial_ref.factoryCode)))

# Saves extent data for band    

bandList = []

# Analyzes band, gets individual pieces of extent
band = arcpy.sa.Raster(pathLandsat)
bandExtent = str(band.extent)
originalBottom, originalLeft, originalTop, originalRight, waste1, waste2, waste3, waste4 = bandExtent.split(" ")
originalBottomFlt = float(originalBottom)
originalLeftFlt = float(originalLeft)
originalTopFlt = float(originalTop)
originalRightFlt = float(originalRight)
bandList.append([bandExtent])

# Fixes orientation, size, and location of acolite image

    
arcpy.DefineProjection_management(acoRaster, proj)

#rotates acolite image if applicable
if rotateYN == 'true':
    arcpy.Rotate_management(acoRaster, "intermedRot" ,"180")
    
arcpy.env.snapRaster = pathLandsat

arcpy.CheckOutExtension("Spatial")

#flips acolite image if appropriate
if flipYN == 'true':
    if rotateYN == 'true':
        arcpy.Mirror_management("intermedRot", "intermedMir")
    else:
        arcpy.Mirror_management(acoRaster, "intermedMir")
#rescales acolite image

cellSizeXResult = arcpy.GetRasterProperties_management(pathLandsat, "CELLSIZEX")
cellSizeYResult = arcpy.GetRasterProperties_management(pathLandsat, "CELLSIZEY")
cellSizeX = cellSizeXResult.getOutput(0)
cellSizeY = cellSizeYResult.getOutput(0)

#Chooses appropriate raster to apply landsat cell size to
if flipYN == 'true':
    arcpy.Rescale_management("intermedMir", "intermedScale", cellSizeX, cellSizeY)
else:
    if rotateYN == 'true':
        arcpy.Rescale_management("intermedRot", "intermedScale", cellSizeX, cellSizeY)
    else:
        arcpy.Rescale_management(acoRaster, "intermedScale", cellSizeX, cellSizeY)

    

#Reclassify and clip corrected acolite image to get rid of nodata border

myRemapRange =  RemapRange([[-1,1,1]])

# Execute Reclassify
outReclassify = arcpy.sa.Reclassify("intermedScale", "VALUE",myRemapRange,'NODATA')

# Save the output 

outReclassify.save("intermedClass")

arcpy.RasterToPolygon_conversion("intermedClass", "dataMask", "NO_SIMPLIFY",
                                  "VALUE")
# Delete the row that has the "NODATA" polygon to make mask  
    
with arcpy.da.UpdateCursor("dataMask", 
                          ["ID"]) as cursor:
        for row in cursor:
            if row[0] == 2:
                cursor.deleteRow()

                
# Clips Rescaled raster to exclude NoData using mask
arcpy.Clip_management("intermedScale", "#", "intermedClipped", "dataMask", "0", "ClippingGeometry")




# Finds difference between acolite image geolocation and original image geolocation, corrects
# This process matches the southwest corner of each image, which *should* have the same pixel size and dimensions
scaledRaster = arcpy.sa.Raster('intermedClipped')
scaledExtent = str(scaledRaster.extent)
acoBottom, acoLeft, acoTop, acoRight, waste5, waste6, waste7, waste8 = scaledExtent.split(" ")
acoBottomFlt = float(acoBottom)
acoLeftFlt = float(acoLeft)
acoTopFlt = float(acoTop)
acoRightFlt = float(acoRight)
xShift = str(originalLeftFlt - acoLeftFlt)
yShift = str(originalBottomFlt - acoBottomFlt)

#This section looks in the title of the landsat file to find the date it was taken, and uses that date in the output file name
foundDate = 'NoDate' # In case this doesn't work
    
def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1

if find_str(pathLandsat, "199") != -1:
    foundDate = pathLandsat[find_str(pathLandsat, "199")+2:find_str(pathLandsat, "199")+8]
if find_str(pathLandsat, "200") != -1:
    foundDate = pathLandsat[find_str(pathLandsat, "200")+2:find_str(pathLandsat, "200")+8]
if find_str(pathLandsat, "201") != -1:
    foundDate = pathLandsat[find_str(pathLandsat, "201")+2:find_str(pathLandsat, "201")+8]
    
    
arcpy.Shift_management('intermedClipped',acoPath+ '\\FA_'+foundDate+cellSizeX+'_'+'m',yShift,xShift,pathLandsat)

#Cleans up by deleting intermediate files.
arcpy.Delete_management("intermedMir")
arcpy.Delete_management("intermedRot")
arcpy.Delete_management("intermedMir")
arcpy.Delete_management("intermedClass")
arcpy.Delete_management("intermedScale")
arcpy.Delete_management("intermedClipped")
arcpy.Delete_management("dataMask")

