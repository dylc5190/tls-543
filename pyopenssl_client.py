from OpenSSL import SSL
import sys, os, select, socket

def verify_cb(conn, cert, errnum, depth, ok):
    # This obviously has to be updated
    print 'Got certificate: %s' % cert.get_subject()
    return ok

if len(sys.argv) < 3:
    print 'Usage: python {0} HOST PORT'.format(sys.argv[0])
    sys.exit(1)

dir = os.path.dirname(sys.argv[0])
if dir == '':
    dir = os.curdir

# Initialize context
ctx = SSL.Context(SSL.SSLv23_METHOD)
ciphers = "DES-CBC3-SHA" 
ctx.set_cipher_list(ciphers)
#ctx.set_verify(SSL.VERIFY_PEER, verify_cb) # Demand a certificate
#ctx.use_privatekey_file (os.path.join(dir, 'client.pkey'))
#ctx.use_certificate_file(os.path.join(dir, 'client.cert'))
#ctx.load_verify_locations(os.path.join(dir, 'CA.cert'))

# Set up client
sock = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
sock.connect((sys.argv[1], int(sys.argv[2])))

line = "GET / HTTP/1.0\n\n"
try:
    sock.send(line)
    sys.stdout.write(sock.recv(1024))
    sys.stdout.flush()
except SSL.Error:
    print 'Connection died unexpectedly'

# followings are not available in Python ssl module
# you can use client_random and master_key to compose (Pre)-Master-Secret log file for Wireshark just like browser's $SSLKEYLOGFILE
print sock.client_random().encode('hex')
print sock.server_random().encode('hex')
print sock.master_key().encode('hex')

sock.shutdown()
sock.close()