#Convert netCDF to Rasters
# Description: Batches netCDF files to rasters in ArcGIS 
#Developer Contact Information:
#NASA DEVELOP, Pamela Kanu: psknasadev@gmail.com

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
#inNetCDFFile = r"C:\Users\ejsimons\Desktop\ACOLITE\Processed_Test\T18SUG\3_17_2017_2\S2A_OPER_MSI_L1C_TL_MTI__20170317T205407_A009060_T18SUG_N02.04_L2.nc"
variableList = [arcpy.GetParameterAsText(1)]

XDimension = "x"
YDimension = "y"
#outRasterLayer = "rainfall"
bandDimmension = ""
dimensionValues = ""
valueSelectionMethod = ""

#out_layer_file = r"C:\GIS Data\Study Area\TEST_Netcdf.ly"


for root, dirs, files in os.walk(arcpy.env.workspace):
    for name in files:
        if ".nc" in name:
            # DO I REALLY WANT TO DO THIS?
            if "RGB" not in name:
                netCDF = (os.path.join(root, name))
                #netCDF = (os.path.join(root, name))
                netCDFs.append(name)
                #print netCDFs
        
            for net in netCDFs:
                print net
                for var in variableList:
                    #outRasterLayer = ((net)[:-3] +"_"+var + "_2.ly").replace("\\", "/")
                    #netPath = ((net)[:-3] +"_"+var + "_2.ly").replace("\\", "/")
                    lyrName = (os.path.join(root, net))[:-3] + ".lyr"
                    print lyrName
####                    RasterLayer = (net.split(".nc")[0]+"_"+var)#.replace("\\", "/")
                    RasterLayer = ((netCDF)[:-3] +"_"+var + ".tif")
                    
                    arcpy.MakeNetCDFRasterLayer_md(netCDF, var, XDimension, YDimension,
                                                       lyrName, bandDimmension, dimensionValues, 
                                                       valueSelectionMethod)
##                    # Execute SaveToLayerFile - You may need this to symbolize the rasters later
##                    #arcpy.SaveToLayerFile_management(outRasterLayer, out_layer_file, "ABSOLUTE")
                    arcpy.CopyRaster_management(lyrName,RasterLayer,"DEFAULTS","","","","","32_BIT_FLOAT")
