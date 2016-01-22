"""
 * cros project                                              https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import posixpath
import socketserver
import os
import urllib
from urllib.parse import unquote
from lib import HTTPHeaders, Out, Gzip, Passwd, crosinfo, Proxy
import base64
import cgi
import spdylay
from lib import IfNoneUseDefault as inud
from xml.sax.saxutils import escape
from lib.Reaper import *
import socket
from sdk import Hooks

class MixIn:
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

    server_version = "cros/" + crosinfo.Version

    def Log(self, key, msg, show=False, exit=False):
        path=""
        if hasattr(self, 'path'): path=self.path
        if self.ServerConfiguration.Logging['Enable']:
            Out.log(self.ServerConfiguration.Logging[key], self.client_address[0] + " | " + msg + " | " + path, show, exit)

    def CheckEverything(self, path):
        if self.client_address in self.ServerConfiguration.Access['bannedIPs']:
            self.ReturnError(403)
            return False
        accessnode = self.ServerConfiguration.Access
        if accessnode['Enable']:
            for bpath in accessnode['blockedPaths']:
                if path.startswith(bpath):
                    self.ReturnError(403, 'Access')
                    return False
            if os.path.splitext(path)[1] in accessnode['blockedExtensions']:
                self.ReturnError(403, 'Access')
                return False
        f = None
        if os.path.isfile(path):
            try:
                f = open(path, 'rb')
            except IOError:
                self.ReturnError(403, 'Access')
                return False
        else:
            self.ReturnError(404, 'Access')
            return False
        for arr in self.ServerConfiguration.Access['Authentication']:
            if arr['path'] == self.path:
                if 'IPs' in arr:
                    if self.client_address[0] in arr['IPs']: return f
                if 'Authorization' in self.headers:
                    auth = self.headers['Authorization'][6:]
                    if Passwd.Compare(auth, arr['passwd']): return f
                self.do_AUTHHEAD(arr)
                return False
        return f

    def do_GET(self):
        """Serve a GET request."""
        path = self.translate_path(self.path)
        f = self.CheckEverything(path)
        if f == False: return False
        Hooks.run("GET_always", [self])
        proxy = self.Proxy()
        if proxy == None:
            Hooks.run("GET_noproxy", [self])
            self.send_response(200)
            Hooks.run("GET_statuscode", [self])
            HTTPHeaders.send(self, path)
            Hooks.run("GET_headers", [self])
            self.SendFile(path)
            Hooks.run("GET_response", [self])

    def Send(self, data):
        enc = inud.get_d(self.headers, 'Accept-Encoding', '')
        dataa = data
        if self.ServerConfiguration.Gzip and 'gzip' in enc.lower(): dataa = Gzip.encode(data)
        self.wfile.write(dataa)
    def SendFile(self, fname):
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                self.Send(chunk)
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


    # Override built-in logging
    def log_request(self, code='-', size='-'):
        self.Log('Access', self.requestline)

    error_content_type = 'text/html; charset=UTF-8'

    # Same HTML from Apache error page
    error_message_format = '''\
<!doctype html>
<html>
<head>
  <title>{code} {reason}</title>
</head>
<body>
  <h1>{code} {reason}</h1>
  {explain}
  <footer>
    <hr/>
    <small>{server}:{port} ({hostname}) on {osname}</small>
  </footer>
</body>'''
    def send_error(self, code):
        # Make sure that code is really int
        code = int(code)
        try:
            shortmsg, longmsg = self.responses[code]
        except KeyError:
            shortmsg, longmsg = '???', '???'
        if message is None:
            message = shortmsg
        explain = longmsg

        content = self.error_message_format.format(\
            code=code,
            reason = escape(message),
            explain=escape(explain),
            server=escape(self.server_version),
            hostname=escape(socket.getfqdn()),
            port=self.server.server_address[1]).encode('UTF-8')

        self.send_response(code, message)
        HTTPHeaders.send(self, 'skip', extra={'Content-Type': self.error_content_type})
        self.wfile.write(content)

    def ReturnError(self, code, etype=False):
        self.Log(etype, "Returned " + str(code) + ".")
        self.send_error(code)

    def Proxy(self):
        if self.ServerConfiguration.Proxy != None:
            headers = {"X-Forwarded-By": self.version_string(), "Accept-Encoding": "gzip"}
            r, t = Proxy.Get(self.ServerConfiguration.Proxy + self.path, self.client_address, headers, dict(self.headers))
            self.send_response(r.status_code)
            HTTPHeaders.send(self, 'skip', r.headers)
            self.Send(t)
        return None

    def do_AUTHHEAD(self, arr):
        path = self.translate_path(self.path)
        if self.Authorize(path, True) != None or self.checkAccess(path, True) != None: self.send_response(401)
        authh = {"WWW-Authenticate": 'Basic'}
        if 'reason' in arr:
            authh = {"WWW-Authenticate": 'Basic realm=\"%r\"' % arr['reason']}
        HTTPHeaders.send(self, path, authh)

    def version_string(self):
        if self.ServerConfiguration.ServerHeader == True: return self.server_version
        else: return ""
