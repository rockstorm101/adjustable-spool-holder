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
threads = sp.import_scad('../lib/MCAD/fasteners/threads.scad')
chamfers = sp.import_scad('../lib/MCAD/fillets/chamfers.scad')
curved_text = sp.import_scad('../lib/MCAD/text/curved_text.scad')

# Config
dim10 = 14              # first step height
B_h = bearing.B + 1.4   # bearing seat height
F_d = 29.5              # flange OD, which the bearing seats against
B_d = bearing.ID - 0.2  # bearing seat diam
dim14 = 120             # full length
T_d = 20                # thread nom diam
T_p = 2.5               # thread pitch
T_c = 0.5               # thread clearance
PN_s = 5                # P/N character height
PN_d = 0.3              # P/N character depth
dim17 = dim14 - dim10 - B_h  # thread length
_code_name = "2910"
_version = ''


# Connectors
BEARING_CONN = [[0, 0, dim10], [0, 0, 1], 0]
NUT_CONN =     [[0, 0, dim14-20.2], [0, 0, -1], 0]

@spu.bom_part(description = "Screw", code_name = _code_name)
def part(variant = '', configuration = '', debug = False):
    tmp = sp.cylinder(d=F_d, h=dim10)
    tmp += sp.translate([0,0,dim10])( bseat() )
    thread = chamfers.mcad_chamfered_cylinder(dim17, internal = False)(
        threads.metric_thread(diameter = T_d,
                              pitch = T_p,
                              length = dim17,
                              internal = False,
                              clearance = T_c ),
        chamfers.mcad_chamfer_cylinder(T_d, T_p+0.25, angle = None, depth=None,
                                       internal = False)
    )
    tmp += sp.translate([0,0,dim17+B_h+dim10])( sp.rotate([180,0,0])(thread) )
    tmp += sp.rotate([180,0,0])(
        sp.translate([0,0,-0.2])(
            sp.import_(
                "../aux/Ender_3_spool_holder/" +
                "Ender3_Spool_Holder_Coupling.stl") ) )
    pn = curved_text.mcad_cylinder_text(diameter=F_d-2*PN_d,
                                        t = _code_name+_version+variant,
                                        depth = PN_d+0.001,
                                        size = PN_s,
                                        font = "Open Sans:style=Bold",
                                        halign = "center",
                                        valign = "bottom",
                                        spacing = 1,
                                        direction = "ccw")
    tmp -= sp.translate([0,0,dim10/2-PN_s/2])( pn )
    if debug: tmp += assembly.connector(BEARING_CONN)
    return tmp

def bseat():
    d = B_d
    h = B_h+0.001
    tmp = chamfers.mcad_chamfered_cylinder(h, internal=False)(
        sp.cylinder(d=d, h=h),
        chamfers.mcad_chamfer_cylinder(diameter = d,
                                       length = None,
                                       angle = 30,
                                       depth = 1,
                                       internal = False)
    )
    tmp = sp.translate([0,0,h-0.001])( sp.rotate([180,0,0])(tmp) )
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
