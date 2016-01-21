"""
 * cros project                                              https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
global hooks
try:
    hooks
except Exception: hooks = {"startup": [], "servers-init": []}

def register_trigger(name, func, args=None):
    hooks[name].append([func, args])
def register(name):
    hooks.update({name: []})

hook = register
trigger = register_trigger

def run(name, args):
    for func in hooks[name]:
        func[0](args, func[1])
