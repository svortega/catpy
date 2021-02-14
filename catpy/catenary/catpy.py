# !usr/bin/env python
# Copyright (c) 2021 CatPy

# Python stdlib imports
import math
from typing import NamedTuple, Tuple, List

# package imports
import numpy as np 
from scipy.optimize import fsolve  
#import xlwings as xw
#from openpyxl import load_workbook
#from catpy.xl.master_sheet import read_master


#
class Coordinates(NamedTuple):
    """
    """
    x:List
    y:List
    z:List
#
class ArchResults(NamedTuple):
    """
    """
    arch_upper:Tuple
    catenary_upper:Tuple
    arch_lower:Tuple
    catenary_lower:Tuple
    catenary:List
    type:str="arch"
#
def line_eq(coord_1, coord_2, c=0):
    """
    """
    delta_x = (coord_2[0] - coord_1[0])
    delta_y = (coord_2[1] - coord_1[1])
    m = delta_y / delta_x
    delta = abs(delta_x) 
    x = delta_x + coord_2[0]
    y = m*delta_x + coord_2[1] + c
    #plot_chart([coord_1[0], coord_2[0], x], 
    #           [coord_1[1], coord_2[1], y])
    return x, y
    
#
def check_cable_length(S, L, d):
    """
    checking if cable length is bigger than total distance between supports
    """
    distance = (L**2 + d**2)**0.5
    if S <= distance:
        raise IOError("Length of cable must be greater than TOTAL distance between supports!")
        #S=float(input("Length of cable [m]: "))      
#
#
class MidArchResults(NamedTuple):
    """
    """
    buoy:Tuple
    catenary_upper:Tuple
    catenary_lower:Tuple
    catenary:List
    type:str="midwater_arch"
#
#
def pyCatenary(L, d, za, MSL, S, w, workbook_name):
    """
    L : Horizontal Distance between supports [m]
    d : Vertical Distance between supports [m]
    za : Elevation of higher support from reference plane [m]
    MSL: mean water level [m]
    
    S : Length of cable [m] - must be greater than distance between supports
    w : Unit weight of cable [kg/m]
    """
    #
    #L=master['L']
    #d=master['d']
    #S=master['S']
    #w=master['w']
    #za=master['za']
    #
    check_cable_length(S, L, d)  
    #
    #
    def cat(a):
        """
        defining catenary function
        """
        return (a*math.sinh(L/(2*a)) + math.atanh(d/S)
                + a*math.sinh(L/(2*a)) - math.atanh(d/S) - S)
    #    
    #
    # solving catenary function for 'a'
    a = fsolve(cat, 1)
    # hor. distance between lowest catenary point (P) to higher support point (La)
    La = a * (L/(2*a) + math.atanh(d/S))
    # hor. distance between lowest catenary point (P) to lower support point (Lb)
    Lb = L - La
    # vert. distance from higher support point to lowest point (P) in catenary (ha)
    ha = a*math.cosh(La/a)-a
    #
    # calculating reaction forces and angles
    #
    # catenary lenght between support "A" (higher) and "P" - Sa
    Sa = a*math.sinh(La/a)
    # catenary lenght between support "B" )lower) and "P" - Sb
    Sb = a*math.sinh(Lb/a)
    # horizontal tension - constant through catenary: H
    H = w*a
    # vertical tension at "A"  (Va) and "B" (Vb)
    Va = Sa*w
    Vb = Sb*w
    # tension at "A" (TA) and B (TB)
    TA = (H**2+Va**2)**0.5
    TB = (H**2+Vb**2)**0.5
    print('--')
    print('Tension A = {:1.2f} kN'.format(TA[0]*9.81/1000))
    print('Tension B = {:1.2f} kN'.format(TB[0]*9.81/1000))
    # inclination angles from vertical at "A" (ThetA) and B (ThetB)
    ThetA = math.atan(H/Va)
    ThetB = math.atan(H/Vb)
    ThetAd = ThetA*180/math.pi
    ThetBd = ThetB*180/math.pi
    # establishing A, B and P in coordinate system
    # index "a" corresponding to point "A", "b" to "B"-point and "P" to lowest caten. point
    zb = za-d
    zp = za-ha
    xa = La
    xp = 0
    xb = -Lb
    #
    results = {'catenary_coefficient': a[0],
               'constant_horizontal_tension': H[0],
               'vertical_tension_end_A': Va[0],
               'total_tension_end_A': TA[0],
               'vertical_tension_end_B': Vb[0],
               'total_tension_end_B': TB[0],
               'inclination_angle_from_vertical_end_A': ThetA,
               'inclination_angle_from_vertical_end_B': ThetB,
               'xb': xb, 'xa':xa}
    #
    print_result(results, workbook_name)
    #xc, y, z = get_coordinates(a, L, xb, xa, MSL, workbook_name)
    #plot_chart(xc, z)
    return results
