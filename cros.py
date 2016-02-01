#!/usr/bin/env python
"""
 * cros project                                              https://github.com/ProjectCros/cros
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://github.com/Py64
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""

from sdk import Hooks
import sys
import imp
if sys.version_info <= (3,0):
    print("[err] cros has been written only for Python 3 and tested on Python 3.5.1.")
    sys.exit(4)
import re, os
try:
    import spdylay
except Exception:
    print("[err] Could not load spdylay.")
    sys.exit(130)
try:
    from lib import IfNoneUseDefault as inud
    from lib import Configuration, Arguments, Out, Gzip, RequestHandlers, Servers, SSL, crosinfo
except Exception as e:
    print("[err] Corrupted cros installation!")
    print(e)
    sys.exit(400)
import threading

# Load configuration
configpath = inud.get(Arguments.get(re.compile("--config|-c")), "RunFile", True)
config = Configuration.Configuration(configpath)
servers = config.Servers

# Register all hooks
hooklist = ["REQUEST", "REQUEST_statuscode", "REQUEST_headers", "REQUEST_response",
            "headers_pathknown", "headers", "REQUEST_exists"]
for hookname in hooklist:
    Hooks.hook(hookname)

# Import plugins
#try:
for plg in config.Plugins:
    imp.load_source(plg, "plugins/" + plg + ".cros-extension")
#except Exception as e:
#    print("[err] Plugin error: " + str(e))

# Show message with version.
crosinfo.Show(config)

# Check for root.
try:
    if os.geteuid() == 0 and crosinfo.Insecure == False:
        Out.log(config.MainLog, " [err] cros cannot be executed by root for security reasons.", True, True)
except AttributeError: None

# Trigger start hook
Hooks.run("startup", {'Configuration': config})

# Start servers. Get ports & addresses. Listen to them.
httpservers = []
threads = []
try:
    for server in servers:
        httpserver = None
        if server.SPDY['Enable']:
            httpserver = Servers.ThreadedSPDYServer((server.Address, server.Port),
                                                    RequestHandlers.SPDY,
                                                    server,
                                                    cert_file=server.SSL['Certificate'],
                                                    key_file=server.SSL['PrivateKey'])
        else:
            httpserver = Servers.ThreadedTCPServer(server, (server.Address, server.Port), RequestHandlers.HTTP)
            if server.SSL['Enable']:
                httpserver.socket = SSL.new_socket(httpserver.socket, crt=server.SSL['Certificate'], key=server.SSL['PrivateKey'],
                                                        ca=inud.get_d(server.SSL, 'CA', None), ciphers=inud.get_d(server.SSL, 'Ciphers', SSL.DefaultCiphers))
        httpservers.append(httpserver)
        Out.log(config.MainLog, " [inf] Serving " + server.Address + " on port " + str(server.Port) + ".", True)
        httpserver.start()
        Hooks.run("servers-init", {'Configuration': config})
except KeyboardInterrupt:
    print("Interrupted by keyboard.")
    for srv in servers: srv.stop()
