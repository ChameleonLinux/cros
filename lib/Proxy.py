"""
 * cros project                                              https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import urllib.request
from lib.magic import magic
import gzip

def Get(url, ip, headers, cheaders):
    heads = {"X-Forwarded-For": ip[0]}
    for key, value in headers.items():
        heads.update({key: value})
    for key, value in cheaders.items():
        if key.lower() != 'accept-encoding':
            heads.update({key: value})
    req = urllib.request.Request(url, headers=heads)
    res = urllib.request.urlopen(req)
    response = res.read()
    mime = bytes.decode(magic.Magic(mime=True).from_buffer(response))
    if "gzip" in mime: response = gzip.decompress(response)
    return response
