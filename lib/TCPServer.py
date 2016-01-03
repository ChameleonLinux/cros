"""
 * cros project                                              https://wolflinux.org/s/4jRm3
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://wolflinux.org/s/mmdoe
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import socketserver

class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    """
      This server provides variable for server configuration object. Nothing more.
    """

    ServerConfiguration = None

    def __init__(self, conf, server_address, RequestHandlerClass, bind_and_activate=True):
        self.ServerConfiguration = conf
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)

    def finish_request(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass."""
        self.RequestHandlerClass(request, client_address, self.ServerConfiguration, self)
