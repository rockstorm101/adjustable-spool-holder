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
T_d = screw.T_d
T_p = screw.T_p
F_d = screw.F_d  # flange diam
F_t = 2          # flange thickness
B_d = screw.B_d  # OD
B_h = screw.B_h  # bearing seat depth
dim14 = F_t + B_h  # full length

# Connectors
THREAD_CONN = [[0, 0, 0], [0, 0, 1], 0]
BEARING_CONN = [[0, 0, F_t], [0, 0, 1], 0]

@spu.bom_part(description = "Nut")
def part(variant = 'A', configuration = 'default', debug = False):
    tmp = sp.cylinder(d=F_d, h=F_t)
    tmp += sp.translate([0,0,F_t-0.1])(sp.cylinder(d=B_d, h=B_h+0.1))
    tmp -= sp.translate([0,0,-0.1])(
        threads.metric_thread(diameter = T_d+0.5,
                              pitch = T_p,
                              length = dim14+0.2,
                              internal = True,
                              leadin = 2,
                              leadfac = 1.5) )
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
