"""
 * cros project                                              https://wolflinux.org/s/4jRm3
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://wolflinux.org/s/mmdoe
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import yaml
from lib import IfNoneUseDefault as inud

class Configuration:
    # Init predefined variables
    RunAs = ConnectionLimit = MainLog = None
    Servers = []

    # Load
    def __init__(self, path):
        file = open(path)
        runfile = yaml.load(file.read())
        self.RunAs = inud.get_d(runfile, 'RunAs', 'http')
        self.ConnectionLimit = inud.get_d(runfile, 'ConnectionLimit', {'PerIP': 200, 'In': 60})
        self.MainLog = inud.get_d(runfile, "MainLog", "/var/log/httpjs/main.log")

        # Put servers configurations into array
        for key, value in runfile['Servers'].items(): self.Servers.append(Server(value))

class Server:
    # Init predefined variables
    Address = Port = Directory = Listing = IndexFiles = Errors = SPDY = SSL = Logging = Gzip = Access = Headers = CGI = XPoweredBy = None

    # Load
    def __init__(self, srvyaml):
        self.Address = inud.get_d(srvyaml, 'Address', None)
        self.Port = int(inud.get_d(srvyaml, 'Port', None))
        self.Directory = inud.get_d(srvyaml, 'Directory', None)
        self.Listing = inud.get_d(srvyaml, 'Listing', False)
        self.IndexFiles = inud.get_d(srvyaml, 'IndexFiles', ["index.html"])
        self.Errors = inud.get_d(srvyaml, "Errors", {
            '404': '/usr/share/httpjs/errors/404.html',
            '403': '/usr/share/httpjs/errors/403.html',
            '500': '/usr/share/httpjs/errors/500.html'
        })
        self.SPDY = inud.get_d(srvyaml, 'SPDY', {
            'Enable': None,
            'Protocols': ['h2','spdy/3.1','http/1.1']
        })
        self.SSL = inud.get_d(srvyaml, 'SSL', {
            'Enable': False,
            'PrivateKey': None,
            'Certificate': None,
            'CA': None,
            'Ciphers': 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-SHA:ECDHE-RSA-RC4-SHA',
            'LetsEncrypt': {
                'Enable': True,
                'Server': 'https://acme-v01.api.letsencrypt.org/directory'
            }
        })
        self.Logging = inud.get_d(srvyaml, 'Logging', {
            'Enable': True,
            'Access': '/var/log/httpjs/access.log',
            'Error': '/var/log/httpjs/error.log',
            'Info': '/var/log/httpjs/info.log',
            'Warn': '/var/log/httpjs/warn.log',
            'Unknown': '/var/log/httpjs/unknown.log'
        })
        self.CGI = inud.get_d(srvyaml, 'CGI', {
            'Enable': False,
            'Directories': ['/cgi-bin']
        })
        self.Gzip = inud.get_d(srvyaml, 'Gzip', True)
        self.Access = inud.get_d(srvyaml, 'Access', {
            'Enable': False,
            'blockedExtensions': [],
            'blockedPaths': []
        })
        self.Headers = inud.get_d(srvyaml, 'Headers', {})
        self.XPoweredBy = inud.get_d(srvyaml, 'XPoweredBy', False)
