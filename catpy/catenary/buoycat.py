# Copyright (c) 2021 CatPy


# Python stdlib imports
from typing import NamedTuple, Union, List
import math

# package imports
from catpy.catenary.catpy import(irvine_method, line_eq, 
                                 Coordinates, riser_touchdown,
                                 MidArchResults)
from catpy.units.main import Units
from catpy.usfos.geometry import geometry_ufo

#
class BuoyData(NamedTuple):
    name: Union[int,str]
    r:float
    L:float
    weigth:float
    buoyancy:float
    CoG:List[float]
#
class RiserData(NamedTuple):
    name: Union[int,str]
    diametre:float
    k_axial:float
    k_bending:float
    unit_weight:float
    upper:float
    lower:float
    
    
#
#
#
class CatBuoy:

    __slots__ = ['_buoy', '_riser', 'MSL', 'Cb',
                 'h_upper', 'h_lower', 'L_upper', 'L_lower']

    def __init__(self):
        """ """
        self._riser:dict = {}
        self.Cb = 1.0 # soil friction

    def midwater_buoy(self, name:Union[int,str], r:Units, L:Units, 
                      weigth:Units, buoyancy:Units, CoG:List[Units]):
        """ Buoy properties
        r : radio
        L : Length
        weigth : dry weigth
        buoyancy: buoyancy"""
        self._buoy = BuoyData(name=name, r=r.value, L=L.value, 
                              weigth=weigth.convert('kilogram').value,
                              buoyancy=buoyancy.convert('kilogram').value,
                              CoG=[CoG[0].value, CoG[1].value, CoG[2].value])


    def riser(self, name:Union[int,str], d:Units, 
              k_axial:Units, k_bending:Units,
              unit_weight:Units,
              upper:Units, lower:Units):
        """
        data : name, d:Units, upper:Units, lower:Units, unit_weight:Units
        """
        self._riser[name] = RiserData(name=name,
                                      diametre=d.value,
                                      k_axial = k_axial.convert('newton').value,
                                      k_bending = k_bending.convert('newton/metre^2').value,
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
        self.h_upper = H_buoy.value
        self.h_lower = self.MSL - H_buoy.value
        self.L_upper = L_upper.value
        self.L_lower = L_lower.value


    def get_catenary(self, riser):
        """ """
        #_global = Coordinates(x=delta_u[0], y= 0, z=delta_u[1])
        _global = Coordinates(x= self._buoy.r, y= 0, z= self.h_lower)
        _steps = math.ceil(0.50* riser.upper / riser.diametre)
        upper_cat = irvine_method(L=self.L_upper, 
                                  d=self.h_upper, 
                                  S=riser.upper, 
                                  w=riser.unit_weight, 
                                  EA = riser.k_axial,
                                  global_coord=_global,
                                  steps=_steps)
        #
        #
        _global = Coordinates(x= -self.L_lower-self._buoy.r, y= 0, z= 0)
        #L_lower = master['L_lower'] - abs(delta_l[0])
        #S_lower = _riser.length_lower - arch_lower.arc_length
        #d_lower = abs(delta_l[1])
        _steps = math.ceil(0.50 * riser.lower / riser.diametre)
        #lower_cat = riser_touchdown(L=self.L_lower, 
        #                            d=self.h_lower, 
        #                            S=riser.lower, 
        #                            w=riser.unit_weight, 
        #                            EA = riser.k_axial,
        #                            Cb=self.Cb,
        #                            global_coord=_global,
        #                            riser_diametre=riser.diametre)
        #
        lower_cat = irvine_method(L=self.L_lower, 
                                  d=self.h_lower, 
                                  S=riser.lower, 
                                  w=riser.unit_weight, 
                                  EA = riser.k_axial,
                                  global_coord=_global,
                                  steps=_steps)
        #
        buoy_coord = [[0],[0],[self.h_lower]]
        #
        x_coord = lower_cat.coordinates.x + buoy_coord[0] + upper_cat.coordinates.x
        y_coord = lower_cat.coordinates.y + buoy_coord[1] + upper_cat.coordinates.y
        z_coord = lower_cat.coordinates.z + buoy_coord[2] + upper_cat.coordinates.z
        #plot_chart(x_coord, z_coord)
        return MidArchResults(buoy= [],
                              catenary_upper= upper_cat,
                              catenary_lower= lower_cat,
                              catenary=Coordinates(x_coord, y_coord, z_coord))
    #
    def print_model(self):
        """ """
        results = {}
        for key, riser in self._riser.items():
            results[key] = self.get_catenary(riser)
        #
        for key, _riser in results.items():
            geometry_ufo(_riser, water_depth=self.MSL)
        print("---")
