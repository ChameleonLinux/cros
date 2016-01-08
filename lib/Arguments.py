"""
 * cros project                                              https://wolflinux.org/s/4jRm3
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://wolflinux.org/s/mmdoe
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import re
import sys

def get(namesre, isshort=False):
    i = 0
    # For each argument
    for arg in sys.argv:
        i += 1
        # If argument matches regex (e.g. --config is wanted)
        if namesre.match(arg):
            # If is short, return True
            if isshort: return True
            # If not, return next.
            else: return sys.argv[i]
    # If there is no wanted argument, return False
    return False
