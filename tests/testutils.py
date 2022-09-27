# utilities for the testing suite (as opposed to the tests for utils.py)
import sys
import os
import inspect

import re


# Units Under Test
_pygcode_in_path = False
def add_pygcode_to_path():
    global _pygcode_in_path
    if not _pygcode_in_path:
        if os.environ.get('PYGCODE_TESTSCOPE', 'local') == 'installed':
            # Run tests on the `pip install` installed libray
            pass  # nothing to be done
        else:
            # Run tests explicitly on files in ../src (ignore any installed libs)
            # Add pygcode_mod (relative to this test-path) to the system path
            _this_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            sys.path.insert(0, os.path.join(_this_path, '../..', 'src'))

        _pygcode_in_path = True

add_pygcode_to_path()


# String Utilities
def str_lines(text):
    """Split given string into lines (ignore blank lines, and automagically strip)"""
    for match in re.finditer(r'\s*(?P<content>.*?)\s*\n', text):
        yield match.group('content')
