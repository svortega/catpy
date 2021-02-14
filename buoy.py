# Copyright (c) 2021 CatPy
#
# Python stdlib imports
import math

# package imports
import catpy as cty

#
units = cty.Units()
test = cty.CatBuoy()
#
# caternaries
# 20" hose with 40' length each
# riser = [name, diamtre, unit_weight, upper_cat, lower_cat]
hose_lenght = 40*units.feet
hose_diam = 20*units.inch
op_weight = 890 * units.kg/units.m**3
unit_weight = op_weight * math.pi * (hose_diam/2)**2
test.riser(name="20in_hose", d=hose_diam, 
           unit_weight=unit_weight,
           upper=hose_lenght * 5, 
           lower=hose_lenght * 3)
#
# buoy dimensions
test.midwater_buoy(name="Ceiba_buoy", 
                   r=1.25 * units.m,
                   L=3.26 * units.m,
                   weigth=7091 * units.kg,
                   buoyancy=8762 * units.kg,
                   CoG=[0*units.m, 0*units.m, 0*units.m])
#
# System Data
# water depth 
LAT = 67.0 * units.m
HAT = 69.5 * units.m
Hbuoy = LAT - 29 * units.m
Lt = 40 * units.m
L1 = 10 * units.m ## guess
test.system(MSL= LAT, H_buoy=Hbuoy,
            L_upper=Lt-L1, L_lower=L1)
#
#
print('-->')

