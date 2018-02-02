## This code describes the original raster, sets the coordinate system of the original
## to the ACOLITE version, and uses snapraster and shift to georeference the ACOLITE version
## to the original in the process. This version of the code is meant to be run in Arcmap as part of a toolbox.
## Created by Randolph Colby, NASA DEVELOP Miami Beach Water Resources Summer 2017.
## Contact at johnrcolby1@gmail.com
## 6/30/2017

import arcpy
import os
from arcpy.sa import *
import datetime
arcpy.env.overwriteOutput = True

pathOriginal = arcpy.GetParameterAsText(0) # Input a band (not Band 8 for landsat) from original landsat/sentinel data
acoPath = arcpy.GetParameterAsText(1)  # Input geodatabase containing the Acolite raster, will be workspace
rotateYN = arcpy.GetParameterAsText(2) # Need to rotate ACOLITE image? check box for yes, leave blank for no.
flipYN = arcpy.GetParameterAsText(3) # Need to flip ACOLITE image? 1 if yes, anything else will read as no.
acoRaster = arcpy.GetParameterAsText(4)
removeborderYN = arcpy.GetParameterAsText(5) #Check box for sentinel, leave blank for for landsat
rotateAngle = arcpy.GetParameterAsText(6) # Degrees of rotation desired (90, 180, or 270)

#sets current workspace to landsat rasters folder
arcpy.env.workspace = acoPath

# This section is a function that returns the projection and
# extent of the landsat raster

# Create the spatial reference object
spatial_ref = arcpy.Describe(pathOriginal).spatialReference
# Get the extent of raster
satRaster = arcpy.sa.Raster(pathOriginal)
myExtent = satRaster.extent

# If the spatial reference is unknown
if spatial_ref.name == "Unknown":
    print("{0} has an unknown spatial reference".format(raster))

    # Otherwise, print out the feature class name and
    # spatial reference
else:
    print("{0} : {1}".format(pathOriginal, spatial_ref.name))
    proj=str(("{1}".format(pathOriginal, spatial_ref.factoryCode)))

# Analyzes band, gets individual pieces of extent
band = arcpy.sa.Raster(pathOriginal)
bandExtent = str(band.extent)
print bandExtent
originalBottom, originalLeft, originalTop, originalRight, waste1, waste2, waste3, waste4 = bandExtent.split(" ")
originalBottomFlt = float(originalBottom)
originalLeftFlt = float(originalLeft)
originalTopFlt = float(originalTop)
originalRightFlt = float(originalRight)
widthOriginal = originalRightFlt -originalLeftFlt
heightOriginal = originalTopFlt -originalBottomFlt
print widthOriginal, heightOriginal
print "Done pulling original data"

# Fixes orientation, size, and location of acolite image

print proj
print acoRaster
arcpy.DefineProjection_management(acoRaster, proj)

#rotates acolite image if applicable
if rotateYN == 'true':
    arcpy.Rotate_management(acoRaster, "intermedRot" ,rotateAngle)
    print "rotate"
        
#bring snapraster back here

arcpy.CheckOutExtension("Spatial")

#flips acolite image if appropriate
if flipYN == 'true':
    if rotateYN == 'true':
        arcpy.Mirror_management("intermedRot", "intermedMir")
        print 'flip + rotate'
    else:
        arcpy.Mirror_management(acoRaster, "intermedMir")    
        print 'flip'

#Clips off border of "NODATA" surrounding Lansat-ACOLITE images. If a Sentinel image has this (and no additional
#"NODATA" pixels inside the raster, uncheck the sentinel box to treat it as a landsat image.
if removeborderYN == 'true':
    #Create common variable name for all rasters possibly entering this process
    if flipYN == 'true':
        classInput = "intermedMir"
    else:
        if rotateYN == 'true':
            classInput = "intermedRot"
        else:
            classInput = acoRaster
    
    #Reclassify and clip oriented acolite image to get rid of nodata border

    myRemapRange =  RemapRange([[-1000000,1000000,1]])
            
    # Execute Reclassify
    outReclassify = arcpy.sa.Reclassify(classInput, "VALUE",myRemapRange,'NODATA')
    # Save the output 

    outReclassify.save("intermedClass")
    arcpy.RasterToPolygon_conversion("intermedClass", "dataMask", "NO_SIMPLIFY","VALUE")
            
    # Delete the row that has the "NODATA" polygon to make mask  
                        
    with arcpy.da.UpdateCursor("dataMask",["ID"]) as cursor:
        for row in cursor:
            if row[0] == 2:
                cursor.deleteRow()
                                    
    # Clips Rescaled raster to exclude NoData using mask
    arcpy.Clip_management(classInput, "#", "intermedClipped", "dataMask", "0", "ClippingGeometry")
            
    print "Done clipping"

