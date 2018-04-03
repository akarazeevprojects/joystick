"""
File name: server.py
Author: Anton Karazeev <anton.karazeev@gmail.com>

This file is part of joystick project (https://github.com/akarazeevprojects/joystick)
"""

import time
import os
import random
import socket
import sys


def movecircle():
    data = connection.recv(32)
    data = data.split()
    print(data)


# Create a TCP/IP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port.
server_address = ('192.168.0.3', 6666)
print('starting up on %s port %s' % server_address)

sock.bind(server_address)
# Listen for incoming connections.
sock.listen(1)

connection, client_address = sock.accept()

while True:
    movecircle()
    time.sleep(0.1)
