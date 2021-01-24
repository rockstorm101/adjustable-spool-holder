# Python imports
import solid as sp
import solid.utils as spu

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')

# Config
ID = 25
OD = 42
B =   9

# Connectors
RACEI_CONN = [[0, 0, 0], [0, 0,  1], 0]
RACEO_CONN = [[0, 0, B], [0, 0, -1], 0]

@spu.bom_part(description = "Bearing 6905-ZZ")
def part(variant = 'A', configuration = 'default', debug = False):
    tmp = sp.cylinder(d=OD, h=B)
    tmp -= sp.translate([0,0,-0.1])(sp.cylinder(d=ID, h=B+0.2))
    if debug: tmp += assembly.connector(DEFAULT_CONN)
    return tmp

if __name__ == '__main__':
    sp.scad_render_to_file(part(), include_orig_code = False)
    # One line per variant to generate all .scad files
    # sp.scad_render_to_file(part(variant = B), include_orig_code = False)
