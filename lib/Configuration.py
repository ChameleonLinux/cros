"""
 * cros project                                              https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import yaml
from lib import IfNoneUseDefault as inud

class Configuration:
    # Init predefined variables
    MainLog = Plugins = None
    Servers = []

    # Load
    def __init__(self, path):
        file = open(path)
        runfile = yaml.load(file.read())
        self.MainLog = inud.get_d(runfile, "MainLog", "/var/log/httpjs/main.log")
        self.Plugins = inud.get_d(runfile, "Plugins", [])

        # Put servers configurations into array
        for key, value in runfile['Servers'].items(): self.Servers.append(Server(value))

class Server:
    # Init predefined variables
    Address = Port = Directory = Listing = IndexFiles = Errors = SPDY = SSL = Logging = Gzip = Access = Headers = CGI = ServerHeader = Proxy = None

    # Load
    def load(self, srvyaml):
        self.Address = inud.get_d(srvyaml, 'Address', None)
        self.Port = int(inud.get_d(srvyaml, 'Port', None))
        self.Directory = inud.get_d(srvyaml, 'Directory', None)
        self.Listing = inud.get_d(srvyaml, 'Listing', False)
        self.IndexFiles = inud.get_d(srvyaml, 'IndexFiles', ["index.html"])
        self.Proxy = inud.get_d(srvyaml, 'Proxy', None)
        self.Errors = inud.get_d(srvyaml, "Errors", {
            'e404': '/usr/share/httpjs/errors/404.html',
            'e403': '/usr/share/httpjs/errors/403.html',
            'e500': '/usr/share/httpjs/errors/500.html'
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
        if self.SPDY['Enable'] == None:
            if self.SSL['Enable'] == True: self.SPDY['Enable'] = True
            else: self.SPDY['Enable'] = False
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
            'blockedPaths': [],
            'bannedIPs': [],
            'Authentication': []
        })
        self.Headers = inud.get_d(srvyaml, 'Headers', {})
        self.ServerHeader = inud.get_d(srvyaml, 'Server-Header', False)

    def __init__(self, srvyaml):
        dict_ = srvyaml
        for f in inud.get_d(srvyaml, 'Includes', []):
            dict_.update(yaml.load(open(f,"r").read()))
        self.load(dict_)
