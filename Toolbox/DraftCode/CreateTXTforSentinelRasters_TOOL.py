# ---------------------------------------------------------------
# File: CreateTXTforSentinelRasters_TOOL .py
# Name: TXT File for Sentinel Alcolite
# Date: Aug 10, 2017
# Contact: develop.geoinformatics@gmail.com
# NASA DEVELOP, Pamela Kanu, GISP // Contact Info: pamelakanu@gmail.com
# -----------------
# Description: Creates a TXT file for all files with your folder path
# Usage: This is a step needed for ALCOLITE to BATCH the process.
# This tool generates the list with commas. This tool can be used interchangebly
# with Landsat and Sentinel batch process by copying the list to the batch path
# Parameters:
#   In: Workspace
# ---------------------------------------------------------------

# Import modules
import csv
import os, sys
import arcpy

# Open a file
Path = arcpy.GetParameterAsText(0)
dirs = os.listdir(Path)

## Prints the path and filenames to all the files and directories
with open(Path + "\\" + 'ImageList.txt', 'w') as txtFile:
    folderCount = sum([len(os.walk(Path).next()[1])])
    for folder in os.walk(Path).next()[1]:
        fldPath = (os.path.join(Path,folder))
        # Adds the ',' between each raster path name
        txtFile.write('"' + fldPath + '",')
    # Deletes the last comma in the text file    
    txtFile.seek(-1, os.SEEK_END)
    txtFile.truncate()       
txtFile.close()
print "Your file is named: ImageList.txt and is located in your input folder"
        