#
def plot_chart(xc, y):
    """
    """
    import matplotlib.pyplot as plt
    # plotting, finally 
    plt.plot(xc, y, 'o')
    plt.xlabel("X-distance [m]")
    plt.ylabel("Z-distance [m]")
    plt.grid()
    plt.show()
#
#
#
class CatenaryResults(NamedTuple):
    """
    V : Vertical force
    H : Horizontal force
    s : cable element lenght
    x : horizontal coordinate
    z : vertical coordinate
    Te : cable element Tension 
    Lb : Unstretched length
    riser_type : touchdown/suspended
    """
    V:float
    H:float
    s:dict
    coordinates:dict
    Te:dict
    Lb:float
    riser_type:str
#
def ln(x):
    return np.log(x + np.sqrt(1 + x**2))
#
def irvine_method(L, d, S, w, EA, global_coord,
                  steps:int =100):
    """
    L : Horizontal Distance between supports [m]
    d : Vertical Distance between supports [m]
    
    S : Length of cable [m] - must be greater than distance between supports
    w : Unit weight of cable [kg/m]
    Axial stiffness EA : [N]
    global_coord : 
    """
    #
    check_cable_length(S, L, d)
    #
    def equation(f):
        """
        """
        V = f[0]
        H = f[1]
        F0 = (H/w * (ln(V/H) - ln((V - w*S) / H))
              + H*S / EA - L)
        F1 = (H/w * (np.sqrt(1 + (V/H)**2) 
                     - np.sqrt(1 + ((V - w*S)/H)**2))
              + (V*S - w*S**2/2.0) / EA  - d)
        return (F0, F1)
    # 
    def eqx(s, H, Va):
        """
        """
        return (H/w * (ln((Va + w*s) / H) 
                       - ln(Va/H))
                + H*s / EA)
    #
    def eqz(s, H, Va):
        """
        """
        return (H/w * (np.sqrt(1 + ((Va + w*s)/H)**2) 
                       - np.sqrt(1 + (Va/H)**2))
                + (Va*s + w*s**2/2.0) / EA)
    #
    #
    fGuess = np.array([1,1])
    V, H = fsolve(equation, fGuess)
    #
    Va = V -  w * S
    print('Vertical tension A = {:1.2f} kN'.format(Va*9.81/1000))
    print('Vertical tension B = {:1.2f} kN'.format(V*9.81/1000))
    print('Constant Horizontal Tension = {:1.2f} kN'.format(H*9.81/1000))
    #
    sinc = S / steps
    s = []
    x = []
    z = []
    Te = []
    for i in range(steps+1):
        s.append(sinc * i)
        x.append(eqx(s[i], H, Va))
        z.append(eqz(s[i], H, Va))
        Te.append((H**2 + (Va + w*s[i])**2)**0.50)
    #
    print('Tension Side A = {:1.2f} kN'.format(Te[0]*9.81/1000))
    print('Tension Side B = {:1.2f} kN'.format(Te[-1]*9.81/1000))
    #plot_chart(x, z)
    #
    x = [ _x + global_coord.x for _x in x]
    y = [ global_coord.y for _x in x]
    z = [ _z + global_coord.z for _z in z]
    coord = Coordinates(x, y, z)    
    #
    Lb = 0
    return CatenaryResults(V, H, s, coord, Te, Lb, riser_type="suspended")

