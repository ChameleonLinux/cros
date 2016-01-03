"""
 * cros project                                              https://wolflinux.org/s/4jRm3
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://wolflinux.org/s/mmdoe
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import http.server
import posixpath
import socketserver
import os
import urllib
from urllib.parse import unquote
from lib import HTTPHeaders, Out, Gzip
import mimetypes

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    ServerConfiguration = None
    AlternativeErrorDocs = {'404': """<!DOCTYPE html>
    <head>
    <meta charset="utf-8">
    <title>404 Not Found</title>
    </head>
    <body>
    <h1>404 Not Found</h1>
    </body>
    </html>""",
    '403': """<!DOCTYPE html>
    <head>
    <meta charset="utf-8">
    <title>403 Forbidden</title>
    </head>
    <body>
    <h1>403 Forbidden</h1>
    </body>
    </html>"""}

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

    def do_GET(self):
        """Serve a GET request."""
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                path = os.path.join(path, "/")
            # Get index file
            for indfile in self.ServerConfiguration.IndexFiles:
                if os.path.isfile(os.path.join(path, indfile)): path = os.path.join(path, indfile)
        accessnode = self.ServerConfiguration.Access
        if accessnode['Enable']:
            for bpath in accessnode['blockedPaths']:
                if path.startswith(bpath):
                    self.ReturnError(403, 'Access')
                    return None
            if os.path.splitext(path)[1] in accessnode['blockedExtensions']:
                self.ReturnError(403, 'Access')
                return None
        if os.path.isfile(path):
            try:
                f = open(path, 'rb')
            except IOError:
                self.ReturnError(403, 'Access')
                return None
        else:
            self.ReturnError(404, 'Access')
            return None

        self.send_response(200)
        HTTPHeaders.send(self, path)
        self.Send(f.read())

    def Send(self, data):
        dataa = data
        if self.ServerConfiguration.Gzip: dataa = Gzip.encode(data)
        self.wfile.write(dataa)

    def do_HEAD(self):
        HTTPHeaders.send(self)

    def translate_path(self, path):
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = os.path.normpath(urllib.parse.unquote(path))
        path = self.ServerConfiguration.Directory + path
        return path

    # Override built-in logging
    def log_request(self, code='-', size='-'):
        self.Log('Access', self.requestline)

    def ReturnError(self, code, etype):
        self.send_response(code)
        HTTPHeaders.send(self, 'skip')
        print(self.ServerConfiguration.Errors)
        errordocpath = self.ServerConfiguration.Errors[code]
        self.Log(etype, "Returned " + str(code) + ".")
        if os.path.isfile(errordocpath):
            f = open(errordocpath, "rb")
            self.wfile.write(f.read())
        else:
            self.wfile.write(self.AlternativeErrorDocs[str(code)])

    def Log(self, key, msg, show=False, exit=False):
        path=""
        if hasattr(self, 'path'): path=self.path
        if self.ServerConfiguration.Logging['Enable']:
            Out.log(self.ServerConfiguration.Logging[key], self.client_address[0] + " | " + msg + " | " + path, show, exit)
