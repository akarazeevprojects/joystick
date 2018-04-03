import time
import os
import random
import socket
import sys

# Create a TCP/IP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening.
server_address = ('192.168.0.3', 6666)
print('connecting to %s port %s' % server_address)

sock.connect(server_address)

while True:
    keypressed = 82

    msg = "{}".format(keypressed).ljust(4).encode()
    print(msg)
    sock.send(msg)

    time.sleep(0.1)