#
def riser_touchdown(L, d, S, w, EA, Cb, global_coord,
                    riser_diametre):
    """
    L : Horizontal Distance between supports [m]
    d : Vertical Distance between supports [m]
    
    S : Length of cable [m] - must be greater than distance between supports
    w : Unit weight of cable [kg/m]
    EA : [N]
    Cb : Soil Friction
    """
    #
    check_cable_length(S, L, d)
    #
    riser_guess = irvine_method(L, d, S, w, EA, global_coord)
    Vi = riser_guess.V
    Hi = riser_guess.H
    #
    #
    def eqx(s, H, Va):
        """
        """
        if s <= alpha:
            return s
        elif s >= Lb:
            return (Lb + H/w * np.arcsinh(w*(s-Lb)/H)
                    + H*s/EA + Cb*w/(2*EA)*(alpha*gamma - Lb**2))
        else:
            return s + Cb*w/(2*EA)*(s**2 - 2*s*gamma + alpha*gamma)
    #
    def eqz(s, H, Va):
        """
        """
        if s <= Lb :
            return 0
        
        return (H/w * ((1 + (w*(s-Lb)/H)**2)**0.5 - 1)
                + w*(s-Lb)**2/(2*EA))
    #
    def equation_touchdown(f):
        """
        """
        V = f[0]
        H = f[1]
        Lbf = (S - V/w)
        #  
        F0 = (Lbf + H/w * np.arcsinh(V/H) + H*S/EA
                + Cb*w/(2*EA) * ((Lbf - H/(Cb*w)) 
                                  * max(Lbf - H/(Cb*w), 0)
                                  - Lbf**2)
                - L)       
        #
        F1 = H/w * (np.sqrt(1 + (V/H)**2) - 1) +  V**2/(2.0*EA*w) - d
        #
        return (F0, F1)
    #
    fGuess = np.array([Vi,Hi])
    V, H = fsolve(equation_touchdown, fGuess)
    Lb = S - V/w
    gamma = Lb - H/(Cb*w)
    alpha = max(gamma, 0)
    #
    #Va = V -  w * S
    print('Unstretched length Lb = {:1.2f} m'.format(Lb))
    #print('Vertical tension A = {:1.2f} kN'.format(Va*9.81/1000))
    print('Vertical tension B = {:1.2f} kN'.format(V*9.81/1000))
    print('Constant Horizontal Tension = {:1.2f} kN'.format(H*9.81/1000))
    #
    #sinc = S / steps
    s = []
    x = []
    z = []
    Te = []
    #for i in range(steps+1):
    #    s.append(sinc * i)
    #    x.append(eqx(s[i], H, V))
    #    z.append(eqz(s[i], H, V))
    #    if s[i] <= Lb:
    #        Te.append(max(H + Cb*w*(s[i]-Lb), H))
    #    else:
    #        Te.append((H**2 + (w*(s[i] - Lb))**2)**0.50)
    #
    _steps = math.ceil(0.50 * Lb / riser_diametre)
    sinc = Lb / _steps
    for i in range(_steps+1):
        s.append(sinc * i)
        x.append(eqx(s[-1], H, V))
        z.append(eqz(s[-1], H, V))
        Te.append(max(H + Cb*w*(s[-1]-Lb), H))    
    #
    Sc = S - Lb
    _steps = math.ceil(0.50 * Sc / riser_diametre)
    sinc = Sc / _steps
    for i in range(1, _steps+1):
        s.append(Lb + sinc * i)
        x.append(eqx(s[-1], H, V))
        z.append(eqz(s[-1], H, V))
        if s[-1] <= Lb:
            Te.append(max(H + Cb*w*(s[-1]-Lb), H))
        else:
            Te.append((H**2 + (w*(s[-1] - Lb))**2)**0.50)    
    #
    #
    print('Tension Side A = {:1.2f} kN'.format(Te[0]*9.81/1000))
    print('Tension Side B = {:1.2f} kN'.format(Te[-1]*9.81/1000))
    #
    x = [ _x + global_coord.x for _x in x]
    y = [ global_coord.y for _x in x]
    z = [ _z + global_coord.z for _z in z]
    coord = Coordinates(x, y, z)
    #plot_chart(x, z)
    #print('end')
    return CatenaryResults(V, H, s, coord, Te, 
                           Lb, riser_type="touchdown")
