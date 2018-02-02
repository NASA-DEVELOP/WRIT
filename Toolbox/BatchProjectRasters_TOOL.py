##====================================
##Project Raster for Miami Beach Water Resources Project
##Usage: Projects All rasters into desired format using the WGS_1984_(ITRF00)_To_NAD_1983 transformation
## NASA DEVELOP NATIONAL PROGRAM, Summer 2017, Pamela Kanu, pamela.kanu@gmail.com
import arcpy
import os

rootDir = arcpy.GetParameterAsText(0)
arcpy.env.workspace = rootDir

rasters = arcpy.ListRasters("*", arcpy.GetParameterAsText(3))

proEx = arcpy.GetParameterAsText(1)
outDir = arcpy.GetParameterAsText(2)
descEx = arcpy.Describe(proEx)
csEx = descEx.spatialReference.factoryCode

sr = arcpy.SpatialReference(32617)

for raster in rasters:
        arcpy.DefineProjection_management(raster, sr)
        desc = arcpy.Describe(raster)
        arcpy.env.cellSize = raster
        cellSize = arcpy.env.cellSize
        srName = ("{0}".format(sr.factoryCode))
        srExName = ("{0}".format(csEx))
        print srExName
        print srName
        name = raster[:-4] + "_E" + srName + ".tif"
        print name
        arcpy.Rename_management(rootDir + '//' + raster, rootDir + '//' + name)
       
        outRaster = (os.path.join(outDir, name[:-11] + "_E" + srExName + ".tif"))
        print outRaster
        
        arcpy.ProjectRaster_management(name, outRaster, csEx,\
                                   "", cellSize, "WGS_1984_(ITRF00)_To_NAD_1983", "#", "")
print "Your files have been projected"

