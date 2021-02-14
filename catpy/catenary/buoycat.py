# Copyright (c) 2021 CatPy


# Python stdlib imports
import math

# package imports
from catpy.catenary.catpy import (arch_geometry, irvine_method,
                                  line_eq, Coordinates, riser_touchdown,
                                  ArchResults)

#
def CatBuoy(master):
    """ """
    _global = Coordinates(x=delta_u[0], y= 0, z=delta_u[1])
    L_upper = master['L_upper'] - abs(delta_u[0]) 
    d_upper = master['d_upper'] - abs(delta_u[1])
    S_upper = _riser.length_upper - arch_upper.arc_length
    _steps = math.ceil(0.50* S_upper / _riser.diametre)
    upper_cat = irvine_method(L=L_upper, 
                              d=d_upper, 
                              S=S_upper, 
                              w=_riser.unit_weight, 
                              EA = _riser.stiffness_axial * 1e6,
                              global_coord=_global,
                              steps=_steps)
    #
    #
    _global = Coordinates(x= - master['L_lower'],
                          y= 0, z= 0)
    L_lower = master['L_lower'] - abs(delta_l[0])
    S_lower = _riser.length_lower - arch_lower.arc_length
    d_lower = abs(delta_l[1])
    _steps = math.ceil(0.50 * S_lower / _riser.diametre)
    lower_cat = riser_touchdown(L=L_lower, 
                                d=d_lower, 
                                S=S_lower, 
                                w=_riser.unit_weight, 
                                EA = _riser.stiffness_axial * 1e6,
                                Cb=master['Cb'],
                                global_coord=_global,
                                riser_diametre=_riser.diametre)    
