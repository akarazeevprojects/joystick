#!/usr/bin/env python

import time
import os
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)

    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
            if (commandout & 0x80):
                    GPIO.output(mosipin, True)
            else:
                    GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                    adcout |= 0x1

    GPIO.output(cspin, True)
    
    adcout >>= 1       # first bit is 'null' so drop it
    return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# button = 11
# GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)

led = 11
GPIO.setup(led, GPIO.OUT)

adc1 = 0;
adc2 = 1;
adc3 = 2;

cols = ['red','yellow','black','green','white','pink','blue']

is_pressed = False
change = False
it = 0

#--------->-------->-------->
import socket, sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.0.101', 6661)
# server_address = ('192.168.1.6', 6661)
print'connecting to %s port %s' % server_address
sock.connect(server_address)

while True:
    x = readadc(adc1, SPICLK, SPIMOSI, SPIMISO, SPICS)
    y = readadc(adc2, SPICLK, SPIMOSI, SPIMISO, SPICS)

    is_wet = readadc(adc3, SPICLK, SPIMOSI, SPIMISO, SPICS)
    if is_wet:
        GPIO.output(led, 1)
        is_wet = 1
    else:
        GPIO.output(led, 0)

    ## Not for .move, only for .coords
    #x *= 600./1023.
    #y *= 600./1023.
    #x = 600 - x   
    #y = 600 - y

    # inp = GPIO.input(button)
    # if inp == False:
    if is_wet == False:
        if not is_pressed:
            # canv.config(bg=cols[it % len(cols)])
            change = True
            it += 1
            is_pressed = True
    else:
        is_pressed = False
    
    # msg = ("{} {} {}".format(int(x)in, t(y), int(change))).ljust(16)
    msg = ("{} {} {}".format(x, y, is_wet)).ljust(16)

    change = False
    print msg.split()
    sock.send(msg)

    time.sleep(0.1)


#  _.........._
# | |  peppa | |
# | |  the   | |
# | |__pig___| |
# |   ______   |
# |  |    | |  |
# |__|____|_|__|
#


# #!/usr/bin/env python

# import time
# import os
# import random
# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)

# # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
# def readadc(adcnum, clockpin, mosipin, misopin, cspin):
#     if ((adcnum > 7) or (adcnum < 0)):
#         return -1
#     GPIO.output(cspin, True)

#     GPIO.output(clockpin, False)  # start clock low
#     GPIO.output(cspin, False)     # bring CS low

#     commandout = adcnum
#     commandout |= 0x18  # start bit + single-ended bit
#     commandout <<= 3    # we only need to send 5 bits here
#     for i in range(5):
#             if (commandout & 0x80):
#                     GPIO.output(mosipin, True)
#             else:
#                     GPIO.output(mosipin, False)
#             commandout <<= 1
#             GPIO.output(clockpin, True)
#             GPIO.output(clockpin, False)

#     adcout = 0
#     # read in one empty bit, one null bit and 10 ADC bits
#     for i in range(12):
#             GPIO.output(clockpin, True)
#             GPIO.output(clockpin, False)
#             adcout <<= 1
#             if (GPIO.input(misopin)):
#                     adcout |= 0x1

#     GPIO.output(cspin, True)
    
#     adcout >>= 1       # first bit is 'null' so drop it
#     return adcout

# # change these as desired - they're the pins connected from the
# # SPI port on the ADC to the Cobbler
# SPICLK = 18
# SPIMISO = 23
# SPIMOSI = 24
# SPICS = 25

# # set up the SPI interface pins
# GPIO.setup(SPIMOSI, GPIO.OUT)
# GPIO.setup(SPIMISO, GPIO.IN)
# GPIO.setup(SPICLK, GPIO.OUT)
# GPIO.setup(SPICS, GPIO.OUT)

# button = 11
# GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)

# adc1 = 0;
# adc2 = 1;
# adc3 = 2;

# ########
# from Tkinter import *
# import tkFont
# from PIL import Image, ImageTk

# root = Tk()

# def drawcircle(canv,x,y,rad):
#     return canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='blue')

# def sign(x):
#     if x > 0:
#         return 1
#     elif x == 0:
#         return 0
#     else:
#         return -1

# def func(x):
#     return sign(x) * 4 * (abs(x) ** .5)

# cols = ['red','yellow','black','green','white','pink','blue']

# is_pressed = False
# it = 0

# def movecircle(canv, cir):
#     # x = readadc(adc1, SPICLK, SPIMOSI, SPIMISO, SPICS)
#     # y = readadc(adc2, SPICLK, SPIMOSI, SPIMISO, SPICS)
#     # vx = func((x-514)/400.)
#     # vy = func((y-536)/400.)
#     # canv.move(cir, -vx, -vy)
#     global is_pressed
#     global it

#     x = readadc(adc1, SPICLK, SPIMOSI, SPIMISO, SPICS)
#     y = readadc(adc2, SPICLK, SPIMOSI, SPIMISO, SPICS)
#     # print x, y
#     vx = func((x-514)/400.)
#     vy = func((y-536)/400.)
#     # print(vx, vy)
#     canv.move(cir, -vx, -vy)
#     # x *= 600./1023.
#     # y *= 600./1023.

#     # x = 600 - x   
#     # y = 600 - y

#     inp = GPIO.input(button)
#     if inp == False:
#         if not is_pressed:
#             canv.config(bg=cols[it % len(cols)])
#             it += 1
#             is_pressed = True
#     else:
#         is_pressed = False
#     # #--------->-------->-------->
#     # msg = "{} {} {} {}".format(int(x), int(y), inp, int(is_pressed))
#     # print msg.split()
#     # sock.send(msg)
#     #--------->-------->-------->

#     # canv.coords(cir,x,y)

#     #--------->-------->-------->

# def callback(event=None):
#     movecircle(canvas, a1)
#     root.after(10, callback)
    

# # #--------->-------->-------->
# # import socket, sys

# # # Create a TCP/IP socket
# # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # # Connect the socket to the port where the server is listening
# # server_address = ('192.168.0.100', 6666)
# # print'connecting to %s port %s' % server_address
# # sock.connect(server_address)
# # #--------->-------->-------->

# canvas = Canvas(width=600, height=600, bg='white')
# canvas.pack()

# img = PhotoImage(file="pepa.gif")
# img = img.subsample(5, 5)
# a1 = canvas.create_image(300,300,image=img)

# root.after(0, callback)
# root.mainloop()
