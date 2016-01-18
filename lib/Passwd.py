"""
 * cros project                                              https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import hashlib
import sys
import base64

def Hash(user, password):
    user = user
    password = password
    d = '%s:%s' % (user, password)
    g = base64.b64encode(d.encode("utf-8"))
    m = hashlib.md5(g)
    g = hashlib.sha256(m.hexdigest()[:25].encode('utf-8')).hexdigest()
    l = int(len(g)/2)
    g = g[:l]
    return g

def Compare(authstr, hash_):
    m = hashlib.md5(authstr.encode("utf-8"))
    g = hashlib.sha256(m.hexdigest()[:25].encode('utf-8')).hexdigest()
    l = int(len(g)/2)
    g = g[:l]
    return g == hash_

if __name__ == "__main__":
    print(Hash(sys.argv[1], sys.argv[2]))
