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
#Path = r"C:\Miami_Beach\Data\IMAGERY\Sentinel2\S2A_OPER_PRD_MSIL1C_PDMC_20161207T164538_R054_V20151004T160016_20151004T160016.SAFE"
dirs = os.listdir(Path)
#print dirs
##
## This would print all the files and directories
with open(Path + "\\" + 'ImageList.txt', 'w') as txtFile:
#for path, subdirs, files in os.walk(Path):
    folderCount = sum([len(os.walk(Path).next()[1])])
    for folder in os.walk(Path).next()[1]:
        
       # folderCo = (folderCount - 1)
       # for i in range(folderCount):
       #     if i != folderCo:
        fldPath = (os.path.join(Path,folder))
        txtFile.write('"' + fldPath + '",')
            #txtFile.write("\n")
    txtFile.seek(-1, os.SEEK_END)
    txtFile.truncate()
            #if i == folderCo:
             #   print folder # prints 3
                    #print folder
               # txtFile.write(fldPath)
        
txtFile.close()
print "Your file is named: ImageList.txt and is located in your input folder"
        

