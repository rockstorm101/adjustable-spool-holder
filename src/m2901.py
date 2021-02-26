# This file is part of the Adjustable Spool Holder.
#
# This source file is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Copyright 2021 Rock Storm <rockstorm at gmx dot com>

# m2901.py -- Mock-Up Spool

# Python imports
import argparse
import solid as sp
import solid.utils as spu

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')

# Config
dim10 = 3  # flange thickness
dim11 = 60  # ID
dim12 = 63  # width
dim13 = 200 # OD


# Connectors
FWD_CLAMP_CONN = [[0, 0, dim12/2], [0, 0, -1], 0]
AFT_CLAMP_CONN = [[0, 0, -dim12/2], [0, 0, 1], 0]

def part(variant = '', configuration = '', debug = False):
    tmp = sp.cylinder(d=dim11+2*dim10, h=dim12-0.2, center=True)
    ear = sp.cylinder(d=dim13, h=dim10)
    for z in [dim12/2-dim10, -dim12/2]:
        tmp += sp.translate([0,0,z])(ear)
    tmp -= sp.cylinder(d=dim11, h=dim12+0.2, center=True )
    if debug: tmp += assembly.connector(FWD_CLAMP_CONN)
    if debug: tmp += assembly.connector(AFT_CLAMP_CONN)
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
