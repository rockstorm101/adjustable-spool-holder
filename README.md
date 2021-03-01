# Adjustable Spool Holder

Spool holder which adapts to different widths and diameters of
filament spools while providing a smooth rolling experience on all
cases.

## Bill of Materials

Part Number | Description  | Quantity
   :---     |     :---     |  :---:
291010      | Screw        |    1
6905-ZZ     | Bearing      |    2
291110      | Clamp        |    2
291210      | Nut, Bearing |    1
291310      | Nut          |    1

This holder is designed to use bearings of size 42x25x9
(6905-xx). Same bearings but with different shields/seals
(i.e. 6905-2RS) should work too. For this type of application any
bearing quality would do.

## Print Settings
### Screw (2910)
- Rafts: No
- Supports: Yes
- Resolution:
  - <= 0.1 mm on the coupling ramp (start Z: 2.8 mm, finish Z: 3.8 mm)
  - <= 0.1 mm on the threaded section (start Z: 41.0 mm, finish Z: 136.6 mm)
  - Any layer height elsewhere (I used 0.2 mm)
- Infill: >= 50%
- Vertical Shells: 3

### Clamp (2911)
- Rafts: No
- Supports: No
- Resolution: Any (I used 0.2 mm)
- Infill: >= 50%
- Vertical Shells: 3

### Nut, Bearing (2912)
- Rafts: No
- Supports: No
- Resolution: <= 0.1 mm
- Infill: >= 20%
- Vertical Shells: 3

### Nut (2913)
- Rafts: No
- Supports: No
- Resolution: <= 0.1 mm
- Infill: >= 20%
- Vertical Shells: 3

## Customise / Compile / Build
### Build STL files

Generate the intermediate SCAD file with the following command. Replace
<...> with the relevant file/name on each case. With no other parameters
this will generate a file called `<source_file>.scad`.
```
python <source_file>.py
```

Generate the STL file with:
```
openscad -o <stl_file>.stl <source_file>.scad
```

### Requirements
- [SolidPython][6]: a python front-end for solid modelling to OpenSCAD
- [OpenSCAD][7]: a solid 3D CAD modeller
- [Custom MCAD][8]: customised version of the MCAD library ('more-dev' branch)
- The [Open Sans][9] font (paticularly the "Bold" style)

[6]: https://github.com/SolidCode/SolidPython
[7]: http://www.openscad.org
[8]: https://github.com/rockstorm101/MCAD/tree/more-dev
[9]: https://www.1001freefonts.com/open-sans.font

## Assembly

See images on `doc/images`. Orientation of the Clamps and the Nut are
critical. Clamps contact the bearings on their outer race and the
Screw and Nut contact the bearings on their inner race. It is critical
that these contacts occur on opposite sides of the bearings.

## Credits

The end coupling to be able to use the original nut from an Ender 3
spool holder is taken from [Ender 3 spool holder][1] by [@emolan][2].

[1]: https://www.thingiverse.com/thing:3979065
[2]: https://www.thingiverse.com/emolan

The font used for engraving is [Open Sans][9] by Steve Matteson.


## License
![open source hardware][3]
[![CC BY-SA 4.0][5]][4]

```
Copyright (c) 2021 Rock Storm

This work is open source hardware: you can redistribute it and/or modify
it under the terms of the Attribution-ShareAlike 4.0 International.

The code generating the models is distributed under the GNU General
Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

This work is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.
```

[3]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[4]: https://creativecommons.org/licenses/by-sa/4.0/
[5]: https://i1.wp.com/www.oshwa.org/wp-content/uploads/2014/03/oshw-logo-100-px.png
