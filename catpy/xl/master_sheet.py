# Copyright (c) 2021 CatPy
#
# Python stdlib imports
from typing import NamedTuple
#
# package imports
import xlwings as xw
#from openpyxl import load_workbook
#
#
class RiserData(NamedTuple):
    """Riser data"""
    name:str
    length_upper:float
    length_lower:float
    unit_weight:float
    diametre:float
    stiffness_axial:float
    stiffness_bending:float
    Y_coordinate:float
    #number:int
#
class ArchData(NamedTuple):
    """
    Arch geometry
    """
    radius:float
    clamp_slot:float
#
def read_master(workbook_name, sheet_name, 
                data_row=14, data_column=20):
    """
    """
    #_number = row_number
    #wb = load_workbook(workbook_name, keep_vba=True)
    # Get sheet names
    sht = xw.sheets[sheet_name]
    #
    # get system data
    #
    Lu = sht.range(data_row, data_column).value
    du = sht.range(data_row + 1, data_column).value
    Ll = sht.range(data_row + 2, data_column).value
    dl = sht.range(data_row + 3, data_column).value
    za = sht.range(data_row + 4, data_column).value    
    MSL = sht.range(data_row + 5, data_column).value
    Cb = sht.range(data_row + 6, data_column).value
    #EA = sht.range(data_row + 7, data_column).value
    riser_type = sht.range(data_row + 7, data_column).value
    #
    # get condition data
    #
    riser_list = sht.range("I21").expand().value
    risers = {}
    _rows = len(riser_list)
    for _row in range(1, _rows):
        _name = riser_list[_row][0]
        risers[_name] = RiserData(*riser_list[_row])
    #
    _arch_radius = sht.range(20, 7).value
    _clamp_slot = sht.range(21, 7).value
    arch = ArchData(radius=_arch_radius, 
                    clamp_slot=_clamp_slot)
    
    # get control data
    #_format = sht.range(control_row, 9).value
    #_design = sht.range(control_row, 10).value
    #_print = sht.range(control_row, 12).expand('down').value
    
    # overwrite data
    #_water_depth = sht.range(29, 4).value
    #_mudline = sht.range(40, 4).value
    #_surface = _mudline + _water_depth
    #
    master = {'L_upper': Lu, 'd_upper': du, 
              'L_lower': Ll, 'd_lower': dl,
              'za': za, 'MSL': MSL, 'Cb':Cb, #'EA' : EA,
              'risers': risers, 'riser_type':riser_type,
              'arch' : arch,
              'workbook_name':workbook_name, 
              'sheet_name':sheet_name}
    #print_input(master, wb)
    return master
#
def print_input(master, wb, sheet_name:str='catenary_res'):
    """
    """
    # writting results to file
    # sht = xw.sheets[fname]
    sht = wb[sheet_name]
    data_column=1
    #
    sht.cell(row=1, column=data_column).value = "Horizontal Distance between supports in meters: ", round(master['L'],3)
    sht.cell(row=2, column=data_column).value = "Catenary length in meters: ", round(master['S'],3)
    sht.cell(row=3, column=data_column).value = "Vertical Distance Between supports in meters: ", round(master['d'],3)
    sht.cell(row=3, column=data_column).value = "Unit Weight of Catenary line in kg/m: ", round(master['w'],3)
    sht.cell(row=4, column=data_column).value = "Elevation of higher support (A) from reference plane in meters: ", round(master['za'],3)
#
#
def print_result(results:dict, workbook_name:str):
    """
    """
    #
    #workbook_name = master['workbook_name']
    #sheet_name = master['sheet_name']
    sheet_name = 'catenary_res'
    #
    sht = xw.sheets[sheet_name]
    #wb = load_workbook(workbook_name, keep_vba=True)
    #sht = wb.active
    #sht = wb[sheet_name]
    #
    a = results['catenary_coefficient']
    H = results['constant_horizontal_tension']
    Va = results['vertical_tension_end_A']
    TA = results['total_tension_end_A']
    TB = results['total_tension_end_B']
    ThetA = results['inclination_angle_from_vertical_end_A']
    ThetB = results['inclination_angle_from_vertical_end_A']
    # writting results to file
    #fname='catenary_res'
    #sht = xw.sheets[fname]
    data_column=1
    sht.range(5, data_column).value = "Catenary coef.: "
    sht.range(5, data_column+1).value = round(a,5)
    sht.range(6, data_column).value = "Horizontal tension in kg (constant along line: "
    sht.range(6, data_column+1).value = round(H,3)
    sht.range(7, data_column).value = "Vertical tension in A in kg: "
    sht.range(7, data_column+1).value = round(Va,3)
    sht.range(8, data_column).value = "Total tension in A in kg: "
    sht.range(8, data_column+1).value = round(TA,3)
    sht.range(9, data_column).value = "Total tension in B in kg: "
    sht.range(9, data_column+1).value = round(TB,3)
    #
    #sht.range(10, data_column).value = "Inclination angle from vertical at A in radians: ", round(ThetA,3)
    #sht.range(11, data_column).value = "Inclination angle from vertical at B in radians: ", round(ThetB,3)
    sht.range(12, data_column).value = "Inclination angle from vertical at A in degrees: "
    sht.range(12, data_column+1).value =  round(ThetA * 180/math.pi, 3)
    sht.range(13, data_column).value = "Inclination angle from vertical at B in degrees: "
    sht.range(13, data_column+1).value = round(ThetB *180/math.pi, 3)
    # save workbook 
    #wb.save(workbook_name)
#
def get_coordinates(a:float, L:float, xb:float, xa:float, MSL:float, 
                    riser_name:str, riser_number:int, workbook_name:str,
                    steps:int =100, sheet_name:str = "catenary_coords"):
    """
    """
    #workbook_name = master['workbook_name']
    #sheet_name = master['sheet_name']
    #sheet_name = "catenary_coords"
    #
    sht = xw.sheets[sheet_name]
    #wb = load_workbook(workbook_name, keep_vba=True)
    #sht = wb[sheet_name]
    #
    #MSL = master['MSL']
    # graphing catenary curve - matplotlib & writting coordinates in file 
    xinc = L / steps
    xc = []
    y = []
    z = []
    #fncoords="catenary_coords"
    #sht = xw.sheets[fncoords]
    data_column=1
    i = 1
    sht.range(i, data_column).value = riser_name
    i+= 1
    sht.range(i, data_column).value = "X-coordinate [m]"
    sht.range(i, data_column+1).value = "Y-coordinate [m]"
    sht.range(i, data_column+2).value = "Z-coordinate [m]"
    for x in np.arange(xb, xa + xinc, xinc):
        i += 1
        zcal = a*math.cosh(x/a)
        xc.append(x)
        y.append(0)
        z.append(zcal - abs(MSL))
        #
        sht.range(i, data_column).value = xc[-1]
        sht.range(i, data_column+1).value = y[-1]
        sht.range(i, data_column+2).value = z[-1]
    #
    return [xc, y, z]
#
#