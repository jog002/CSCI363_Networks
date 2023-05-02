from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import DH
import socket

HOST = 'localhost'
PORT = 5000


def receive_key(sock):
    # Receive public key from server
    public_key = sock.recv(1024)

    # Load received public key
    key = DH.construct((int(public_key), 2))

    # Generate shared secret key
    shared_secret = key.generate_shared_secret()

    return shared_secret


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # Generate private and public key
    key = DH.generate(2048)
    # Send public key to server
    s.sendall(str(key.public_key().y).encode())
    # Receive public key from server
    shared_secret = receive_key(s)

print("Shared secret key: ", shared_secret.hex())
