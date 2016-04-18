'''based on http://carlo-hamalainen.net/blog/2013/1/24/python-ssl-socket-echo-test-with-self-signed-certificate'''
import socket, ssl, pprint
import re

#cert_path="C:\\ca-certificates.crt"

host = 'Ebay.com'
ciphers = "kRSA, aRSA, RSA"	# for RSA
ciphers = "kDHE, kEDH, DH"	# for Diffie-Hellman
# DH ciphers work on openssl
#   e.g. openssl s_client -connect ebay.com:443 -cipher "kDHE, kEDH, DH" -tls1
# but not in my office desktop, why?
# try it in lab, works too. could it be caused by company proxy?

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Require a certificate from the server. We used a self-signed certificate
# so here ca_certs must be the server certificate itself.
ssl_sock = ssl.wrap_socket(s,
                           ciphers=ciphers,
                           #ca_certs=cert_path,                           
                           cert_reqs=ssl.CERT_NONE)

ssl_sock.settimeout(5)
try:
               ssl_sock.connect((host, 443))
               print repr(ssl_sock.getpeername())
               print ssl_sock.cipher()
               #print pprint.pformat(ssl_sock.getpeercert())
            
               ssl_sock.write("GET / HTTP/1.0\n\n")
               ssl_sock.read()
except socket.error as msg:
               print msg            

# note that closing the SSLSocket will also close the underlying socket
ssl_sock.shutdown(socket.SHUT_RDWR)
ssl_sock.close()
