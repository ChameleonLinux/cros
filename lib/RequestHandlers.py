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
from lib import HTTPHeaders, Out, Gzip, Passwd
import mimetypes
import base64
import cgi

class HTTP(http.server.BaseHTTPRequestHandler):
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
        if self.Banned(): return None
        path = self.translate_path(self.path)
        f = self.Authorize(path)
        if self.checkAccess(path) == None or f == None or self.Authenticate() == False: return None
        self.send_response(200)
        HTTPHeaders.send(self, path)
        self.Send(f.read())

    def Banned(self):
        if self.client_address in self.ServerConfiguration.BannedIPs:
            self.ReturnError(403)
            return True
        return False

    def checkAccess(self, path, honly=False):
        accessnode = self.ServerConfiguration.Access
        if accessnode['Enable']:
            for bpath in accessnode['blockedPaths']:
                if path.startswith(bpath):
                    self.ReturnError(403, 'Access', honly)
                    return None
            if os.path.splitext(path)[1] in accessnode['blockedExtensions']:
                self.ReturnError(403, 'Access', honly)
                return None
        return True

    def Send(self, data):
        dataa = data
        if self.ServerConfiguration.Gzip and 'gzip'.lower() in self.headers['Accept-Encoding'].lower(): dataa = Gzip.encode(data)
        self.wfile.write(dataa)

    def do_HEAD(self):
        path = self.translate_path(self.path)
        if self.Authorize(path, True) != None or self.checkAccess(path, True) != None: self.send_response(200)
        HTTPHeaders.send(self, path)

    def translate_path(self, path):
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = os.path.normpath(urllib.parse.unquote(path))
        path = self.ServerConfiguration.Directory + path
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                path = os.path.join(path, "/")
            # Get index file
            for indfile in self.ServerConfiguration.IndexFiles:
                if os.path.isfile(os.path.join(path, indfile)): path = os.path.join(path, indfile)
        return path

    def Authorize(self, path, honly=False):
        f = None
        if os.path.isfile(path):
            try:
                f = open(path, 'rb')
            except IOError:
                self.ReturnError(403, 'Access', honly)
                return None
        else:
            self.ReturnError(404, 'Access', honly)
            return None
        return f

    # Override built-in logging
    def log_request(self, code='-', size='-'):
        self.Log('Access', self.requestline)

    def ReturnError(self, code, etype, honly=False):
        self.send_response(code)
        self.Log(etype, "Returned " + str(code) + ".")
        if honly == False:
            errordocpath = self.ServerConfiguration.Errors["e" + str(code)]
            if os.path.isfile(errordocpath):
                HTTPHeaders.send(self, errordocpath)
                f = open(errordocpath, "rb")
                self.Send(f.read())
            else:
                HTTPHeaders.send(self, 'skip', {'Content-Type': 'text/html'})
                self.Send(self.AlternativeErrorDocs[str(code)].encode("utf-8"))

    def do_AUTHHEAD(self, arr):
        path = self.translate_path(self.path)
        if self.Authorize(path, True) != None or self.checkAccess(path, True) != None: self.send_response(401)
        authh = {"WWW-Authenticate": 'Basic'}
        if 'reason' in arr:
            authh = {"WWW-Authenticate": 'Basic realm=\"%r\"' % arr['reason']}
        HTTPHeaders.send(self, path, authh)

    def Authenticate(self):
        for arr in self.ServerConfiguration.Authentication:
            if arr['path'] == self.path:
                if 'IPs' in arr:
                    if self.client_address[0] in arr['IPs']: return True
                if 'Authorization' in self.headers:
                        auth = self.headers['Authorization'][6:]
                        if Passwd.Compare(auth, arr['passwd']): return True
                self.do_AUTHHEAD(arr)
                return False

    def Log(self, key, msg, show=False, exit=False):
        path=""
        if hasattr(self, 'path'): path=self.path
        if self.ServerConfiguration.Logging['Enable']:
            Out.log(self.ServerConfiguration.Logging[key], self.client_address[0] + " | " + msg + " | " + path, show, exit)
