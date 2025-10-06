import socket
import ssl
import certifi

HOST = 'ac-akpxg6y-shard-00-00.reorq1w.mongodb.net'
PORT = 27017

context = ssl.create_default_context(cafile=certifi.where())
# context.check_hostname = True  # default True
# context.verify_mode = ssl.CERT_REQUIRED

print('Using Python SSL:', ssl.OPENSSL_VERSION)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)

try:
    wrapped = context.wrap_socket(s, server_hostname=HOST)
    print(f'Connecting to {HOST}:{PORT}...')
    wrapped.connect((HOST, PORT))
    print('Handshake succeeded')
    print('Protocol:', wrapped.version())
    print('Cipher:', wrapped.cipher())
    peercert = wrapped.getpeercert()
    print('Peer cert subject:', peercert.get('subject'))
    wrapped.close()
except Exception as e:
    import traceback
    traceback.print_exc()
    print('Exception:', type(e).__name__, e)
finally:
    try:
        s.close()
    except:
        pass
