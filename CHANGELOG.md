# Changelog

## Unreleased

### Added

- 2910: Extended Screw by 20 mm
- Added argument parsing and a 'version' parameter to all sources
- Added a filament spool mockup (m2901)
- 2912: Changed size and font of scribed P/N

### Fixed
- 2910: Fixed Screw not using thread clearance parameter
- Removed unsued functions (which are now ported to MCAD)

## 0.1

### Added

- Thread clearance reduced to 0.3 mm
- Added nut-like feature and scribed P/N to Nut (2912)
- Sharp edges removed and added lead-in chamfer to Clamp (2911)
- GA (2900) generates BoM

### Fixed

- Connector calls/naming
- Fixed 'debug' parameter call on GA (2900)

## 0.1-p7 - Thread Fit Test
 - Updated MCAD file to produce threads
 - Thread clearances: 0.4 mm on both male and female
 - g1: layer height 0.2 mm
 - g2: layer height 0.1 mm on threaded areas

## 0.1-p6 - Thread Fit Test
 - Thread clearances: -0.5 on male and +0.5 on female.
 - Thread printed at 0.1 layer height.
 - Using version 2.5 of threads file

## 0.1-p2 - Coupling Fit Test
 - Ramp printed a 0.1 mm layer height
 - Supports everywhere

## 0.1-p1 - Thread Fit Test
 - Using version 1.3 of threads file

