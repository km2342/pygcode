=======
pygcode
=======

GCODE Parser for Python

Currently in development, ``pygcode`` is a low-level GCode interpreter
for python.


Changes made
============

-- This fork allows the user to pass the amount of decimal places that
they want (maximum of 6 to prevent user error) the X and Y letters
to display to allow for greater precision.

-- mappings for specific letters and conversion from letters to gcode in gcodes.py

-- The dependencies are pinned to prevent blockers in production.

-- The letters 'S' and 'H' are treated as strings instead of floats to prevent
issues with the CNC machine.

-- setup.py is now able to install pygcode via pip to virtual environments.


Installation
============

Install using ``pip``

``pip install git+https://github.com/km2342/pygcode``


Documentation
=============

`Check out the wiki <https://github.com/fragmuffin/pygcode/wiki>`__ for documentation.

