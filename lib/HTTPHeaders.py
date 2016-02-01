"""
 * cros project                                              https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
from lib import crosinfo, Out
from lib.magic import magic
import os, mimetypes
from sdk import Hooks
def send(handself, path, extra={}, nogzip=False):
    Hooks.run("headers", [handself, extra, nogzip])
    if path != "skip":
        Hooks.run("headers_pathknown", [handself, path, extra, nogzip])
        mimem = mimetypes.MimeTypes()
        mime = mimem.guess_type(path)[0]
        if mime == None:
            mimem = magic.Magic(mime=True)
            mime = mimem.from_file(path).decode('utf-8')
        handself.send_header("Content-Type", mime)
    for header, value in handself.ServerConfiguration.Headers.items(): handself.send_header(header, value)
    if handself.ServerConfiguration.Gzip == True and nogzip==False: handself.send_header("Content-Encoding", "gzip")
    for key, value in extra.items(): handself.send_header(key, value)
    if getattr(handself, "end_headers", None): handself.end_headers()
