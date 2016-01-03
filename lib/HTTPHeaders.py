from lib import crosinfo
from lib.magic import magic
import os
def send(handself, path):
    if not path is "skip":
        mime = None
        mimem = None
        if os.name == "nt":
            magicfile = os.getcwd() + "\\magic"
            mimem = magic.Magic(magic_file=magicfile,mime=True)
        else: mimem = magic.Magic(mime=True)
        handself.send_header("Content-Type", bytes.decode(mimem.from_file(path)))
    for header, value in handself.ServerConfiguration.Headers.items(): handself.send_header(header, value)
    if handself.ServerConfiguration.XPoweredBy == True: handself.send_header("X-Powered-By", "cros/" + crosinfo.Version)
    if handself.ServerConfiguration.Gzip == True: handself.send_header("Content-Encoding", "gzip")
    handself.end_headers()
