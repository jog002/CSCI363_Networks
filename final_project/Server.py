"""
Diffie-Hellman Key Exchange
CSCI 363 Networks
BY: Christiaan Smith, Jackie Quinlavin, and Oscar Giller

This server script should be run before the companion client script. It receives
a connection from the client and then performs the Diffie-Hellman Key Exchange
to establish a shared key between the client and server without allowing
any potential interception of privet information.
"""
import socket
from pyDH import DiffieHellman

p = 2017
g = 2

server_dh_key = DiffieHellman()

# listen for the connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen()

# create the connection and send the public key
client_conn, address = server_socket.accept()
print("Connection to Client established")
server_public_key = server_dh_key.gen_public_key()
print("Initial server public key: ", hex(server_public_key))
client_conn.send(server_public_key.to_bytes(2048, 'big'))

# receive the client's public key and generate the shared key
client_public_key_bytes = client_conn.recv(2048)
client_public_key = int.from_bytes(client_public_key_bytes, 'big')
print("Received Client public key: ", hex(client_public_key))

server_shared_secret = server_dh_key.gen_shared_key(client_public_key)

# receive the shared key
client_shared_secret_bytes = client_conn.recv(2048)
client_shared_secret = hex(int.from_bytes(client_shared_secret_bytes, 'big'))
client_conn.close()
print("Server's shared secret key: ", server_shared_secret)
print("Client's shared secret key: ", str(client_shared_secret)[2:])
if server_shared_secret == str(client_shared_secret)[2:]:
    print("SUCCESS: the shared secret keys are identical\n\n")
else:
    print("FAILURE: the shared secret keys are not identical\n\n")

server_socket.close()