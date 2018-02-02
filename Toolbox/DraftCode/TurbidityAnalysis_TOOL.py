# ---------------------------------------------------------------
# File: TurbidityAnalysis_TOOL.py
# Name: Calculate Turbidity
# Date: Aug 10, 2017
# Contact: develop.geoinformatics@gmail.com
# NASA DEVELOP, Pamela Kanu, GISP // Contact Info: http://pamelakanu.wixsite.com/gisportfolio
# -----------------
# Description: Calculates Turbidity, Sand and Bottom Reflectance based on thresholds and coefficent of variance
# Usage: This code is scripted to run as a basic tool for ArcMap
#        Requires arcpy and spatial analyst packages
#        This tool works best when ran through ArcMap
# Parameters:
#   In: Workspace
#   In: Processing Workspace
#   In: Minimum Turbidity Threshold
#   In: Maximum Turbidity Threshold
# ---------------------------------------------------------------

# Import modules
import arcpy
from arcpy.sa import *

# Set the current workspace
arcpy.env.workspace = arcpy.GetParameterAsText(0)

# List of GRIDs from the workspace
rasters = arcpy.ListRasters("*", "GRID")
arcpy.ClearWorkspaceCache_management()

arcpy.env.workspace = arcpy.GetParameterAsText(1)

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

# List of GRIDs from the workspace
rasters = arcpy.ListRasters("*", "GRID")

#Threshold Parameters
minThres = arcpy.GetParameterAsText(2)

#Threshold Parameters
maxThres = arcpy.GetParameterAsText(3)

#Step 1:
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

symbologyRLayer = r"Z:\Miami_Beach\Data\LAYERFILES\TurbiditySTD.lyr"
symbologyLayer = r"Z:\Miami_Beach\Data\LAYERFILES\SANDYBOTTOM.lyr"
    
