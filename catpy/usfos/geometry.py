# Copyright (c) 2019 CatPy


# Python stdlib imports
from typing import NamedTuple, Dict


# package imports
from catpy.usfos.headers import print_head_line, print_EOF
from catpy.usfos.loading import print_gravity

#
#
class Nodes(NamedTuple):
    """nodes coordiantes"""
    x:float
    y:float
    z:float
    #number:int
#
class Riser(NamedTuple):
    """beam element type riser"""
    number:int
    nodes:Dict
    section:int
    material:int
    type:str
#
class Spring(NamedTuple):
    """beam element type spring"""
    number:int
    nodes:Dict
    section:int
    material:int
    master:int
    type:str
#
class Material(NamedTuple):
    """material"""
    number:int
    name:str
    type: str
    E:float
    poisson:float
    Fy:float
    density:float
    alpha:float
#
class SectionTubular(NamedTuple):
    """Tubualr section"""
    number:int
    name:str
    shape:str
    diameter:float
    thickness:float
    SFH:float
    SFV:float
#
#
def get_nodes_clone(coord, node_number, nodes,
                    water_depth, node_step=50000):
    """
    """
    node_no = node_number
    #nodes = []
    items = len(coord.x)
    for x in range(items):
        number = node_no + x + 1
        nodes[number] = Nodes(x= coord.x[x], 
                              y= coord.y[x], 
                              z= coord.z[x] - water_depth)
        # zero length springs
        x_step = node_step + number
        nodes[x_step] = Nodes(x= coord.x[x], 
                              y= coord.y[x], 
                              z= coord.z[x] - water_depth)
    return number
#
def geometry_ufo(riser, water_depth, node_step:int = 50000):
    """
    """
    #
    #total_items = len(riser.catenary.x)
    #coord = master['coordinates']
    nodes = {}
    if riser.type == 'arch':
        # Lower catenary
        coord = riser.catenary_lower.coordinates
        Lb = riser.catenary_lower.Lb
        s = riser.catenary_lower.s
        items = len(coord.x)
        node_no = 0
        node_number = 0
        #
        # arch_upper.slot
        coord = riser.arch_upper.slot
        node_number = get_nodes_clone(coord, node_number, nodes,
                                      water_depth, node_step)
        # arch_upper.circle
        coord = riser.arch_upper.circle
        node_number = get_nodes_clone(coord, node_number, nodes,
                                      water_depth, node_step) 
        #
        # upper_cat
        coord = riser.catenary_upper.coordinates
        items = len(coord.x)
        node_no = node_number
        for x in range(items):
            node_number = node_no + x + 1
            nodes[node_number] = Nodes(x= coord.x[x], 
                                       y= coord.y[x], 
                                       z= coord.z[x] - water_depth)        
        #
        #print('-->')
    else:
        coord = riser.catenary
        items = len(coord.x)
        for x in range(items):
            nodes[x+1] = Nodes(x=coord.x[x], 
                               y=coord.y[x], 
                               z=coord.z[x])
        node_number = items
    #
    elements = {}
    items = len(riser.catenary[0]) - 1
    items = node_number - 1
    for x in range(items):
        elements[x] = Riser(number=x+1,
                            nodes=[x+1, x+2], 
                            section=1, material=1,
                            type='riser')
        try:
            node_number = x+1 + node_step
            nodes[node_number]
            elements[node_number] = Spring(number=node_number,
                                           nodes=[node_number, x+1], 
                                           section=1, material=2,
                                           master=x+1, type='spring')
        except KeyError:
            continue
    #
    materials = {}
    materials[1] = Material(number=1, name='dummy', type='Plastic',
                            E=1.9950E+11, poisson=3.0000E-01,
                            Fy=4.7574E+08, density=8.1101E+03,
                            alpha=1.2000E-05)
    #
    sections = {}
    sections[1] = SectionTubular(number=1, name='tub', shape='tubular',
                                 diameter=0.3106, thickness=0.10, 
                                 SFH=1.0, SFV=1.0)
    #
    UFOnodes = print_nodes(nodes)
    UFOelements = print_beam(elements)
    UFOmaterials = print_material(materials)
    UFOsections = print_sections(sections)
    #
    file_out = 'cat_ufo.fem'
    print_out = open(file_out, 'w+')
    print_out.write("".join(UFOnodes))
    print_out.write("".join(UFOelements))
    print_out.write("".join(UFOmaterials))
    print_out.write("".join(UFOsections))
    print_out.write("".join(print_gravity()))
    print_out.write("".join(print_EOF(subfix="'")))
    print_out.close()
    print('    * File : {:}'.format(file_out))
    #print('???')
#
def print_nodes(nodes, factor=1):
    """
    """
    header = 'NODAL DATA'
    UFOmod = print_head_line(header, subfix="'")
    UFOmod.append("'\n")
    UFOmod.append("'                                                                  (0:Free, 1:Fixed)\n")
    UFOmod.append("'            Node ID              X              Y              Z   Boundary code\n")
    UFOmod.append("'\n")
    
    for number, _node in nodes.items():
        UFOmod.append(" NODE {:14.0f}".format(number))
        UFOmod.append(" {: 14.5f} {: 14.5f} {: 14.5f}".format(*_node))
        #
        #if _node.boundary:
        #    UFOmod.append("  ")
        #    for _bound in _node.boundary.releases:
        #        _ir = 0
        #        if _bound != 0:
        #            _ir = 1
        #        UFOmod.append((" {:1.0f}").format(_ir))
        UFOmod.append("\n")    
    #
    return UFOmod
