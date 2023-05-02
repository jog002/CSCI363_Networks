import socket
from pyDH import DiffieHellman

# Step 1: Both parties agree on a common modulus p and base g

p = 2017
g = 2

# Step 2: Bob generates a private key

bob_key = DiffieHellman()

# Step 3: Bob listens for Alice's connection and sends his public key

bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bob_socket.bind(('localhost', 12345))
bob_socket.listen()

alice_conn, address = bob_socket.accept()
bob_public_key = bob_key.gen_public_key()
alice_conn.send(bob_public_key.to_bytes(2048, 'big'))

# Step 4: Bob receives Alice's public key and computes the shared secret key

alice_public_key_bytes = alice_conn.recv(2048)
alice_public_key = int.from_bytes(alice_public_key_bytes, 'big')

bob_shared_secret = bob_key.gen_shared_key(alice_public_key)

# Step 5: Bob receives the shared secret key from Alice

alice_shared_secret_bytes = alice_conn.recv(2048)
alice_shared_secret = int.from_bytes(alice_shared_secret_bytes, 'big')
alice_conn.close()

print("Shared secret key: ", bob_shared_secret)