# 
# Copyright (c) 2019 iLift
# 

# Python stdlib imports


# package imports
from iLift.process.units.buckingham import Number
from iLift.process.io_module.text import match_line, search_line


#
def find_length_unit(lineIn):
    """
    """
    _key = {"metre" :r"\b(m(et[r]?e[r]?[s]?)?)\b",
            "decimetre" : r"\b(d(eci\s*)?m(et[r]?e[r]?[s]?)?)\b",
            "centimetre" : r"\b(c(enti\s*)?m(et[r]?e[r]?[s]?)?)\b",
            "millimetre" : r"\b(m(illi\s*)?m(et[r]?e[r]?[s]?)?)\b",
            "decametre" : r"\b(d(e[ck]?)?am(et[r]?e[r]?[s]?)?)\b",
            "hectometre" : r"\b(h(ecto\s*)?m(et[r]?e[r]?[s]?)?)\b",
            "kilometre" : r"\b(k(ilo\s*)?m(et[r]?e[r]?[s]?)?)\b",
            "nanometre" : r"\b(n(ano\s*)?m(et[r]?e[r]?[s]?)?)\b",
            "micrometre" : r"\b(micro[n]?|u(m(et[r]?e[r]?[s]?)?)?)\b",
            # US units
            "foot" : r"\b(f(oo|ee)?t|\')\b",
            "inch" : r"\b(in(ch(es)?)?|\"|\'')\b",
            "yard" : r"\b(y(ar)?d[s]?)\b",
            "mile" : r"\b((statute|land)?mi(le[s]?)?)\b"}
    
    keyWord, lineOut, _match = search_line(lineIn, _key)
    
    
    return keyWord
#
def find_mass_unit(lineIn):
    """
    """
    _key = {"gram" :r"\b(g(ram(me)?[s]?)?)\b",
            "decigram" :r"\b(d(eci)?g(ram(me)?[s]?)?)\b",
            "centigram" :r"\b(c(enti)?g(ram(me)?[s]?)?)\b",
            "milligram" :r"\b(m(illi)?g(ram(me)?[s]?)?)\b",
            "microgram" :r"\b((m[i]?c(ro)?|u)g(ram(me)?[s]?)?)\b",
            "nanogram" :r"\b(n(ano)?g(ram(me)?[s]?)?)\b",
            "picogram" :r"\b(p(ico)?g(ram(me)?[s]?)?)\b",
            "kilogram" :r"\b(k(ilo)?g(ram(me)?[s]?)?)\b",
            "hectogram" :r"\b(h(ecto)?g(ram(me)?[s]?)?)\b",
            "decagram" :r"\b(d(e[ck]?)?ag(ram(me)?[s]?)?)\b",
            "megagram" :r"\b((M|mega\s*)g(ram(me)?[s]?)?|(metric\s*)?tonne[s]?)\b",
            # US units
            "pound" : r"\b((gee)?(pound[s]?|lb)(\s*m(ass)?)?)\b",
            "2000*pound" : r"\b((short\s*)?ton)\b",
            "2240*pound" : r"\b((long|weight|imperial)\s*ton)\b"}
    
    keyWord, lineOut, _match = search_line(lineIn, _key)
    
    return keyWord     
#
def find_force_unit(lineIn):
    """
    """
    _key = {"newton" :r"\b(N|newton[s]?)\b",
            "kilonewton" :r"\b(k(ilo\s*)?N|newton[s]?)\b",
            "meganewton" :r"\b((M|mega\s*)N|newton[s]?)\b",
            # US units
            "lbf" : r"\b((pound[s]?|lb)\s*f(orce)?)\b",
            "1000*lbf" : r"\b(k[i]?(lo)?(p(ound[s]?)?|lb)\s*f(orce)?)\b"}
    
    keyWord, lineOut, _match = search_line(lineIn, _key)
    
    return keyWord     
