# 
# Copyright (c) 2019 iLift
# 

# Python stdlib imports


# package imports
#import iLift.units.control as unit_control
from catpy.units.buckingham import Number



#
class Units:
    
    def __init__(self):
        """
        Units [length, mass, time, temperature, force, pressure/stress]
        """
        #self._units = ["", "", "second", "", "", ""]
        pass
    #
    def __getattr__(self, key):
        """
        """
        #_item = unit_control.find_unit_case(key)
        #
        # mass
        if key.lower() in ['g', 'gram', 'gramme']:
            return Number(1, dims = 'gram')
        elif key.lower() in ['kg', 'kilogram', 'kilogramme']:
            return Number(1, dims = 'kilogram')        
        elif key.lower() in ['tonne', 't', 'metric_ton']:
            return Number(1, dims = 'megagram')
        elif key.lower() in ['lb', 'lbs', 'pound']:
            return Number(1, dims = 'pound')
        elif key.lower() in ['slug']:
            return Number(1, dims = 'lbf * second^2 / foot')
        elif key.lower() in ['st', 'stone', 'stone_weight']:
            return Number(14, dims = 'pound')
        elif key.lower() in ['long_ton', 'imperial_ton', 'displacement_ton']:
            return  Number(2_440, dims = 'pound')
        elif key.lower() in ['ton', 'short_ton']:
            return Number(2_000, dims = 'pound')
        # grav
        elif key.lower() in ['g0', 'gn', 'gravity']:
            return Number(9.80665, dims = 'metre/second^2')
        # time
        elif key.lower() in ['s', 'second', 'sec']:
            return Number(1, dims = 'second')
        elif key.lower() in ['min', 'minute', 'minutes']:
            return Number(1, dims = 'minute')
        elif key.lower() in ['h', 'hr', 'hour', 'hours']:
            return Number(1, dims = 'hour')
        # length 
        elif key.lower() in ['m', 'metre', 'metres', 'meter', 'meters']:
            return Number(1, dims = 'metre')
        elif key.lower() in ['km', 'kilometre', 'kilometres', 'kilometer', 'kilometers']:
            return Number(1, dims = 'kilometre')
        elif key.lower() in ['dm', 'decimetre', 'decimetres', 'decimeter', 'decimeters']:
            return Number(1, dims = 'decimetre')
        elif key.lower() in ['cm', 'centimetre', 'centimetres', 'centimeter', 'centimeters']:
            return Number(1, dims = 'centimetre')
        elif key.lower() in ['mm', 'millimetre', 'millimetres', 'millimeter', 'millimeters']:
            return Number(1, dims = 'millimetre')
        elif key.lower() in ['inch']:
            return Number(1, dims = 'inch')
        elif key.lower() in ['ft', 'foot', 'feet']:
            return Number(1, dims = 'foot')
        elif key.lower() in ['yr', 'yard', 'yards']:
            return Number(1, dims = 'yard')
        elif key.lower() in ['mi', 'mile', 'miles']:
            return Number(1, dims = 'mile')
        elif key.lower() in ['nmi', 'nq', 'nautical_mile']:
            return Number(6080, dims = 'foot')
        # speed
        elif key.lower() in ['mph']:
            return Number(1, dims = 'mile/hour')
        elif key.lower() in ['knot']:
            return Number(6080, dims = 'foot/hour')
        # temperature
        elif key.lower() in ['k', 'kelvin']:
            return Number(1, dims = 'kelvin')
        elif key.lower() in ['c','oc', 'c_degrees', 'cdeg', 'celsius']:
            return Number(1, dims = 'kelvin') + 273.15
        elif key.lower() in ['of', 'f_degrees', 'fdeg', 'fahrenheit']:
            return (Number(1, dims = 'kelvin') + 459.67) * 5/9
        elif key.lower() in ['or', 'r_degrees', 'rdeg', 'rankine']:
            return Number(1, dims = 'kelvin') * 5/9
        # force
        elif key.lower() in ['n', 'newton']:
            return Number(1, dims = 'newton')
        elif key.lower() in ['kn', 'kilonewton']:
            return Number(1, dims = 'kilonewton')
        elif key.lower() in ['mn', 'meganewton']:
            return Number(1, dims = 'meganewton')
        elif key.lower() in ['gn', 'giganewton']:
            return Number(1, dims = 'giganewton')
        elif key.lower() in ['lbf', 'pound_force']:
            return Number(1, dims = 'lbf')
        elif key.lower() in ['kip', 'kips', 'kipf', 'klbf']:
            return  Number(1, dims = 'kilolbf')
        elif key.lower() in ['pdl', 'poundal']:
            return Number(1, dims = 'pound * foot / second^2')
        # pressure
        elif key.lower() in ['pa', 'pascal']:
            return Number(1, dims = 'pascal')
        elif key.lower() in ['kpa', 'kilopascal']:
            return Number(1, dims = 'kilopascal')
        elif key.lower() in ['mpa', 'bar', 'megapascal']:
            return  Number(1, dims = 'megapascal')
        elif key.lower() in ['gpa', 'gigapascal']:
            return Number(1, dims = 'gigapascal')
        elif key.lower() in ['mbar', 'mb', 'hectopascal']:
            return Number(1, dims = 'hectopascal')
        elif key.lower() in ['psf']:
            return Number(1, dims = 'lbf / foot^2')
        elif key.lower() in ['psi']:
            return Number(1, dims = 'psi')
        elif key.lower() in ['ksi']:
            return Number(1, dims = 'kilopsi')
        # energy 
        elif key.lower() in ['w', 'watt']:
            return Number(1, dims = 'watt')
        elif key.lower() in ['j', 'joule']:
            return Number(1, dims = 'joule')
        elif key.lower() in ['hp']:
            return Number(33000, dims = 'foot * lbf / minute')        
        # angle
        elif key.lower() in ['rad', 'radian', 'radians']:
            return Number(1, dims = 'radian')        
        elif key.lower() in ['deg', 'degree', 'degrees']:
            return Number(1, dims = 'degree')
        elif key.lower() in ['arcmin']:
            return Number(1/60., dims='degree')
        elif key.lower() in ['arcsec']:
            return Number(1/120., dims='degree')
        else:
            raise Exception(" unit item {:} not recognized".format(key))
    #
    #def __setattr__(self, key, value):
    #    """
    #    """
    #    #_item = unit_control.find_unit_case(key)
    #    
    #    if key == 'kg':
    #        self._mass = Number(1, dims = 'kilogram')
    #    else:
    #        super().__setattr__(key, value)
    #
    def output(self):
        """
        """
        print('output')
    #
    #
    #def __copy__(self):
    #    cls = self.__class__
    #    result = cls.__new__(cls)
    #    result.__dict__.update(self.__dict__)
    #    return result
    #
    #def __deepcopy__(self, memo):
    #    cls = self.__class__
    #    result = cls.__new__(cls)
    #    memo[id(self)] = result
    #    for k, v in self.__dict__.items():
    #        setattr(result, k, copy.deepcopy(v, memo))
    #    return result    



    