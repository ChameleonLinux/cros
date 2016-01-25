"""
 * cros project                                              https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
from lib import crosinfo
from lib.magic import magic
import os
from sdk import Hooks
def send(handself, path, extra={}, nogzip=False):
    Hooks.run("headers", [handself, extra, nogzip])
    if not path is "skip":
        Hooks.run("headers_pathknown", [handself, path, extra, nogzip])
        mime = None
        mimem = None
        if os.name == "nt":
            magicfile = os.getcwd() + "\\magic"
            mimem = magic.Magic(magic_file=magicfile,mime=True)
        else: mimem = magic.Magic(mime=True)
        handself.send_header("Content-Type", bytes.decode(mimem.from_file(path)))
    for header, value in handself.ServerConfiguration.Headers.items(): handself.send_header(header, value)
    if handself.ServerConfiguration.Gzip == True and nogzip==False: handself.send_header("Content-Encoding", "gzip")
    for key, value in extra.items(): handself.send_header(key, value)
    if getattr(handself, "end_headers", None): handself.end_headers()
