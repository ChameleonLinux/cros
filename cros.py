"""
 * cros project                                              https://wolflinux.org/s/4jRm3
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://wolflinux.org/s/mmdoe
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import re, os
from lib import IfNoneUseDefault as inud
from lib import Configuration, Arguments, Out, crosinfo, Gzip, HTTPRequestHandler, TCPServer, SSL
import threading

# Load configuration
configpath = inud.get(Arguments.getArgument(re.compile("--config|-c")), "RunFile", True)
config = Configuration.Configuration(configpath)
servers = config.Servers

# Show message with version.
Out.log(config.MainLog, "cros " + crosinfo.Version, True)

# Check for root.
try:
    if os.geteuid() == 0 and config.RunAs != "root":
        Out.log(config.MainLog, " [err] cros cannot be executed by root for security reasons.", True, True)
except AttributeError: None

# Start servers. Get ports & addresses. Listen to them.
httpservers = []
threads = []
for server in servers:
    httpservers.append(TCPServer.TCPServer(server, (server.Address, server.Port), HTTPRequestHandler.HTTPRequestHandler))
    if server.SSL['Enable']:
        httpservers[-1].socket = SSL.new_socket(httpservers[-1].socket, crt=server.SSL['Certificate'], key=server.SSL['PrivateKey'],
                                                ca=inud.get_d(server.SSL, 'CA', None), ciphers=inud.get_d(server.SSL, 'Ciphers', 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-SHA:ECDHE-RSA-RC4-SHA'))
    Out.log(config.MainLog, " [inf] Serving " + server.Directory + " at " + server.Address + " on port " + str(server.Port) + ".", True)
    server_thread = threading.Thread(target=httpservers[-1].serve_forever())
    server_thread.daemon = True
    server_thread.start()
    threads.append(server_thread)

# ... not implemented yet.