#
def find_pressure_unit(lineIn):
    """
    """
    # stress
    _key = {"pascal" :r"Pa|pascal[s]?",
            "hectopascal" :r"h(ecto\s*)?Pa|pascal[s]?",
            "kilopascal" :r"k(ilo\s*)Pa|pascal[s]?",
            "megapascal" :r"(M|mega\s*)Pa|pascal[s]?|((N|newton[s]?)\/(m(illi)?m(et[r]?e[r]?[s]?)?(\**|\^)?2))",
            "gigapascal" :r"(G|giga\s*)Pa|pascal[s]?",
            # pressure
            "bar" :r"bar",
            "megabar" :r"(M|mega\s*)bar",
            "kilobar" :r"k(ilo\s*)bar",
            "decibar" :r"d(eci\s*)?bar",
            "centibar" :r"c(enti\s*)?bar",
            "millibar" :r"m(illi\s*)?b(ar)?",
            # US units
            "psi" : r"(p(ound[s]?)?|lb)\s*f(orce)?(\s*per|\/)?(\s*s(quare)?)\s*i[n]?(che[s]?)?((\**|\^)?2))?",
            "kilopsi" : r"k(ilo\s*)((p(ound[s]?)?|lb)\s*f(orce)?)?(\s*per|\/)?(\s*s(quare)?)\s*i[n]?(che[s]?)?((\**|\^)?2))?"}
    
    keyWord, lineOut, _match = search_line(lineIn, _key)
    
    return keyWord 
#
def find_temperature_unit(lineIn):
    """
    """
    _key = {"kelvin+273.15" :r"\b(c(entigrade[s]?)?)\b",
            "kelvin" :r"\b(k(elvin[s]?)?)\b",
            # US units
            "(kelvin+459.67)*5.0/9.0" : r"\b(f(ahrenheit)?)\b"}
    
    keyWord, lineOut, _match = search_line(lineIn, _key)
    
    return keyWord     
#
# Acceleration
def find_acceleration_unit(lineIn):
    """
    """
    _key = {"9.80665 metre/second^2" : r"\b(g(ravity)?)\b"}
    
    keyWord, lineOut, _match = search_line(lineIn, _key)
    
    return keyWord    
#
# ---
#
def find_unit_case(word_in):
    
    _key = {"length" : r"\b(l(a|e)ng(th|[d]?e)?|long(itud|ueur)?|largo)\b",
            "force" : r"\b(force|fuerza|kraft)\b",
            "mass" : r"\b(mass(e[n]?)?|masa)\b",
            "temperature" : r"\b(temp(eratur(e|a)?)?)\b",
            "acceleration" : r"\b(acc(eleration)?)\b",}
    
    #
    _match = match_line(word_in, _key)
    
    if not _match:
        raise IOError('  **  error unit {:} not recognized'.format(word_in))
    
    return _match
#
def units_module(_unit, item, _unit_list=False):               
    """
    Units [length, mass, time, temperature, force, pressure/stress]
    """
    if not _unit_list:
        _unit_list = ["", "", "second", "", "", ""]
    
    if _unit == 'length':
        item = find_length_unit(item)
        _unit_list[0] = item
    
    elif _unit == 'mass'  : 
        item = find_mass_unit(item)
        _unit_list[1] = item
    
    elif _unit == 'time'  : 
        item = find_mass_unit(item)
        _unit_list[2] = item
    
    elif _unit == 'temperature'  : 
        item = find_mass_unit(item)
        _unit_list[3] = item
    
    elif _unit == 'force' : 
        item = find_force_unit(item)
        _unit_list[4] = item
    
    elif _unit == 'pressure' : 
        item = find_force_unit(item)
        _unit_list[5] = item
    
    elif _unit == 'acceleration' :
        item = find_acceleration_unit(item)
        _unit_list[5] = item
    
    else: 
        raise IOError('  **  erorr unit {:} not recognized'.format(_unit))
    
    return _unit_list
