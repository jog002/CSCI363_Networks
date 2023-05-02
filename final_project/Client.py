"""
Diffie-Hellman Key Exchange
CSCI 363 Networks
BY: Christiaan Smith, Jackie Quinlavin, and Oscar Giller

This client script should be run after the companion server script. It initiates
a connection with the server and then performs the Diffie-Hellman Key Exchange
to establish a shared key between the client and server without allowing
any potential interception of privet information.
"""
import socket
from pyDH import DiffieHellman


p = 2017
g = 2


client_dh_key = DiffieHellman()

# Make the connection to the Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
print("Connection to Server established")

# Generate and send the public key
client_public_key = client_dh_key.gen_public_key()
print("Initial client public key: ", str(client_public_key))
client_socket.send(client_public_key.to_bytes(2048, 'big'))

# Receive the servers public key and generate the shared secret
server_public_key_bytes = client_socket.recv(2048)
server_public_key = int.from_bytes(server_public_key_bytes, 'big')

client_shared_secret = client_dh_key.gen_shared_key(server_public_key)

# Send the shared secret to the server
client_socket.send(int(client_shared_secret, 16).to_bytes(2048, 'big'))
client_socket.close()

print("Shared secret key: ", client_shared_secret)