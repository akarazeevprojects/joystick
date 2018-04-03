#!/usr/bin/env python

import time
import os
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

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

    for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                    adcout |= 0x1

    GPIO.output(cspin, True)
    
    adcout >>= 1
    return adcout

SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

led = 11
GPIO.setup(led, GPIO.OUT)

while True:
    x = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
    if x:
        GPIO.output(led, 1)
    else:
        GPIO.output(led, 0)
    print(x)
    time.sleep(0.1)