for raster in rasters:
    desc = arcpy.Describe(raster)
    outputRaster = "{}".format(desc.name)

    #Calculate the Bottom
    arcpy.CalculateStatistics_management(raster)
    turbResult = arcpy.GetRasterProperties_management(arcpy.env.workspace + "\\" + raster, "MAXIMUM")
    
    #Get the elevation standard deviation value from geoprocessing result object
    turbMax = turbResult.getOutput(0)
    remap = RemapRange([[0, 3.5, "NODATA"], [3.5, turbMax, 1]])
    outTurbRec = Reclassify(arcpy.env.workspace + "\\" + raster, "VALUE", remap, "DATA")
    outTurbRec.save(arcpy.env.workspace + "\\" + raster + "_rec")
    arcpy.RasterToPolygon_conversion(arcpy.env.workspace + "\\" + raster + "_rec", outputRaster + "_BOTTOM", "SIMPLIFY", "VALUE")

    # Calculate Coefficient of Variance
    outPoint = raster + "pts"
    arcpy.RasterToPoint_conversion(raster, outPoint, "Value")
    outPointStats = PointStatistics(outPoint, "grid_code", 29.9867417488804, 
                                    NbrCircle(3, "CELL"), "STD")
    outPointStats.save(raster + "_STD")
    RasterLayer = arcpy.MakeRasterLayer_management(raster + "_STD", "TURBIDITY_" + raster, "", "", "")
    
    # Calculate Sand
    outFocalStat = FocalStatistics(arcpy.env.workspace + "\\" + raster, NbrAnnulus(0, 0, "CELL"), "STD", "")
    outFocalStat.save(arcpy.env.workspace + "\\" + raster + "_FS")
    elevSTDResult = arcpy.GetRasterProperties_management(arcpy.env.workspace + "\\" + raster + "_FS", "MAXIMUM")
    # Get the elevation standard deviation value from geoprocessing result object
    elevSTD = elevSTDResult.getOutput(0)
    
    # Execute Reclassify
    print elevSTD
    remap2 = RemapRange([[0, 0.6, "NODATA"], [0.6, elevSTD, 2]])
    outReclassify = Reclassify(arcpy.env.workspace + "\\" + raster + "_FS", "VALUE", remap2, "DATA")
    outReclassify.save(arcpy.env.workspace + "\\" + raster + "_SAND")
    arcpy.RasterToPolygon_conversion(arcpy.env.workspace + "\\" + raster + "_SAND", raster + "_SANDPly", "SIMPLIFY",
                                 "VALUE")

    # Calculate Turbidity
    remap3 = RemapRange([[0, 0.25, "NODATA"], [minThres, maxThres, 3], [0.5, elevSTD, "NODATA"]])
    outRecTurb = Reclassify(arcpy.env.workspace + "\\" + outputRaster + "_FS", "VALUE", remap3, "DATA")
    outRecTurb.save(arcpy.env.workspace + "\\" + raster + "_TURB")
    arcpy.RasterToPolygon_conversion(arcpy.env.workspace + "\\" + raster + "_TURB", raster + "_TURBIDITY1", "SIMPLIFY",
                                 "VALUE")

    arcpy.Clip_analysis(raster + "_TURBIDITY1", outputRaster + "_BOTTOM", raster + "_TURBIDITY", )

    arcpy.Merge_management([raster + "_TURBIDITY", raster + "_BOTTOM", raster + "_SANDPly"], "SANDYBOTTOM_" + raster)

    arcpy.AddField_management("SANDYBOTTOM_" + raster, "TYPE", "TEXT", 25, "", "", "", "NULLABLE", "REQUIRED")

    # Execute MakeFeatureLayer
    arcpy.MakeFeatureLayer_management("SANDYBOTTOM_" + raster, "SANDYLAYER_" + raster)

    expression = 'Shape_Area < 10000' 

    # Execute SelectLayerByAttribute to determine which features to delete
    arcpy.SelectLayerByAttribute_management("SANDYLAYER_" + raster, "NEW_SELECTION", 
                                            expression)
     
    # Execute GetCount and if some features have been selected, then 
    # Execute DeleteFeatures to remove the selected features.
    if int(arcpy.GetCount_management("SANDYLAYER_" + raster).getOutput(0)) > 0:
        arcpy.DeleteFeatures_management("SANDYLAYER_" + raster)

    # Type = BOTTOM
    arcpy.SelectLayerByAttribute_management("SANDYLAYER_" + raster, "NEW_SELECTION", 
                                            """ gridcode = 1 """)
    arcpy.CalculateField_management("SANDYLAYER_" + raster, "TYPE", 
                                    '"' + "BOTTOM" + '"', "PYTHON")
    # Type = SAND
    arcpy.SelectLayerByAttribute_management("SANDYLAYER_" + raster, "NEW_SELECTION", 
                                            """ gridcode = 2 """)
    arcpy.CalculateField_management("SANDYLAYER_" + raster, "TYPE", 
                                    '"' + "SAND" + '"', "PYTHON")
    # Type = TURBIDITY
    arcpy.SelectLayerByAttribute_management("SANDYLAYER_" + raster, "NEW_SELECTION", 
                                            """ gridcode = 3 """)
    arcpy.CalculateField_management("SANDYLAYER_" + raster, "TYPE", 
                                    '"' + "TURBIDITY" + '"', "PYTHON")
    arcpy.SelectLayerByAttribute_management ("SANDYLAYER_" + raster, "CLEAR_SELECTION")
    SandyLayer = arcpy.mapping.Layer("SANDYLAYER_" + raster)
    TurbidityLayer = arcpy.mapping.Layer("TURBIDITY_" + raster)
    arcpy.mapping.AddLayer(df, SandyLayer, "BOTTOM")
    arcpy.mapping.AddLayer(df, TurbidityLayer, "BOTTOM")

# Adds layers to the map
for lyr in arcpy.mapping.ListLayers(mxd, "", df):
    if lyr.name.startswith('TURBID'):
        arcpy.ApplySymbologyFromLayer_management (lyr, symbologyRLayer)
    
    if lyr.name.startswith('SANDY'):
        arcpy.ApplySymbologyFromLayer_management (lyr, symbologyLayer)
        
            
