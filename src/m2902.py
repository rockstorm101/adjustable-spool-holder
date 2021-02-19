# Python imports
import argparse
import math
import solid as sp
import solid.utils as spu

# Project imports
import p2910 as screw

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')
chamfers = sp.import_scad('../lib/MCAD/fillets/chamfers.scad')
threads = sp.import_scad('../lib/MCAD/fasteners/threads.scad')
regular_shapes = sp.import_scad('../lib/MCAD/shapes/2Dshapes.scad')

# Config
T_d = screw.T_d  # thread nominal diameter
T_p = screw.T_p  # thread pitch
T_c = screw.T_c  # thread clearance
T_l = 27         # thread length
F_d = screw.F_d  # flange diam
F_t = 5          # flange thickness
B_d = screw.B_d  # bearing seat diameter
PN_s = 5         # part number character height
PN_d = 0.3       # part number engraving depth
_code_name = "M2902"
_version = ''

def part(variant = '', configuration = '', debug = False):
    flange = sp.cylinder(d=F_d, h=F_t)
    thread = threads.metric_thread(diameter = T_d,
                                   pitch = T_p,
                                   length = T_l,
                                   clearance = T_c,
                                   internal = False)
    chamfer = chamfers.mcad_chamfer_cylinder(T_d, T_p+0.25, None, None)
    thread = chamfers.mcad_chamfered_cylinder(T_l, internal = False)(
        thread, chamfer)
    thread = sp.rotate([180,0,0])(thread)
    tmp = flange + sp.translate([0,0,F_t+T_l-0.001])(thread)
    tmp -= sp.translate([0,PN_s/2,0])(locate_part_number(_code_name))
    tmp -= sp.translate([0,-3*PN_s/2,0])(
        locate_part_number(_version+variant))
    return tmp

def locate_part_number(text):
    pn = sp.text(text=text,
                 size = PN_s,
                 font="Open Sans:style=Bold",
                 halign = "center")
    pn = sp.linear_extrude(PN_d+0.001)(pn)
    pn = sp.rotate([0,180,0])(pn)
    pn = sp.translate([0,0,PN_d])(pn)
    return pn

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help = "include debug code on SCAD render")
    parser.add_argument('-e', '--version', default='',
                        help = "add 'VERSION' to P/N")
    args = parser.parse_args()
    _version = args.version

    for variant in ['']:
        filename = parser.prog.replace(".py","")+_version+variant
        tmp = part(variant=variant, debug=args.debug)
        sp.scad_render_to_file(tmp, filepath=filename+".scad",
                               include_orig_code = False)
