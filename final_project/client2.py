from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import DH
import socket

HOST = 'localhost'
PORT = 5000


def receive_key(sock):
    # Receive public key from client 1
    public_key = sock.recv(1024)

    # Load received public key
    key = DH.construct((int(public_key), 2))

    # Generate shared secret key
    shared_secret = key.generate_shared_secret()

    # Send public key to client 1
    sock.sendall(str(key.public_key().y).encode())

    return shared_secret


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        # Receive public key from client 1
        shared_secret = receive_key(conn)

print("Shared secret key: ", shared_secret.hex())
