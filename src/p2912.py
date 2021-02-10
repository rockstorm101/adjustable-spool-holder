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
PN_s = 5         # part number character height
PN_d = 0.3       # part number engraving depth
dim14 = F_t + B_h + N_h  # full length

# Connectors
THREAD_CONN = [[0, 0, 0], [0, 0, 1], 0]
BEARING_CONN = [[0, 0, F_t+N_h], [0, 0, 1], 0]

@spu.bom_part(description = "Nut")
def part(ver = "01", variant = 'A', configuration = 'default', debug = False):
    nut = regular_shapes.hexagon(0,0,across_flats = N_af)
    tmp = sp.linear_extrude(N_h)(nut)
    flange = sp.cylinder(d=F_d, h=F_t+0.1)
    tmp += sp.translate([0,0,N_h-0.1])(flange)
    bseat = sp.cylinder(d=B_d, h=B_h+0.1)
    tmp += sp.translate([0, 0, N_h+F_t-0.1])(bseat)
    thread = threads.metric_thread(diameter = T_d,
                                   pitch = T_p,
                                   length = dim14+0.2,
                                   internal = True,
                                   clearance = T_c)
    chamfer = threads.chamfer_cylinder(T_d-2*T_p, T_d+0.5, internal = True)
    thread = threads.chamfered_thread(dim14+0.2, internal = True)(
        thread, chamfer, chamfer)
    tmp -= sp.translate([0,0,-0.1])(thread)
    pn1 = sp.text(text="2912", size = 5, halign = "center")
    pn2 = sp.text(text = ver + variant, size = 5, halign = "center")
    tmp -= locate_part_number(pn1)
    tmp -= sp.rotate([0,0,60])(locate_part_number(pn2))
    # tmp -= chamfer_cylinder_internal(T_d+0.25)
    # tmp -= sp.translate([0,0,dim14])(
    #     sp.rotate([180,0,0])(
    #         chamfer_cylinder_internal(T_d+0.25) ) )
    if debug: tmp += assembly.connector(BEARING_CONN)
    if debug: tmp += assembly.connector(THREAD_CONN)
    return tmp

def locate_part_number(part_number):
    pn = part_number
    pn = sp.linear_extrude(PN_d+0.001)(pn)
    pn = sp.rotate([90,0,0])(pn)
    pn = sp.translate([0,-N_af/2+PN_d-0.001,(N_h-PN_s)/2])(pn)
    return pn

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