#
#
def print_beam(elements):
    """
    print beam elements
    """
    UFOmod = []
    _iter = 0
    # Beam Elements
    for number, _elem in elements.items():
        if _elem.type != 'riser':
            continue
        if _iter == 0:
            UFOmod.append("'\n")
            UFOmod.append("'{:} Riser element\n".format(70 * "-"))
            UFOmod.append("'\n")
            UFOmod.append("'            Elem ID      np1      np2   material   geom    lcoor    ecc1    ecc2\n")
            UFOmod.append("'\n")
            UFOmod.append(" BeamType Riser Mat 1\n")
            UFOmod.append("'\n")
        UFOmod.append((" BEAM {:14.0f}").format(_elem.number))
        for _node in _elem.nodes:
            UFOmod.append(" {:8.0f}".format(_node))

        UFOmod.append(" {:8.0f}".format(_elem.material))
        UFOmod.append(" {:8.0f}".format(_elem.section))
        #
        _iter += 1
        UFOmod.append("\n")
    # spring
    _iter = 0
    for number, _elem in elements.items():
        if _elem.type != 'spring':
            continue
        if _iter == 0:
            UFOmod.append("'\n")
            UFOmod.append("'  2 node spring element\n")
            UFOmod.append("'\n")
            UFOmod.append("'            Elem ID      np1      np2   material   geom    lcoor    ecc1    ecc2\n")
            UFOmod.append("'\n")
        #
        UFOmod.append((" BEAM {:14.0f}").format(_elem.number))
        for _node in _elem.nodes:
            UFOmod.append(" {:8.0f}".format(_node))
        UFOmod.append(" {:8.0f}".format(_elem.material))
        UFOmod.append(" {:8.0f}".format(_elem.section))
        UFOmod.append("\n")
        UFOmod.append(" ElmTrans   MainBeam {:8.0f}    ZeroSpri  {:16.0f}\n"
                      .format(_elem.master, _elem.number))
        #
        _iter += 1
        #print('-->')
    #
    return UFOmod
#
#
def print_material(materials):
    """
    print material properties
    """
    UFOmod = []
    _iter = 0
    _stress = 1
    _density = 1
    #
    UFOmod.append("' \n")
    UFOmod.append("'         Mat_ID    Type  E-modulus    Poisson  Yield(Fy)    Density  Thermal-X\n")
    UFOmod.append("' \n")        
    
    for key, _mat in materials.items():
        UFOmod.append(" MATERIAL {:6.0f} {:7s} {:1.4E} {:1.4E} {:1.4E} {:1.4E} {:1.4E}  ' {:}\n"
                      .format(_mat.number, _mat.type, _mat.E * _stress,
                              _mat.poisson, _mat.Fy * _stress,
                              _mat.density * _density, _mat.alpha,
                              _mat.name))
    #
    _mat_number = _mat.number + 1
    UFOmod.append("' \n")
    UFOmod.append("'          MatID   Type  SprType   Coeff      Stf    FricDofs  ForceDof\n")    
    UFOmod.append(" MATERIAL {:6.0f}   {:6s} {:6s} {:1.3E} {:1.3E} {:8.0f} {:8.0f}  ' {:}\n"
                  .format(_mat_number, 'Fric', 'Compr', 0.50, 1e6, 12, 3, 'Riser touchdown'))
    #
    return UFOmod    
#
#
def print_sections(sections, factor=1):
    """
    print section properties
    """

    header = 'CROSS SECTION DATA'
    UFOmod = print_head_line(header, subfix="'")
    #
    # Tubular cross section
    #_items = get_section_shape(sections, shape=r"\btub(ular)?|pipe\b")
    #if _items:
    UFOmod.append("'{:} Tubular cross section\n".format(61 * "-"))
    UFOmod.append("'\n")
    UFOmod.append("'{:}Geom ID {:}Do {:}Thick    (Shear_y    Shear_z      Diam2 )\n"
                  .format(12*" ", 8*" ", 4*" "))
    UFOmod.append("'\n")
        
    for key, _section in sections.items():
        if _section.shape != 'tubular':
            continue
        UFOmod.append((" PIPE {:14.0f}").format(_section.number))
        UFOmod.append((" {:10.6f}").format(_section.diameter * factor))
        UFOmod.append((" {:10.6f}").format(_section.thickness * factor))
        UFOmod.append((" {:10.3f}").format(_section.SFH))
        UFOmod.append((" {:10.3f}").format(_section.SFV))
        # cone
        UFOmod.append((" {:}").format(14*" "))
        UFOmod.append(("  ' {:}").format(_section.name))
        UFOmod.append("\n")
    #
    return UFOmod
    



