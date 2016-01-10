"""
 * cros project                                              https://wolflinux.org/s/4jRm3
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://wolflinux.org/s/mmdoe
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import http.server
from lib import BasicMixIn, HTTPHeaders, Out
import spdylay
import socketserver

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
        #spdylay.BaseSPDYRequestHandler.__init__(self, request, client_address, serverself)
        socketserver.BaseRequestHandler.__init__(self, request, client_address, serverself)
