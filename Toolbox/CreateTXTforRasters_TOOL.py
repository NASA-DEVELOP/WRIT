# Creates a TXT file for all files with your folder path
# This is a step needed for ALCOLITE to BATCH the process
# Pamela Kanu, NASA DEVELOP National Program - Summer 2017, psknasadev@gmail.com

import csv
import os, sys
from Tkinter import *
import sys
import arcpy

# Open a file
Path = arcpy.GetParameterAsText(0)
#Path = r"C:\Miami_Beach\Data\IMAGERY\Landsat8"
dirs = os.listdir(Path)

# This would print all the files and directories
with open(Path + "\\" + 'ImageList.txt', 'w') as txtFile:
    for path, subdirs, files in os.walk(Path):
        #for file in files:
        #file_counter = sum([len(files)
            #if file.endswith(param1):
        #if param1 in path:
            #fileList.append(file)
        txtFile.write(path)
        txtFile.write("\n")
        folder_counter = sum([len(subdirs)])
        for subdir in subdirs:
            subdirPath =(os.path.join(path,subdir))
            #print folder_counter
    if folder_counter != 0:
        txtFile.write(subdirPath)
        txtFile.write("\n")
              
txtFile.close()
print "Your file is named: ImageList.txt and is located in your input folder"
        
