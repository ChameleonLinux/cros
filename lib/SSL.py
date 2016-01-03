import ssl
def new_socket(sock, crt, key, ca, ciphers):
    return ssl.wrap_socket(sock, certfile=crt, keyfile=key, ciphers=ciphers, server_side=True)
