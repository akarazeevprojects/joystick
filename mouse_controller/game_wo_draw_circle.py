"""
File name: game_wo_draw_circle.py
Author: Anton Karazeev <anton.karazeev@gmail.com>

This file is part of joystick project (https://github.com/akarazeevprojects/joystick)
"""

import time
import os
import random
import autopy

from Tkinter import *
import tkFont
from PIL import Image, ImageTk

root = Tk()

def sign(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1

def func(x):
    return sign(x) * 4 * (abs(x) ** .5)

cols = ['red','yellow','black','green','white','pink','blue']

is_pressed = False
it = 0
old_vx = 0
old_vy = 0
old_x = 0
old_y = 0
acc = 3

def movecircle(canv, cir):
    global is_pressed
    global it
    global old_vx
    global old_vy
    global old_x
    global old_y
    global acc

    data = connection.recv(16)
    # x, y, change, press = data.split()
    x, y, press = data.split()

    x = int(x)
    y = int(y)
    press = int(press)

    if press == 1:
        if not is_pressed:
            autopy.mouse.toggle(True)
            is_pressed = True
    else:
        if is_pressed:
            autopy.mouse.toggle(False)
            is_pressed = False

    vx = func((x-514)/100.)
    vy = func((y-536)/100.)

    ## Accuracy
    # if abs(vx - old_vx) <= acc:
    #     vx = 0
    # else:
    #     old_vx = vx

    # if abs(vy - old_vy) <= acc:
    #     vy = 0
    # else:
    #     old_vy = vy

    canv.move(cir, -vx, -vy)

    # if change == '1':
    #     canv.config(bg=cols[it % len(cols)])
    #     it += 1

    p = autopy.mouse.get_pos()
    tx = 1279 - int((x * 1279.)/1023.)
    ty = 799 - int((y * 799.)/1023.)

    tx *= 880./1279.
    ty *= 400./799.

    tx += 200.
    ty += 200.
    # tx = p[0] - int((x-514)/50.)
    # ty = p[1] - int((y-536)/50.)

    # Accuracy
    # if abs(tx - old_x) <= acc:
    #     tx = old_x
    # else:
    #     old_x = tx

    # if abs(ty - old_y) <= acc:
    #     ty = old_y
    # else:
    #     old_y = ty

    print(tx, ty, '_', x, y, '_', press)
    autopy.mouse.move(int(tx), int(ty))

    # print(p)
    # (1280, 800)

    # canv.coords(cir,x,y)

def callback(event=None):
    movecircle(canvas, a1)
    root.after(1, callback)

#--------->-------->-------->
import socket, sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.0.101', 6661)
# server_address = ('192.168.1.6', 6661)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

sock.listen(1)

connection, client_address = sock.accept()
#--------->-------->-------->

canvas = Canvas(width=600, height=600, bg='white')
canvas.pack()

img = PhotoImage(file="img/pepa.gif")
img = img.subsample(5, 5)
a1 = canvas.create_image(100,100,image=img)

root.after(0, callback)
root.mainloop()
