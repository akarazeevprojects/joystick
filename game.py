#!/usr/bin/env python

import time
import os
import random

from Tkinter import *
import tkFont
from PIL import Image, ImageTk

root = Tk()

def drawcircle(canv,x,y,rad):
    return canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='blue')

cols = ['red','yellow','black','green','white','pink','blue']

is_pressed = False
it = 0

def movecircle(canv, cir):
    global is_pressed
    global it

    data = connection.recv(32)
    data = data.split()
    if len(data) >= 2:
        x = data[0]
        y = data[1]
    else:
        x = 300
        y = 300
    print data

    # if inp == False:
    #     if not is_pressed:
    #         canv.config(bg=cols[it % len(cols)])
    #         it += 1
    #         is_pressed = True
    # else:
    #     is_pressed = False

    canv.coords(cir,x,y)

def callback(event=None):
    movecircle(canvas, a1)
    root.after(100, callback)
    

#--------->-------->-------->
import socket, sys

#Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.0.100', 6666)
print 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

connection, client_address = sock.accept()
#--------->-------->-------->

canvas = Canvas(width=600, height=600, bg='white')
canvas.pack()

img = PhotoImage(file="pepa.gif")
img = img.subsample(5, 5)
a1 = canvas.create_image(100,100,image=img)

root.after(0, callback)
root.mainloop()
