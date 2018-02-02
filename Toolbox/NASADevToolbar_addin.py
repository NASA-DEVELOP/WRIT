import arcpy
import pythonaddins
import os
from os.path import expanduser

class ButtonClass15(object):
    """Implementation for NASADevToolbar_addin.button_3 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(os.environ['USERPROFILE'] + r"\Documents\ArcGIS\AddIns\nasadevtoolbar\Install\Water Resources Data Processing.tbx", "netCDF2Raster")

class LandsatAcolite(object):
    """Implementation for NASADevToolbar_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(os.environ['USERPROFILE'] + r"\Documents\ArcGIS\AddIns\nasadevtoolbar\Install\Water Resources Data Processing.tbx", "TXTALCOLITELAN")

class RenameRasters(object):
    """Implementation for NASADevToolbar_addin.button_2 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(os.environ['USERPROFILE'] + r"\Documents\ArcGIS\AddIns\nasadevtoolbar\Install\Water Resources Data Processing.tbx", "RenameRaster")

class SentinelAcolite(object):
    """Implementation for NASADevToolbar_addin.button_1 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog(os.environ['USERPROFILE'] + r"\Documents\ArcGIS\AddIns\nasadevtoolbar\Install\Water Resources Data Processing.tbx", "TXTALCOLITESEN")
