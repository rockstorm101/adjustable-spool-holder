# This file is part of the Adjustable Spool Holder.
#
# This source file is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Copyright 2021 Rock Storm <rockstorm at gmx dot com>

# Python imports
import argparse
import solid as sp
import solid.utils as spu

spu.set_bom_headers("code_name")

# Import parts to be assembled
import p2910 as screw
import p2911 as clamp
import p2912 as nut
import p2913 as cnut
import v2901 as bearing
import m2901 as spool

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')

def assy(variant = '', configuration = '', debug = False):
    C = sp.color("SeaGreen", 1)( clamp.part(debug=debug) )
    B = bearing.part(debug=debug)
    N = sp.color("Plum", 1)( nut.part(debug=debug) )
    S = sp.color("Khaki", 1)(screw.part(debug=debug))
    P = sp.color("White", 0.5)(spool.part(debug=debug))
    CN = sp.color("Orange", 1)(cnut.part(debug=debug))

    tmp = N + assembly.attach(nut.THREAD_CONN, cnut.THREAD_CONN)(CN)
    tmp = B + assembly.attach(bearing.RACEI_CONN, nut.BEARING_CONN)(tmp)
    tmp = C + assembly.attach(clamp.BEARING_CONN, bearing.RACEO_CONN)(tmp)
    tmp = P + assembly.attach(spool.FWD_CLAMP_CONN, clamp.SPOOL_CONN)(tmp)
    tmp = C + assembly.attach(clamp.SPOOL_CONN, spool.AFT_CLAMP_CONN)(tmp)
    tmp = B + assembly.attach(bearing.RACEO_CONN, clamp.BEARING_CONN)(tmp)
    tmp = S + assembly.attach(screw.BEARING_CONN, bearing.RACEI_CONN)(tmp)

    tmp = sp.rotate([0,90,0])(tmp)

    if debug:
        tmp *= sp.translate([0,1000,0])(
            sp.cube([2000,2000,2000], center = True)
        )
    return tmp

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help = "include debug code on SCAD render")
    parser.add_argument('-e', '--version', default = '',
                        help = "add 'VERSION' to P/N")
    args = parser.parse_args()

    for variant in ['']:
        filename = parser.prog.replace(".py","")+args.version+variant
        tmp = assy(variant=variant, debug=args.debug)
        sp.scad_render_to_file(tmp, filepath=filename+".scad",
                               include_orig_code = False)
        bom = spu.bill_of_materials(tmp, csv=True)
        with open(filename+"BOM.csv", 'w') as bom_file:
            bom_file.write(bom)
