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
import math
import solid as sp
import solid.utils as spu

import v2901 as bearing

# SCAD imports
assembly = sp.import_scad('../lib/MCAD/assembly/attach.scad')
chamfers = sp.import_scad('../lib/MCAD/fillets/chamfers.scad')
curved_text = sp.import_scad('../lib/MCAD/text/curved_text.scad')

# Config
dim10 = 80    # OD
dim11 = bearing.OD + 0.4  # bearing seat ID
dim13 = 16    # full height
dim14 = 38.5  # flange ID
dim15 = 2     # flange height
dim16 = dim13 - dim15   # bearing seat depth
PN_s = 5                # P/N character height
PN_d = 0.3              # P/N character depth
_code_name = "2911"
_version = ''

# Connectors
SPOOL_CONN = [[0, 0, dim16-bearing.B/2], [0, 0, 1], 0]
BEARING_CONN = [[0, 0, dim16], [0, 0, -1], 0]


@spu.bom_part(description = "Clamp", code_name = _code_name)
def part(variant = '', configuration = '', debug = False):
    out_cyl = sp.cylinder(h=dim15+0.001, d=dim10)
    cone = sp.cylinder(h=dim16, d1=dim10, d2=dim11)
    cone = sp.translate([0,0,dim15])(cone)
    tmp = out_cyl + cone
    bseat = sp.translate([0,0,-0.1])( sp.cylinder(d=dim11, h=dim16+0.1) )
    tmp -= bseat
    flange = sp.cylinder(d=dim14, h=dim15+0.2)
    flange = sp.translate([0,0,dim16-0.1])(flange)
    tmp -= flange
    chamfer = chamfers.mcad_chamfer_cylinder(diameter = dim11,
                                             length = 1.5,
                                             angle = 30,
                                             depth = None,
                                             internal = True)
    tmp -= chamfer
    pn = curved_text.mcad_circle_text(diameter=(dim10+dim11)/2-PN_s,
                                      t = _code_name+_version+variant,
                                      size = PN_s,
                                      font = "Open Sans:style=Bold",
                                      halign = "center",
                                      valign = "baseline",
                                      spacing = 1,
                                      direction = "cw")
    pn = sp.linear_extrude(PN_d+0.001)( pn )
    tmp -= sp.translate([0,0,PN_d])( sp.rotate([0,180,0])(pn) )
    if debug: tmp += assembly.connector(SPOOL_CONN)
    if debug: tmp += assembly.connector(BEARING_CONN)
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
        filename = parser.prog.replace(".py","")+args.version+variant
        tmp = part(variant=variant, debug=args.debug)
        sp.scad_render_to_file(tmp, filepath=filename+".scad",
                               include_orig_code = False)
