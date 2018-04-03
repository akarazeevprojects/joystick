import time
import os
import random
import socket
import sys

from evdev import InputDevice, categorize, ecodes

# Create a TCP/IP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening.
server_address = ('192.168.0.3', 6665)

print('connecting to %s port %s' % server_address)
sock.connect(server_address)

dev = InputDevice('/dev/input/event0')
for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:

            msg = "{}".format(event.code).ljust(4).encode()
            print(msg)
            sock.send(msg)

            time.sleep(0.01)
