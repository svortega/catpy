# Copyright (c) 2021 CatPy


# Python stdlib imports
from typing import NamedTuple, Union
import math

# package imports
from catpy.catenary.catpy import (arch_geometry, irvine_method,
                                  line_eq, Coordinates, riser_touchdown,
                                  ArchResults)
from catpy.units.main import Units

#
class BuoyData(NamedTuple):
    name: Union[int,str]
    r:float
    L:float
    weigth:float
    buoyancy:float
    CoG:list[float]
#
class RiserData(NamedTuple):
    name: Union[int,str]
    diametre:float
    unit_weight:float
    upper:float
    lower:float
    
    
#
#
#
class CatBuoy:

    __slots__ = ['_buoy', '_riser', 'MSL', 'h_buoy',
                'L_upper', 'L_lower']

    def __init__(self):
        """ """
        self._riser:dict = {}
    

    def midwater_buoy(self, name:Union[int,str], r:Units, L:Units, 
                      weigth:Units, buoyancy:Units, CoG:list[Units]):
        """ Buoy properties
        r : radio
        L : Length
        weigth : dry weigth
        buoyancy: buoyancy"""
        self._buoy = BuoyData(name=name, r=r.value, L=L.value, 
                              weigth=weigth.convert('kilogram').value,
                              buoyancy=buoyancy.convert('kilogram').value,
                              CoG=[CoG[0].value, CoG[1].value, CoG[2].value])


    def riser(self, name:Union[int,str], d:Units, unit_weight:Units,
              upper:Units, lower:Units):
        """
        data : name, d:Units, upper:Units, lower:Units, unit_weight:Units
        """
        self._riser[name] = RiserData(name=name,
                                      diametre=d.value,
                                      unit_weight=unit_weight.convert('kilogram/metre').value,
                                      upper=upper.value,
                                      lower=lower.value)
        #print('--')

    def system(self, MSL:Units, H_buoy:Units,
               L_upper:Units, L_lower:Units):
        """ 
        MSL: 
        L : Horizontal Distance between supports
        d : Vertical Distance between supports
        za : Elevation of higher support from reference plane
        """
        self.MSL = MSL.value
        self.h_buoy = H_buoy.value
        self.L_upper = L_upper.value
        self.L_lower = L_lower.value


    def get_catenary(self, master):
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
