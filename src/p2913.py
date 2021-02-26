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

# Project imports
import p2912 as nut

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')
chamfers = sp.import_scad('../lib/MCAD/fillets/chamfers.scad')

# Config
N_af = nut.N_af        # nut across-flats dimension
N_h = nut.N_h          # nut height
_code_name = "2913"
_version = ''

# Connectors
THREAD_CONN = [[0, 0, 0], [0, 0, -1], 0]

@spu.bom_part(description = "Nut", code_name = _code_name)
def part(variant = '', configuration = '', debug = False):
    tmp = nut.hexagon()
    tmp -= nut.thread(N_h)
    outer_chamfer = chamfers.mcad_chamfer_cylinder(diameter = N_af+10,
                                                   length = 5,
                                                   angle = 90-15,
                                                   depth = None,
                                                   internal = False)
    outer_chamfer = sp.translate([0,0,N_h])( sp.rotate([180,0,0])(outer_chamfer))
    tmp -= outer_chamfer
    tmp -= nut.locate_part_number(_code_name+_version+variant)
    if debug: tmp += assembly.connector(THREAD_CONN)
    return tmp

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help = "include debug code on SCAD render")
    parser.add_argument('-e', '--version', default='',
                        help = "add 'VERSION' to P/N")
    args = parser.parse_args()
    _version = args.version

    for variant in ['']:
        filename = parser.prog.replace(".py","")+_version+variant
        tmp = part(variant=variant, debug=args.debug)
        sp.scad_render_to_file(tmp, filepath=filename+".scad",
                               include_orig_code = False)
