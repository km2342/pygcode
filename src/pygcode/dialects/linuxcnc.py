"""
LinuxCNC

The linuxcnc gcode dialect is typically used for subtractive fabrication, such
as milling.

This dialect is the basis for all other dialects; GCodes and Words in other
dialects either inherit, or directly reference these classes.

**Specification:** http://www.linuxcnc.org

TODO: verify above info before publishing
"""
import re
import sys, os

os.path.dirname(os.path.abspath(__file__))
from .utils import WordType
from .. import config
from .. import words

# ======================== WORDS ========================

# Value cleaning functions
def _clean_codestr(value):
    if value < 10:
        return "0%g" % value
    return "%g" % value


def _clean_x_y(value):
    val = "%." + str(config.float_precision) + "f"
    fp_val = val % value
    return edge_case_clean(fp_val)


def clean_float(value):
    val = "%.3f" % value
    return edge_case_clean(val)


def edge_case_clean(string_clean):
    # removes leading zeros and the negative sign if the value a zero
    if float(string_clean) == 0:
        string_clean = string_clean.replace("-0.", ".")
        string_clean = string_clean.replace("-.", ".")
        string_clean = string_clean.replace("0.", ".")
    return string_clean


CLEAN_NONE = lambda v: v
# CLEAN_FLOAT = lambda v: "{0:.3}".format(v)
CLEAN_FLOAT = clean_float
CLEAN_X_Y_FLOAT = _clean_x_y
CLEAN_CODE = _clean_codestr
CLEAN_INT = lambda v: "%d" % v
# first parses for scientific notation, then for regular float values
REGEX_FLOAT_SCIENTIFIC_NOTATION = re.compile(r'^[+-]?\d+(?:\.\d*(?:[eE][+-]?\d+)?)?')
REGEX_FLOAT_INTEGER = re.compile(r'^\s*-?\d+\.?\d*|(-?\.\d+)')
REGEX_INT = re.compile(r'^\s*-?\d+')
REGEX_POSITIVEINT = re.compile(r'^\s*\d+')
REGEX_CODE = re.compile(r'^\s*\d+(\.\d)?') # float, but can't be negative

WORD_MAP = {
    # Descriptions copied from wikipedia:
    #   https://en.wikipedia.org/wiki/G-code#Letter_addresses

    # Rotational Axes
    'A': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Absolute or incremental position of A axis (rotational axis around X axis)",
        clean_value=CLEAN_FLOAT,
    ),
    'B': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Absolute or incremental position of B axis (rotational axis around Y axis)",
        clean_value=CLEAN_FLOAT,
    ),
    'C': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Absolute or incremental position of C axis (rotational axis around Z axis)",
        clean_value=CLEAN_FLOAT,
    ),
    'D': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Defines diameter or radial offset used for cutter compensation. D is used for depth of cut on lathes. It is used for aperture selection and commands on photoplotters.",
        clean_value=CLEAN_FLOAT,
    ),
    # Feed Rates
    'E': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Precision feedrate for threading on lathes",
        clean_value=CLEAN_FLOAT,
    ),
    'F': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Feedrate",
        clean_value=CLEAN_FLOAT,
    ),
    # G-Codes
    'G': WordType(
        value_class=float,
        value_regex=REGEX_CODE,
        alternate_regex=None,
        description="Address for preparatory commands",
        clean_value=CLEAN_CODE,
    ),
    # Tool Offsets
    'H': WordType(
        value_class=float,
        value_regex=REGEX_CODE,
        alternate_regex=None,
        description="Defines tool length offset; Incremental axis corresponding to C axis (e.g., on a turn-mill)",
        clean_value=CLEAN_CODE,
    ),
    # Arc radius center coords
    'I': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Defines arc center in X axis for G02 or G03 arc commands. Also used as a parameter within some fixed cycles.",
        clean_value=CLEAN_FLOAT,
    ),
    'J': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Defines arc center in Y axis for G02 or G03 arc commands. Also used as a parameter within some fixed cycles.",
        clean_value=CLEAN_FLOAT,
    ),
    'K': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Defines arc center in Z axis for G02 or G03 arc commands. Also used as a parameter within some fixed cycles, equal to L address.",
        clean_value=CLEAN_FLOAT,
    ),
    # Loop Count
    'L': WordType(
        value_class=int,
        value_regex=REGEX_POSITIVEINT,
        alternate_regex=None,
        description="Fixed cycle loop count; Specification of what register to edit using G10",
        clean_value=CLEAN_INT,
    ),
    # Miscellaneous Function
    'M': WordType(
        value_class=float,
        value_regex=REGEX_CODE,
        alternate_regex=None,
        description="Miscellaneous function",
        clean_value=CLEAN_CODE,
    ),
    # Line Number
    'N': WordType(
        value_class=int,
        value_regex=REGEX_POSITIVEINT,
        alternate_regex=None,
        description="Line (block) number in program; System parameter number to change using G10",
        clean_value=CLEAN_INT,
    ),
    # Program Name
    'O': WordType(
        value_class=str,
        value_regex=re.compile(r'^.+$'), # all the way to the end
        alternate_regex=None,
        description="Program name",
        clean_value=CLEAN_NONE,
    ),
    # Parameter (arbitrary parameter)
    'P': WordType(
        value_class=float, # parameter is often an integer, but can be a float
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Serves as parameter address for various G and M codes",
        clean_value=CLEAN_FLOAT,
    ),
    # Peck increment
    'Q': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Depth to increase on each peck; Peck increment in canned cycles",
        clean_value=CLEAN_FLOAT,
    ),
    # Arc Radius
    'R': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Defines size of arc radius, or defines retract height in milling canned cycles",
        clean_value=CLEAN_FLOAT,
    ),
    # Spindle speed
    'S': WordType(
        value_class=float,
        value_regex=REGEX_CODE,
        alternate_regex=None,
        description="Defines speed, either spindle speed or surface speed depending on mode",
        clean_value=CLEAN_CODE,
    ),
    # Tool Selecton
    'T': WordType(
        value_class=str,
        value_regex=REGEX_POSITIVEINT, # tool string may have leading '0's, but is effectively an index (integer)
        alternate_regex=None,
        description="Tool selection",
        clean_value=CLEAN_NONE,
    ),
    # Incremental axes
    'U': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Incremental axis corresponding to X axis (typically only lathe group A controls) Also defines dwell time on some machines (instead of 'P' or 'X').",
        clean_value=CLEAN_FLOAT,
    ),
    'V': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Incremental axis corresponding to Y axis",
        clean_value=CLEAN_FLOAT,
    ),
    'W': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Incremental axis corresponding to Z axis (typically only lathe group A controls)",
        clean_value=CLEAN_FLOAT,
    ),
    # Linear Axes
    'X': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Absolute or incremental position of X axis.",
        clean_value=CLEAN_X_Y_FLOAT,
    ),
    'Y': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Absolute or incremental position of Y axis.",
        clean_value=CLEAN_X_Y_FLOAT,
    ),
    'Z': WordType(
        value_class=float,
        value_regex=REGEX_FLOAT_SCIENTIFIC_NOTATION,
        alternate_regex=REGEX_FLOAT_INTEGER,
        description="Absolute or incremental position of Z axis.",
        clean_value=CLEAN_FLOAT,
    ),
}

# ======================== G-CODES ========================