print "Made it to cell sizing"
#Looks at cell size of original image and number of rows/ columns of original image to decide a scaling factor for the acolite image that
#may(Landsat) or may not(Sentinel) be clipped at theis point. Assumes an ACOLITE output cell size of 1m.
cellSizeXResult = arcpy.GetRasterProperties_management(pathOriginal, "CELLSIZEX")
cellSizeYResult = arcpy.GetRasterProperties_management(pathOriginal, "CELLSIZEY")
cellSizeX = cellSizeXResult.getOutput(0)
cellSizeY = cellSizeYResult.getOutput(0)
rowsOriginalResult = arcpy.GetRasterProperties_management(pathOriginal, "ROWCOUNT")
columnsOriginalResult = arcpy.GetRasterProperties_management(pathOriginal, "COLUMNCOUNT")
rowsOriginal =rowsOriginalResult.getOutput(0)
columnsOriginal = columnsOriginalResult.getOutput(0)
print cellSizeX
print cellSizeY

#Divides scaling factor by rows(acolite)/rows(original)

if removeborderYN == 'true':
    rowsAcoResult = arcpy.GetRasterProperties_management("intermedClipped", "ROWCOUNT")
    columnsAcoResult = arcpy.GetRasterProperties_management("intermedClipped", "COLUMNCOUNT")
else:
    rowsAcoResult = arcpy.GetRasterProperties_management(acoRaster, "ROWCOUNT")
    columnsAcoResult = arcpy.GetRasterProperties_management(acoRaster, "COLUMNCOUNT")

rowsAco=rowsAcoResult.getOutput(0)
columnsAco=columnsAcoResult.getOutput(0)
print rowsAco
print type(columnsAco)
     
#Chooses appropriate raster to apply landsat cell size to, scales raster up while considering possible row/column number mismatch
#between acolite and original
cellSizeXFlt = float(cellSizeX)
cellSizeYFlt =float(cellSizeY)
rowsOriginalFlt =float(rowsOriginal)
columnsOriginalFlt =float(columnsOriginal)
rowsAcoFlt =float(rowsAco)
columnsAcoFlt = float(columnsAco)
        
if removeborderYN == 'true':
    arcpy.Rescale_management("intermedClipped", "intermedScale", cellSizeXFlt/(columnsAcoFlt/columnsOriginalFlt), cellSizeYFlt/(rowsAcoFlt/rowsOriginalFlt))
else:
    if flipYN == 'true':
        arcpy.Rescale_management("intermedMir", "intermedScale", cellSizeXFlt/(columnsAcoFlt/columnsOriginalFlt), cellSizeYFlt/(rowsAcoFlt/rowsOriginalFlt))
    else:
        if rotateYN == 'true':
            arcpy.Rescale_management("intermedRot", "intermedScale", cellSizeXFlt/(columnsAcoFlt/columnsOriginalFlt), cellSizeYFlt/(rowsAcoFlt/rowsOriginalFlt))
        else:
            arcpy.Rescale_management(acoRaster, "intermedScale", cellSizeXFlt/(columnsAcoFlt/columnsOriginalFlt), cellSizeYFlt/(rowsAcoFlt/rowsOriginalFlt))  
                
print "Done rescaling"

scaledRaster = arcpy.sa.Raster('intermedScale')

# Finds difference between acolite image geolocation and original image geolocation, corrects
# This process matches the southwest corner of each image, which *should* have the same pixel size and dimensions
scaledExtent = str(scaledRaster.extent)
print scaledExtent
scaleBottom, scaleLeft, scaleTop, scaleRight, waste5, waste6, waste7, waste8 = scaledExtent.split(" ")
scaleBottomFlt = float(scaleBottom)
scaleLeftFlt = float(scaleLeft)
scaleTopFlt = float(scaleTop)
scaleRightFlt = float(scaleRight)
widthNew = scaleRightFlt -scaleLeftFlt
print widthNew
xShift = str(originalLeftFlt - scaleLeftFlt)
yShift = str(originalBottomFlt - scaleBottomFlt)
print "Done calculating shift parameters"

#This section looks in the title of the original file to find the date it was taken, and uses that date in the output file name
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

if find_str(pathOriginal, "201") != -1:
    foundDate = pathOriginal[find_str(pathOriginal, "201")+2:find_str(pathOriginal, "201")+8]
if find_str(pathOriginal, "200") != -1:
    foundDate = pathOriginal[find_str(pathOriginal, "200")+2:find_str(pathOriginal, "200")+8]
if find_str(pathOriginal, "199") != -1:
    foundDate = pathOriginal[find_str(pathOriginal, "199")+2:find_str(pathOriginal, "199")+8]
print "Done naming"

arcpy.env.snapRaster = pathOriginal
        
arcpy.Shift_management('intermedScale',acoPath+ '\\FA_'+foundDate+'_'+cellSizeX+'m',yShift,xShift,pathOriginal)

#Cleans up by deleting intermediate files.
arcpy.Delete_management("intermedMir")
arcpy.Delete_management("intermedRot")
arcpy.Delete_management("intermedMir")
arcpy.Delete_management("intermedClass")
arcpy.Delete_management("intermedScale")
arcpy.Delete_management("intermedClipped")
arcpy.Delete_management("dataMask")

print "Done"
