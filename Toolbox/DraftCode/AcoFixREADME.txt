===============
 AcoFix
===============

Date Created: June 30th, 2017
Last Updated: July 11, 2017

This code is intended to be used as a toolbox in ArcMap. ACOLITE outputs files that are not geolocated, and are often shrunk, rotated, and flipped.
Sometimes the output files also has an extra padding of NoData around them, in addition to any present before. AcoFix lets the user correct these
issues by re-orienting, trimming extra nodata buffers from, scaling up, and geolocating ACOLITE outputs (based on the bottom left hand corner of the image).
If there is a date (YYYYMMDD) present in the title of the file, AcoFix will name the finished product fa_YYMMDD_XXm, where XX is the resolution of the final image, in meters. "fa" stands for
"fixed ACOLITE".

 Required Packages
===================
* ESRI ArcMap
* Arcpy
* Spatial Analyst Extension

 Parameters
-------------
Describe any steps needed for the script to run. It will help to 
specify which line in the code will need to be changed by the user
based on their needs. 

1. Navigate to the toolbox AcoFix is saved under in ArcCatalog, run AcoFix.
2. For "Original image", input the original Landsat 8 or Sentinel 2 scene that was used in ACOLITE.
3. For "Acolite workspace", input the folder or geodatabase where you would like your corrected ACOLITE image to go. This folder/geodatabase
no longer has to contain your ACOLITE output to be corrected, such as in past versions of the software. This folder is also where intermediate files are
created and later deleted. If AcoFix crashes before completion, you may need to manually delete these intermediate files, or look at them to use in debugging.
4. For "Rotate?" and "Flip?", check the boxes if you need to rotate or horizontally flip your ACOLITE output. If you check yes to rotate, you will need to specify 
how many degrees you want your file rotated by in the "Angle of rotation?" box later. Usually this is 180 degrees, although sometimes only 90. 
5. For "Acolite image", input the ACOLITE output that you are trying to correct. This should be a raster file, which you will need to have created from the NetCDF file Acolite outputs.
6. Check "Remove NoData border?" only if there is an extra rectangle of NoData around the edge of your ACOLITE output that was not present around the original satelite image. You can
check for this by changing the symbology of the ACOLITE output layer to "Display NoData as" any color, as by default it does not display. The two user erors encountered most often are checking
this box when it does not need to be checked and forgetting to specify an angle of rotation.
7. Run the program! If it crashes, try changing some options. 
8. If you want to get really into debugging/extending this code, you should know that:
	a. I did most of the editing by right clicking on the script in Windows File Explorer and clicking "Edit with IDLE". I had a separate version of the code to do this, which was a lot of trouble
	   that you could avoid by figuring out how to make print statements work in ArcMap (the print statements currently in the code are left over from this test version). If you did this you could test the tool
	   directly by running it in ArcMap.
	b. I'm pretty new to coding, so my methods are by no means authoritative, just the best I could figure out in a few weeks while also working on other things. So if you see something you think should be changed,
	   go ahead and change it to try to make it work for you. 

 Contact
---------
Name(s): John Colby
E-mail(s): johnrcolby1@gmail.com