"""
 * cros project                                              https://wolflinux.org/s/4jRm3
 * (c) 2016 Py64 <py64.wolflinux@gmail.com>                  https://wolflinux.org/s/mmdoe
 *
 * This software is distributed on CPL license.
 * https://github.com/ProjectCros/CPL
"""
import socketserver
import spdylay
import ssl
import threading

class ServerStart:
    server_thread = None
    def start(self, daemon=False):
        self.server_thread = threading.Thread(target=self.serve_forever)
        self.server_thread.daemon = daemon
        self.server_thread.start()
    def stop(self):
        if type(self.server_thread) != None: self.server_thread.stop()

class ThreadedTCPServer(ServerStart, socketserver.ThreadingMixIn, socketserver.TCPServer):

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

class ThreadedSPDYServer(ServerStart, spdylay.ThreadedSPDYServer):

    ServerConfiguration = None

    def __init__(self, server_address, RequestHandlerCalss, srvconf,
                 cert_file, key_file):
        self.ServerConfiguration = srvconf
        spdylay.ThreadedSPDYServer.__init__(self, server_address, RequestHandlerCalss, cert_file, key_file)

    def process_request(self, request, client_address):
        # ThreadingMixIn.process_request() dispatches request and
        # client_address to separate thread. To cleanly shutdown
        # SSL/TLS wrapped socket, we wrap socket here.

        # SSL/TLS handshake is postponed to each thread.
        request = self.ctx.wrap_socket(\
            request, server_side=True, do_handshake_on_connect=False)

        socketserver.ThreadingMixIn.process_request(self,
                                                    request, client_address)

    def finish_request(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass."""
        self.RequestHandlerClass(request, client_address, self.ServerConfiguration, self)
