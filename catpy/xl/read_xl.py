# Copyright (c) 2019 CatPy
#
# Python stdlib imports
#import math
import os

# package imports
#import xlwings as xw
from catpy.xl.master_sheet import read_master
from catpy.catenary.rsscat import CatRSS
from catpy.usfos.geometry import geometry_ufo
#
#
#
#
def get_riser():
    """
    """
    # get excel workbook
    wb = xw.Book.caller()
    #
    # get sheet naming
    sheet_name = wb.sheets.active.name
    path_name = xw.sheets[sheet_name].range('T1').value
    workbook_name = xw.sheets[sheet_name].range('T2').value
    #workbook_name = path_name +'\\'+ workbook_name
    #
    # get sheet path
    path = os.path.normcase(path_name)
    # change working directory
    os.chdir(path)
    #
    # get master sheet data
    master = read_master(workbook_name, sheet_name)
    #
    # Calculate catenary
    master['coordinates'] = CatRSS(master, workbook_name)
    #
    #master['coordinates'] = coord
    # print ufo 
    for key, _riser in master['coordinates'].items():
        geometry_ufo(_riser, water_depth=master['MSL'])
    #
    print('end')
#
#