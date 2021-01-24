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
dim11 = bearing.OD + 0.2  # bearing seat ID
dim12 = 11.8  # bearing seat depth
dim13 = 15    # full height
dim14 = 38.5  # flange ID

# Connectors
DEFAULT_CONN = [[0, 0, 0], [0, 0, -1], 0]
BEARING_CONN = [[0, 0, dim12], [0, 0, -1], 0]

@spu.bom_part(description = "Clamp")
def part(variant = 'A', configuration = 'default', debug = False):
    tmp = sp.cylinder(h=dim13, d1=dim10, d2=dim14)
    tmp -= sp.translate([0,0,-0.1])(sp.cylinder(d=dim11, h=dim12+0.1))
    tmp -= sp.translate([0,0,-0.1])(sp.cylinder(d=dim14, h=dim13+0.2))
    if debug: tmp += assembly.connector(DEFAULT_CONN)
    return tmp

if __name__ == '__main__':
    sp.scad_render_to_file(part(), include_orig_code = False)
    # One line per variant to generate all .scad files
    # sp.scad_render_to_file(part(variant = B), include_orig_code = False)
