"""
 * cros project                                              https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
from sdk import IfNoneUseDefault
import os, time
def Get(p, name, default):
    return IfNoneUseDefault.get_d(p[0].ServerConfiguration.MeDict, name, default)
