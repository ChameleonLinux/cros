"""
 * cros project                                              https://wolflinux.org/s/4jRm3
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://wolflinux.org/s/mmdoe
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import http.server
from lib import BasicMixIn, HTTPHeaders

class HTTP(BasicMixIn.MixIn, http.server.BaseHTTPRequestHandler):
    ServerConfiguration = None

    def __init__(self, request, client_address, srvconf, serverself):
        self.ServerConfiguration = srvconf
        self.request = request
        self.client_address = client_address
        self.server = serverself
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

class SPDY(BasicMixIn.MixIn, spdylay.BaseSPDYRequestHandler):
    ServerConfiguration = None

    def __init__(self, request, client_address, srvconf, serverself):
        self.ServerConfiguration = srvconf
        spdylay.BaseSPDYRequestHandler.__init__(self, request, client_address, serverself)

    def do_GET(self):
        """Serve a GET request."""
        if self.Banned(): return None
        path = self.translate_path(self.path)
        f = self.Authorize(path)
        if self.checkAccess(path) == None or f == None or self.Authenticate() == False: return None
        self.send_response(200)
        HTTPHeaders.send(self, path)
        self.Send(f.read())

    def log_request(self, code='-', size='-'):
        self.Log('Access', self.requestline)
