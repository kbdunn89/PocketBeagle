#!/usr/bin/python

'''
working versions of the encoder functions
'''

import Adafruit_BBIO.GPIO as GPIO
import time


inPin1 = "P1_20" #Forward motor
inPin2 = "P1_34" #Back motor

#Forward motor variables
prevTime1 = 0.0
slots1 = 0
rpm1 = 0
timeDiff1 = 0

#Back motor variables
prevTime2 = 0.0
slots2 = 0
rpm2 = 0
timeDiff2 = 0

#Forward motor function
def risingEdge1(arg):
    global prevTime1
    global timeDiff1
    global slots1
    global rpm1
    if (prevTime1 == 0.0):
        prevTime1 = time.time()
    else:
        timeDiff1 = timeDiff1 + (time.time() - prevTime1)
        prevTime1 = time.time()
        slots1 = slots1 + 1
        if (slots1 == 360):
            rpm1 = 60/timeDiff1
            slots1 = 0
            timeDiff1 = 0
            print("Forward: " + str(rpm1))

#Back motor function            
def risingEdge2(arg):
    global prevTime2
    global timeDiff2
    global slots2
    global rpm2
    if (prevTime2 == 0.0):
        prevTime2 = time.time()
    else:
        timeDiff2 = timeDiff2 + (time.time() - prevTime2)
        prevTime2 = time.time()
        slots2 = slots2 + 1
        if (slots2 == 360):
            rpm2 = 60/timeDiff2
            slots2 = 0
            timeDiff2 = 0
            print("Back: " + str(rpm2))
