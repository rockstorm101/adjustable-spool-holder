# Python imports
import argparse
import math
import solid as sp
import solid.utils as spu

# Project imports
import p2910 as screw

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')
threads = sp.import_scad('../lib/MCAD/fasteners/threads.scad')
chamfers = sp.import_scad('../lib/MCAD/fillets/chamfers.scad')
regular_shapes = sp.import_scad('../lib/MCAD/shapes/2Dshapes.scad')

# Config
T_d = screw.T_d  # thread nominal diameter
T_p = screw.T_p  # thread pitch
T_c = screw.T_c  # thread clearance
F_d = screw.F_d  # flange diam
F_t = 2          # flange thickness
B_d = screw.B_d  # bearing seat diameter
B_h = screw.B_h  # bearing seat depth
N_af = 30        # nut across-flats dimension
N_h = 10         # nut height
PN_s = 3         # part number character height
PN_d = 0.3       # part number engraving depth
dim14 = F_t + B_h + N_h  # full length
_code_name = "2912"
_version = ''

# Connectors
THREAD_CONN = [[0, 0, 0], [0, 0, 1], 0]
BEARING_CONN = [[0, 0, F_t+N_h], [0, 0, 1], 0]

@spu.bom_part(description = "Nut", code_name = _code_name)
def part(variant = '', configuration = '', debug = False):
    nut = regular_shapes.hexagon(None,None,across_flats = N_af)
    tmp = sp.linear_extrude(N_h)(nut)
    flange = sp.cylinder(d=F_d, h=F_t+0.1)
    tmp += sp.translate([0,0,N_h-0.1])(flange)
    tmp += sp.translate([0, 0, N_h+F_t-0.001])(screw.bseat())
    thread = threads.metric_thread(diameter = T_d,
                                   pitch = T_p,
                                   length = dim14+0.2,
                                   internal = True,
                                   clearance = T_c)
    chamfer = chamfers.mcad_chamfer_cylinder(diameter = T_d-2*T_p,
                                             length = T_p+0.25,
                                             angle = None,
                                             depth = None,
                                             internal = True)
    thread = chamfers.mcad_chamfered_cylinder(dim14+0.2, internal = True)(
        thread, chamfer, chamfer)
    tmp -= sp.translate([0,0,-0.1])(thread)
    tmp -= locate_part_number(_code_name+_version+variant)
    # tmp -= sp.rotate([0,0,60])(locate_part_number(version+variant))
    if debug: tmp += assembly.connector(BEARING_CONN)
    if debug: tmp += assembly.connector(THREAD_CONN)
    return tmp

def locate_part_number(text):
    pn = sp.text(text=text,
                 size = PN_s,
                 font="Open Sans:style=Bold",
                 halign = "center")
    pn = sp.linear_extrude(PN_d+0.001)(pn)
    pn = sp.rotate([90,0,0])(pn)
    pn = sp.translate([0,-N_af/2+PN_d-0.001,(N_h-PN_s)/2])(pn)
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
