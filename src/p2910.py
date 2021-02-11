# Python imports
import math
import solid as sp
import solid.utils as spu

import v2901 as bearing

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')
threads = sp.import_scad('../lib/MCAD/fasteners/threads.scad')

# Config
dim10 = 14              # first step height
B_h = bearing.B + 1.4   # bearing seat height
F_d = 29.5              # flange OD, which the bearing seats against
B_d = bearing.ID - 0.2  # bearing seat diam
dim14 = 90              # full length
T_d = 20                # thread nom diam
T_p = 2.5               # thread pitch
T_c = 0.4               # thread clearance
dim17 = dim14 - dim10 - B_h  # thread length


# Connectors
BEARING_CONN = [[0, 0, dim10], [0, 0, 1], 0]
NUT_CONN =     [[0, 0, dim14-20.2], [0, 0, -1], 0]

@spu.bom_part(description = "Screw")
def part(variant = 'A', configuration = 'default', debug = False):
    tmp = sp.cylinder(d=F_d, h=dim10)
    tmp += sp.translate([0,0,dim10-0.1])(sp.cylinder(d=B_d, h=B_h+0.1))
    #tmp += sp.translate([0,0,+0.1])(sp.cylinder(d=T_p, h=dim14-0.1))
    thread = threads.chamfered_thread(dim17, internal = False)(
        threads.metric_thread(diameter = T_d,
                              pitch = T_p,
                              length = dim17,
                              internal = False,
                              clearance = 1 ),
        threads.chamfer_cylinder(T_d, T_d - 2*T_p - 0.5, internal = False)
    )
    tmp += sp.translate([0,0,dim17+B_h+dim10])( sp.rotate([180,0,0])(thread) )
    # tmp -= sp.translate([0,0,dim14])(
    #     sp.rotate([180,0,0])(
    #         chamfer_cylinder_external(2, 45, diameter = 20) ))
    tmp += sp.rotate([180,0,0])(
        sp.translate([-107,-113,-0.2])(
            sp.import_(
                "../aux/Ender_3_spool_holder/files/" +
                "Ender3_Spool_Holder_Coupling.stl") ) )
    if debug: tmp += assembly.connector(BEARING_CONN)
    return tmp

def chamfer_cylinder_external(length = 1, angle = 45, diameter = 10):
    # create a solid chamfer that then has to be substracted
    #   length = chamfer length
    #   angle  = chamfer angle
    #   diameter = diameter of the cylinder onto which this chamfer
    #              will be applied
    e = length
    tg_a = math.tan(math.radians(angle))
    d = diameter
    h = e / tg_a
    e_p = e + 0.1*(1 + tg_a)
    h_p = h + 0.1*(1 + 1/tg_a)
    p1 = [d/2 + 0.1 - e_p,      -0.1, 0]
    p2 = [d/2 + 0.1,            -0.1, 0]
    p3 = [d/2 + 0.1,       h_p - 0.1, 0]
    tmp = sp.rotate_extrude()( sp.polygon([p1, p2, p3]) )
    return tmp

if __name__ == '__main__':
    sp.scad_render_to_file(part(), include_orig_code = False)
    # One line per variant to generate all .scad files
    # sp.scad_render_to_file(part(variant = B), include_orig_code = False)
