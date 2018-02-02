# ---------------------------------------------------------------
# File: CreateTXTforRasters_TOOL.py
# Name: TXT File for Landsat Alcolite
# Date: Aug 10, 2017
# Contact: develop.geoinformatics@gmail.com
# NASA DEVELOP, Pamela Kanu, GISP // Contact Info: pamelakanu@gmail.com
# -----------------
# Description: Creates a TXT file for all files with your folder path
# Usage: This is a step needed for ALCOLITE to BATCH the process        
# Parameters:
#   In: Workspace
#   In: Processing Workspace
# ---------------------------------------------------------------

# Import modules
import csv
import os, sys
import arcpy

# Open a file
Path = arcpy.GetParameterAsText(0)
dirs = os.listdir(Path)

# Prints the path and filenames to all the files and directories
with open(Path + "\\" + 'ImageList.txt', 'w') as txtFile:
    for path, subdirs, files in os.walk(Path):
        txtFile.write(path)
        txtFile.write("\n")
        folder_counter = sum([len(subdirs)])
        for subdir in subdirs:
            subdirPath =(os.path.join(path,subdir))
    if folder_counter != 0:
        txtFile.write(subdirPath)
        txtFile.write("\n")
# Prints a txt file named "ImageList" in the same directory              
txtFile.close()
print "Your file is named: ImageList.txt and is located in your input folder"
        
