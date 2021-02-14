# !usr/bin/env python
# Copyright (c) 2021 CatPy

# Python stdlib imports
import math
#from typing import NamedTuple, Tuple, List

# package imports
from catpy.catenary.catpy import (arch_geometry, irvine_method,
                                  line_eq, Coordinates, riser_touchdown,
                                  ArchResults)


#
def CatRSS(master):
    """
    """
    riser_type = master['riser_type']
    risers = master['risers']
    #
    # Calculate catenary
    results = {}
    #coord = {}
    #riser_no = 0
    for key, _riser in risers.items():
        #riser_no += 1 
        #
        if 'arch' in riser_type.lower():
            _arch =master['arch']
            print('Arch')
            print('')
            print('Upper catenary')
            _global = Coordinates(x= 0, y= 0, z= 0)
            angle_segment = 16
            angle = 90 / angle_segment
            arch_upper = arch_geometry(radius=_arch.radius, 
                                       clamp_slot=_arch.clamp_slot,
                                       d_arch = master['d_lower'],
                                       riser_diametre=_riser.diametre,
                                       theta = angle * 10,
                                       global_coord=_global)
            arch_x_u = arch_upper.slot.x + arch_upper.circle.x
            arch_z_u = arch_upper.slot.z + arch_upper.circle.z
            arch_y_u = arch_upper.slot.y + arch_upper.circle.y
            #plot_chart(arch_x_u, arch_z_u)
            delta_u = line_eq(coord_1=(arch_upper.circle.x[-2], arch_upper.circle.z[-2]), 
                              coord_2=(arch_upper.circle.x[-1], arch_upper.circle.z[-1]))            
            #
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
            #plot_chart(upper_cat.coordinates.x, upper_cat.coordinates.z)
            #
            print('')
            print('Lower catenary')
            _global = Coordinates(x= 0, y= 0, z= 0)
            arch_lower = arch_geometry(radius=_arch.radius, 
                                       clamp_slot=_arch.clamp_slot,
                                       d_arch = master['d_lower'],
                                       riser_diametre=_riser.diametre,
                                       theta = angle * 12, 
                                       global_coord=_global,
                                       reverse=True)
            #
            arch_x_l =  arch_lower.circle.x + arch_lower.slot.x
            arch_z_l =  arch_lower.circle.z + arch_lower.slot.z
            arch_y_l =  arch_lower.circle.y + arch_lower.slot.y
            #plot_chart(arch_x_l, arch_z_l)
            delta_l = line_eq(coord_1=(arch_lower.circle.x[1], arch_lower.circle.z[1]), 
                              coord_2=(arch_lower.circle.x[0], arch_lower.circle.z[0]))
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
            #plot_chart(lower_cat.coordinates.x, lower_cat.coordinates.z)
            #plot_chart(lower_cat.x, lower_cat.z)
            #
            x_coord = lower_cat.coordinates.x + arch_x_l + arch_x_u + upper_cat.coordinates.x
            z_coord = lower_cat.coordinates.z + arch_z_l + arch_z_u + upper_cat.coordinates.z
            y_coord = lower_cat.coordinates.y + arch_y_l + arch_y_u + upper_cat.coordinates.y
            #
            #plot_chart(x_coord, z_coord)
            results[key] = ArchResults(arch_upper= arch_upper,
                                       catenary_upper= upper_cat,
                                       arch_lower= arch_lower,
                                       catenary_lower= lower_cat,
                                       catenary=Coordinates(x_coord, y_coord, z_coord))
        else:
            raise NotImplemented("Riser type {:} not yet implemented".format(riser_type))
        #
    #
    #print('end')
    return results
#
