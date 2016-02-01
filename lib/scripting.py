"""
 * cros project                                              https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import subprocess, os
from lib import Out

class CGIResponse:
    headers = {}
    content = b''
    status = 500

    def __init__(self, output):
        end_of_headers = False
        output = output.split(b'\n')
        for ln in output:
            if end_of_headers == False:
                ln = ln.decode('utf-8')
                if ln in ('\r\n', '\n', '', '\r'):
                    end_of_headers = True
                    continue
                h = ln.split(':', 1)
                self.headers[h[0].strip()] = h[1].strip()
            else:
                self.content = self.content + b"\n" + ln
        status = self.headers.get("Status")
        if status:
            self.status = int(status.split(" ")[0])

def run(relativepath, path, documentroot, serversoftware, serverprotocol, remoteaddr,
        requestheaders, lb, lc, post="", qs="", servername="127.0.0.1", requestmethod="GET",
        https="off", contentlength=0):
    script_env = {}
    script_env["SCRIPT_FILENAME"] = path
    script_env["DOCUMENT_ROOT"] = documentroot
    script_env["QUERY_STRING"] = qs
    script_env["SERVER_NAME"] = servername
    script_env["HTTPS"] = https
    script_env["REQUEST_URI"] = relativepath
    script_env["GATEWAY_INTERFACE"] = "CGI/1.1"
    script_env["SERVER_SOFTWARE"] = serversoftware
    script_env["SERVER_PROTOCOL"] = serverprotocol
    script_env["REDIRECT_STATUS"] = "1"
    script_env["REQUEST_METHOD"] = requestmethod
    script_env["REMOTE_ADDR"] = remoteaddr
    script_env["PHP_SELF"] = relativepath
    script_env["SCRIPT_NAME"] = path
    if requestmethod in ['POST', 'PUT']:
        script_env['POST_DATA'] = post.read(contentlength).decode()
        script_env['CONTENT_LENGTH'] = str(contentlength)
    p = subprocess.Popen(lb.replace("^filename", path) + " " + lc.replace("^filename", path), stdout=subprocess.PIPE, env=script_env, shell=True)
    std = p.communicate()
    stdout = std[0]
    stderr = std[1]
    return CGIResponse(stdout)