#
#
class ArchOutput(NamedTuple):
    """
    circle: 
    """
    circle:list
    slot:list
    arc_length:float
#
#
def straight_line(x, m=1, c=0):
    """
    straight line equation
    """
    return x*m + c
#
def circunference_line(x, r, xp1=0, yp1=0):
    """
    Calculating the coordinates of a point on a circles
    circumference from the radius, an origin and the 
    arc between the points
    """
    xp2 = xp1 + r * math.sin(x)
    yp2 = yp1 - r * (1- math.cos(x) )   
    #try:
    #    xp2 = xp1 + r * math.cos(math.tau/x)
    #    yp2 = yp1 + r * math.sin(math.tau/x)
    #except ZeroDivisionError:
    #    xp2 = x 
    #    yp2 = yp1       
    return xp2, yp2
#
def arch_geometry(radius, clamp_slot, 
                  d_arch, riser_diametre,
                  theta, global_coord,
                  reverse=False):
    """
    """
    # Clamp Slot
    _steps = math.floor(clamp_slot/(2*riser_diametre))
    sinc = clamp_slot / (2*_steps)
    x_slot = []
    z_slot = []
    for i in range(_steps):
        x_slot.append(sinc * i)
        z_slot.append(d_arch)
    #plot_chart(x_slot, z_slot)
    #
    # Arch
    arc_length = radius * math.tau * theta / 360
    _steps = math.floor(arc_length/riser_diametre)
    sinc = arc_length / _steps
    r_theta = 360 * sinc / (radius * math.tau)
    #print(r_theta)    
    x_circle = []
    z_circle = []
    for i in range(_steps):
        rad = math.radians(i*r_theta)
        _x, _z = circunference_line(x=rad, r=radius,
                                    xp1= clamp_slot/2.0,
                                    yp1=d_arch)
        x_circle.append(_x)
        z_circle.append(_z)
    #plot_chart(x_circle, z_circle)
    #
    #x_t = x_slot + x_circle
    #z_t = z_slot + z_circle
    #plot_chart(x_t, z_t)
    #
    #x_slot = x_slot[:-2]
    #z_slot = z_slot[:-2]
    #y_slot = [ 0 for _x in x_slot]
    x_slot = [ _x + global_coord.x for _x in x_slot]
    y_slot = [ global_coord.y for _x in x_slot]
    z_slot = [ _z + global_coord.z for _z in z_slot]
    #
    #
    x_circle = [ _x + global_coord.x for _x in x_circle]
    y_circle = [ global_coord.y for _x in x_circle]
    z_circle = [ _z + global_coord.z for _z in z_circle]
    if reverse:
        x_circle = [-1*_x for _x in x_circle]
        x_circle = list(reversed(x_circle))
        z_circle = list(reversed(z_circle))
        #
        x_slot = [-1*_x for _x in x_slot]
        y_slot = list(reversed(y_slot))
        z_slot = list(reversed(z_slot))
    #
    slot_circle = Coordinates(x_circle, y_circle, z_circle)    
    slot_coord = Coordinates(x_slot, y_slot, z_slot)
    #return [x_circle, z_circle], [x_slot, z_slot], arc_length
    return ArchOutput(circle = slot_circle,
                      slot = slot_coord,
                      arc_length = arc_length)