import socket
from pyDH import DiffieHellman

# Step 1: Both parties agree on a common modulus p and base g

p = 2017
g = 2

# Step 2: Alice generates a private key

alice_key = DiffieHellman()

# Step 3: Alice connects to Bob and sends her public key

alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice_socket.connect(('localhost', 12345))

alice_public_key = alice_key.gen_public_key()
alice_socket.send(alice_public_key.to_bytes(2048, 'big'))

# Step 4: Alice receives Bob's public key and computes the shared secret key

bob_public_key_bytes = alice_socket.recv(2048)
bob_public_key = int.from_bytes(bob_public_key_bytes, 'big')

alice_shared_secret = alice_key.gen_shared_key(bob_public_key)

# Step 5: Alice sends the shared secret key to Bob

alice_socket.send(int(alice_shared_secret, 16).to_bytes(2048, 'big'))
alice_socket.close()

print("Shared secret key: ", alice_shared_secret)