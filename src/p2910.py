# Python imports
import argparse
import math
import solid as sp
import solid.utils as spu

import v2901 as bearing

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')
threads = sp.import_scad('../lib/MCAD/fasteners/threads.scad')
chamfers = sp.import_scad('../lib/MCAD/fillets/chamfers.scad')

# Config
dim10 = 14              # first step height
B_h = bearing.B + 1.4   # bearing seat height
F_d = 29.5              # flange OD, which the bearing seats against
B_d = bearing.ID - 0.2  # bearing seat diam
dim14 = 110             # full length
T_d = 20                # thread nom diam
T_p = 2.5               # thread pitch
T_c = 0.7               # thread clearance
dim17 = dim14 - dim10 - B_h  # thread length
_version = ''


# Connectors
BEARING_CONN = [[0, 0, dim10], [0, 0, 1], 0]
NUT_CONN =     [[0, 0, dim14-20.2], [0, 0, -1], 0]

@spu.bom_part(description = "Screw", code_name = "2910")
def part(variant = '', configuration = '', debug = False):
    tmp = sp.cylinder(d=F_d, h=dim10)
    tmp += sp.translate([0,0,dim10-0.1])(sp.cylinder(d=B_d, h=B_h+0.1))
    thread = chamfers.mcad_chamfered_cylinder(dim17, internal = False)(
        threads.metric_thread(diameter = T_d,
                              pitch = T_p,
                              length = dim17,
                              internal = False,
                              clearance = T_c ),
        chamfers.mcad_chamfer_cylinder(T_d, T_p+0.25, depth=None,
                                       internal = False)
    )
    tmp += sp.translate([0,0,dim17+B_h+dim10])( sp.rotate([180,0,0])(thread) )
    tmp += sp.rotate([180,0,0])(
        sp.translate([-107,-113,-0.2])(
            sp.import_(
                "../aux/Ender_3_spool_holder/files/" +
                "Ender3_Spool_Holder_Coupling.stl") ) )
    if debug: tmp += assembly.connector(BEARING_CONN)
    return tmp

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
