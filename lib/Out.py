"""
 * cros project                                              https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import sys
import time

def log(logname, txt, console=False, exit=False):
    if logname == "__DEBUG__": logname = "debug.log"
    file = open(logname, "a")
    file.write(time.strftime("%c") + " | ")
    file.write(txt)
    file.write("\n")
    file.close()
    if console: print(txt)
    if exit: sys.exit()
