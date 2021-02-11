# Python imports
import solid as sp
import solid.utils as spu

# Import parts to be assembled
import p2910 as screw
import p2911 as clamp
import p2912 as nut
import v2901 as bearing

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')

def part(variant = 'A', configuration = 'default', debug = False):
    C = sp.color("SeaGreen", 1)( clamp.part(debug=debug) )
    B = bearing.part(debug=debug)
    N = sp.color("Plum", 1)( nut.part(debug=debug) )
    S = sp.color("Khaki", 1)(screw.part(debug=debug))

    BC = B + assembly.attach(bearing.RACEO_CONN, clamp.BEARING_CONN)(C)
    NBC = N + assembly.attach(nut.BEARING_CONN, bearing.RACEI_CONN)(BC)

    tmp = S + assembly.attach(screw.BEARING_CONN, bearing.RACEI_CONN)(BC)
    tmp    += assembly.attach(screw.NUT_CONN, nut.THREAD_CONN)(NBC)

    tmp = sp.rotate([0,90,0])(tmp)
    if debug:
        tmp -= sp.translate([50-0.1,-50,0])(
            sp.color("White",0.1)( sp.cube([100,100,100], center = True) )
        )
    return tmp

if __name__ == '__main__':
    tmp = part()
    sp.scad_render_to_file(tmp, include_orig_code = False)
    # One line per variant to generate all .scad files
    # sp.scad_render_to_file(part(variant = B), include_orig_code = False)
    bom = spu.bill_of_materials(tmp, csv=True)
    print(bom)
