import ssl
DefaultCiphers='ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-SHA:ECDHE-RSA-RC4-SHA'
def new_socket(sock, crt, key, ca, ciphers):
    return ssl.wrap_socket(sock, certfile=crt, keyfile=key, ciphers=ciphers, server_side=True)
