# Python imports
import math
import solid as sp
import solid.utils as spu

import v2901 as bearing

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')
threads = sp.import_scad('../lib/MCAD/fasteners/threads.scad')

# Config
dim10 = 80    # OD
dim11 = bearing.OD + 0.4  # bearing seat ID
dim13 = 16    # full height
dim14 = 38.5  # flange ID
dim15 = 2     # flange height
dim16 = dim13 - dim15   # bearing seat depth

# Connectors
DEFAULT_CONN = [[0, 0, 0], [0, 0, -1], 0]
BEARING_CONN = [[0, 0, dim16], [0, 0, -1], 0]

@spu.bom_part(description = "Clamp")
def part(variant = 'A', configuration = 'default', debug = False):
    out_cyl = sp.cylinder(h=dim15+0.001, d=dim10)
    cone = sp.cylinder(h=dim16, d1=dim10, d2=dim11)
    cone = sp.translate([0,0,dim15])(cone)
    tmp = out_cyl + cone
    bseat = sp.translate([0,0,-0.1])( sp.cylinder(d=dim11, h=dim16+0.1) )
    tmp -= bseat
    flange = sp.cylinder(d=dim14, h=dim15+0.2)
    flange = sp.translate([0,0,dim16-0.1])(flange)
    tmp -= flange
    chamfer = threads.chamfer_cylinder(cyl_diameter = dim11,
                                       chfr_diameter = dim11 + 2*1.5,
                                       angle = 30,
                                       internal = True)
    tmp -= chamfer
    if debug: tmp += assembly.connector(DEFAULT_CONN)
    if debug: tmp += assembly.connector(BEARING_CONN)
    return tmp

if __name__ == '__main__':
    sp.scad_render_to_file(part(), include_orig_code = False)
    # One line per variant to generate all .scad files
    # sp.scad_render_to_file(part(variant = B), include_orig_code = False)
