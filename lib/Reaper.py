"""
 * reaper project                                            https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import inspect

class private():
    @staticmethod
    def print(msg):
        print(msg, end="")

def deprecated(alternative=None, reason=None):
    calledby = inspect.getouterframes(inspect.currentframe(), 2)[1][3]
    private.print("Function " + calledby + " is deprecated and should not be used.")
    if alternative != None: private.print(" However, " + alternative + " is available.")
    if reason != None: private.print("\nReason: " + reason)
    print()
