"""
 * cros project                                              https://wolflinux.org/s/4jRm3
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://wolflinux.org/s/mmdoe
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import sys

def log(logname, txt, console=False, exit=False):
    file = open(logname, "a")
    file.write(txt)
    file.write("\n")
    file.close()
    if console: print(txt)
    if exit: sys.exit()
