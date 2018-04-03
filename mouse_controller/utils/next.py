#!/usr/bin/env python

import time
import os
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

adc1 = 0;
adc2 = 1;
adc3 = 2;

########
from Tkinter import *

root = Tk()

def drawcircle(canv,x,y,rad):
    return canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='blue')

def movecircle(canv, cir):
    x = readadc(adc1, SPICLK, SPIMOSI, SPIMISO, SPICS)
    y = readadc(adc2, SPICLK, SPIMOSI, SPIMISO, SPICS)

    tup = canv.coords(cir)
    dx = tup[2]-tup[0]
    dy = tup[3]-tup[1]
    
    canv.coords(cir, x-(dx/2.), y-(dy/2.), x+(dx/2.), y+(dy/2.))

def callback(event=None):
    movecircle(canvas, circ1)
    movecircle(canvas, circ2)
    root.after(10, callback)
    
canvas = Canvas(width=600, height=600, bg='white')
canvas.pack()

circ1=drawcircle(canvas,100,100,20)          

root.after(0, callback)
root.mainloop()