#
# ---
#
#
def find_unit_system(_InputUnit):
    #
    _english = ['foot',' inch', 'mile', 'nautical-mile', 'fathom', 'yard', 'rod', 'furlong',
                'pound', 'slug', 'pound-force', 'ounce-force', 'pound', 'ounce', 'ton', 'long-ton',
                'hundredweight', 'dram' 'grain', 'pennyweight', 'scruple', 'acre', 'square-mile',
                'cubic-inch', 'cubic-foot', 'cubic-yard', 'cubic-mile', 'acre-foot', 'gallon',
                'quart', 'peck', 'bushel', 'fifth', 'pint', 'cup', 'fluid-ounce', 'gill', 'fluidram',
                'minim', 'tablespoon', 'teaspoon', 'foot-pound', 'horsepower-hour', 'grain',
                'horsepower', 'british-thermal-unit', 'btu', 'pounds-per-square-inch', 'psi',
                'miles-per-hour', 'miles-per-second', 'feet-per-second', 'knot',
                'square-foot', 'square-yard', 'square-inch']
    #
    _outUnit = 'si'
    for _item in _english:
    
        if _InputUnit in _item:
            _outUnit = 'us'
            break

    #
    return _outUnit
    #
#
#
def get_length_mass(_input, _output):
    """
    factors : Units [length, mass, time, temperature, force, pressure/stress]
    """
    # Input units
    factors = [0, 0, 0, 0, 0, 0]
    # length
    _dim0 = _input[0] 
    _length = Number(1, dims = _dim0)
    #  set units
    _dim0out = _output[0]
    factors[0] = _length.convert(_dim0out).value    
    
    if _input[1]:
        _dim1 = _input[1]
    else:
        _dim1 = 'kilogram'
        _unit_guess = find_unit_system(_input[0])
        if _unit_guess == 'us':
            _dim1 = 'pound'
        _input[1] = _dim1
    
    if _output[1]:
        _dim1out = _output[1]
    else:
        _dim1out = 'kilogram'
        _unit_guess = find_unit_system(_output[0])
        if _unit_guess == 'us':
            _dim1out = 'pound'
        
        _output[1] = _dim1out
    
    _mass_temp = Number(1, dims = _dim1)
    factors[1] = _mass_temp.convert(_dim1out).value
    
    return factors
#
def get_factors_and_gravity(_input, _output):
    """
    factors : Units [length, mass, time, temperature, force, pressure/stress]
    """
    # Input units
    factors = [0, 0, 0, 0, 0, 0]
    #
    # length
    _dim0 = _input[0] 
    _length = Number(1, dims = _dim0)
    # time
    _dim2 = _input[2]
    # force
    _dim4 = _input[4]
    _force = Number(1, dims = _dim4)
    # pressure
    try:
        _dim5 = _input[5]
        if not _dim5:
            _dim5 = str(_dim4)+ '/' + str(_dim0) + '^2'
    except IndexError:
        _dim5 = str(_dim4)+ '/' + str(_dim0) + '^2'
    _pressure = Number(1, dims = _dim5)
    # grav
    gravity = Number(9.80665, dims = 'metre')
    
    #  set units
    _dim0out = _output[0]
    _grav = gravity.convert(_dim0out).value
    factors[0] = _length.convert(_dim0out).value
    
    _dim4out = _output[4]
    factors[4] = _force.convert(_dim4out).value 
    
    try:
        _dim5out = _output[5]
        if not _dim5out:
            _dim5out = str(_dim4out)+ '/' + str(_dim0out) + '^2'
    except IndexError:
        _dim5out = str(_dim4out)+ '/' + str(_dim0out) + '^2'
    factors[5] = _pressure.convert(_dim5out).value 
    
    # FIXME: need to check mass
    try:
        _dim1 = _input[1]
        _mass_temp = Number(1, dims = _dim1)
        factors[1] = _mass_temp.convert(_output[1]).value
    
    except :
        _mass_temp = Number(1, dims = 'newton*second^2/metre')
        _grav_out = _dim4out + '*second^2/' + _dim0out
        factors[1] = _mass_temp.convert(_grav_out).value
    
    #print(_mass_temp.units(), _mass_temp.value)
    #
    return factors, _grav

#
def get_tolerance(length_unit, tolerance=0.1):
    """
    set tolerance = 10 cm
    """
    # 
    _dim0 = length_unit
    _toldim = Number(tolerance, dims = 'metre')
    _tol = _toldim.convert(_dim0).value
    
    return _tol
#
#
def find_unit_item(unit_items):
    """
    """
    for key, value in kwargs.items(): 
        _unit = find_unit_case(key)
        self.units_in = units_module(_unit, value, 
                                     self.units_in)
#
