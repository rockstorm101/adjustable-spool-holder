# m2901.py -- Male Thread Prototype

# Python imports
#import math
import solid as sp
import solid.utils as spu

import p2910 as screw 

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')
threads = sp.import_scad('../lib/MCAD/fasteners/threads.scad')

# Config
T_d = screw.T_d      # thread nom diam
T_p = screw.T_p     # thread pitch
T_c = screw.T_c     # thread clearance
T_l = 16  # thread length
F_d = T_d + 5  # flange OD
F_h = 2  # flange height


# Connectors
# BEARING_CONN = [[0, 0, dim10], [0, 0, 1], 0]
# NUT_CONN =     [[0, 0, dim14-dim17/2+0.9], [0, 0, -1], 0]

def part(variant = 'A', configuration = 'default', debug = False):
    tmp = sp.cylinder(d=F_d, h=F_h)
    thread = threads.chamfered_thread(T_l, internal = False)(
        threads.metric_thread(diameter = T_d,
                              pitch = T_p,
                              length = T_l,
                              internal = False,
                              clearance = T_c ),
        threads.chamfer_cylinder(T_d, T_d - 2*T_p - 0.5, internal = False)
    )
    tmp += sp.translate([0,0,T_l+F_h-0.001])( sp.rotate([180,0,0])(thread) )
    return tmp

if __name__ == '__main__':
    sp.scad_render_to_file(part(), include_orig_code = False)
    # One line per variant to generate all .scad files
    # sp.scad_render_to_file(part(variant = B), include_orig_code = False)
