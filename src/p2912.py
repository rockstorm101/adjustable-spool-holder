# Python imports
import math
import solid as sp
import solid.utils as spu

# Project imports
import p2910 as screw

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')
threads = sp.import_scad('../lib/MCAD/fasteners/threads.scad')
metric_fasteners = sp.import_scad('../lib/MCAD/fasteners/metric_fastners.scad')

# Config
T_d = screw.T_d  # thread nominal diameter
T_p = screw.T_p  # thread pitch
T_c = screw.T_c  # thread clearance
F_d = screw.F_d  # flange diam
F_t = 2          # flange thickness
B_d = screw.B_d  # bearing seat diameter
B_h = screw.B_h  # bearing seat depth
dim14 = F_t + B_h  # full length

# Connectors
THREAD_CONN = [[0, 0, 0], [0, 0, 1], 0]
BEARING_CONN = [[0, 0, F_t], [0, 0, 1], 0]

@spu.bom_part(description = "Nut")
def part(variant = 'A', configuration = 'default', debug = False):
    tmp = sp.cylinder(d=F_d, h=F_t)
    tmp += sp.translate([0,0,F_t-0.1])(sp.cylinder(d=B_d, h=B_h+0.1))
    thread = threads.metric_thread(diameter = T_d,
                                   pitch = T_p,
                                   length = dim14+0.2,
                                   internal = True,
                                   clearance = T_c)
    chamfer = threads.chamfer_cylinder(T_d-2*T_p, T_d+0.5, internal = True)
    thread = threads.chamfered_thread(dim14+0.2, internal = True)(
        thread, chamfer, chamfer)
    tmp -= sp.translate([0,0,-0.1])(thread)
    # tmp -= chamfer_cylinder_internal(T_d+0.25)
    # tmp -= sp.translate([0,0,dim14])(
    #     sp.rotate([180,0,0])(
    #         chamfer_cylinder_internal(T_d+0.25) ) )
    if debug: tmp += assembly.connector(BEARING_CONN)
    return tmp

def chamfer_cylinder_internal(diameter = 10, angle = 45):
    d = diameter/2
    h = d / math.tan(math.radians(angle))
    h_p = h + 0.1
    d_p = h_p / h * d
    tmp = sp.translate([0,0,-0.1])(sp.cylinder(h = h_p, d1 = 2*d_p, d2 = 0))
    return tmp

if __name__ == '__main__':
    sp.scad_render_to_file(part(), include_orig_code = False)
    # One line per variant to generate all .scad files
    # sp.scad_render_to_file(part(variant = B), include_orig_code = False)
