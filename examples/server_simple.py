import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.0.3', 6665)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

connection, client_address = sock.accept()

while True:
    data = connection.recv(16)
    data = data.decode().split()
    for x in data:
        print('received {} w {}'.format(int(x), len(data)))
