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

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')

# Config
ID = 25
OD = 42
B =   9

# Connectors
RACEI_CONN = [[0, 0, 0], [0, 0,  1], 0]
RACEO_CONN = [[0, 0, B], [0, 0, -1], 0]

@spu.bom_part(description = "Bearing", code_name = "6905-ZZ")
def part(variant = '', configuration = '', debug = False):
    tmp = sp.cylinder(d=OD, h=B)
    tmp -= sp.translate([0,0,-0.1])(sp.cylinder(d=ID, h=B+0.2))
    if debug: tmp += assembly.connector(RACEI_CONN)
    if debug: tmp += assembly.connector(RACEO_CONN)
    return tmp

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help = "include debug code on SCAD render")
    parser.add_argument('-e', '--version', default='',
                        help = "add 'VERSION' to P/N")
    args = parser.parse_args()

    for variant in ['']:
        filename = parser.prog.replace(".py","")+args.version+variant
        tmp = part(variant=variant, debug=args.debug)
        sp.scad_render_to_file(tmp, filepath=filename+".scad",
                               include_orig_code = False)
