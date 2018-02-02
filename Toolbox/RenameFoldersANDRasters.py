#Rename folder names and rasters
#Developer Contact Information:
#NASA DEVELOP, Pamela Kanu: psknasadev@gmail.com

import arcpy
import os
#import listdir
from os.path import isfile, join
from os import walk
import glob
arcpy.env.overwriteOutput = True


myPath = arcpy.GetParameterAsText(0)
truncate = arcpy.GetParameterAsText(1)
append = arcpy.GetParameterAsText(2)



workSpace = os.listdir(myPath)
#Set the current workspace
arcpy.env.workspace = myPath

for folder in workSpace:
    if folder.startswith("RAW"):
        pass
    if folder.startswith("ImageList"):
        pass
    #os.rename(folder, folder[int(truncate):])
    os.rename(folder, folder[int(truncate):])

# Get and print a list of GRIDs from the workspace
rasters = arcpy.ListRasters("*", "*")
for raster in rasters:
    rename1 = os.path.splitext(raster)[0]
    desc = arcpy.Describe(raster)
    #print("Layer name: {}".format(desc.name))
    #   os.path.join("fgdb.gdb", fc))
    r1 = desc.name
    newname = append + r1[int(truncate):]
    #print newname
    #print raster
    os.rename((myPath + "\\" + r1), myPath + "\\" + newname)
    print raster
##    #raster.replace("S2A_OPER_MSI_L1C_TL_EPA__", "")
##   # print(raster)
