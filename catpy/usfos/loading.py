# Copyright (c) 2019 CatPy


# Python stdlib imports
#from typing import NamedTuple, Dict

# package imports
#from catpy.usfos.headers import print_head_line, print_EOF



def print_gravity():
    """
    """
    UFOmod = []
    #_iter = 0
    #for _key, _load in sorted(load.items()):
        #try:
            #_try = 1.0 / len(_load.gravity)
    UFOmod.append("' \n")
    UFOmod.append("' \n")
    UFOmod.append("'{:} Gravity Load\n".format(70 * "-"))
    UFOmod.append("' \n")
    UFOmod.append("'          Load Case         Acc_X        Acc_Y        Acc_Z\n")
    UFOmod.append("' \n")
    UFOmod.append(" GRAVITY           1   0.00000E+00  0.00000E+00 -9.80665E+00")
    UFOmod.append("\n")
        #except ZeroDivisionError:
        #    pass
    return UFOmod