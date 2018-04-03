import socket
import sys
import time
import numpy as np
import utils

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.0.3', 6665)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

connection, client_address = sock.accept()

s = utils.State()
presses = []
utils.find_pattern(s, presses)

while True:
    data = connection.recv(16)
    data = data.decode().split()
    for x in data:
        presses.append(int(x))
        presses = utils.find_pattern(s, presses)

    time.sleep(0.01)
