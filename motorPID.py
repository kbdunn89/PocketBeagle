#!/usr/bin/python

'''
this file contains the functions used to read in the encoders
it also contains the function used to calculate the current 
motor RPM
'''
import Adafruit_BBIO.GPIO as GPIO
import time


inPin1 = "P1_20" #Left motor tachometer read
inPin2 = "P1_34" #Right motor tachometer read

#Left motor variables
prevTime1 = 0.0
slots1 = 0
rpm1 = 0
timeDiff1 = 0

#Right motor variables
prevTime2 = 0.0
slots2 = 0
rpm2 = 0
timeDiff2 = 0

#Left motor function
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
        if (slots1 == 1000):
            slots1 = 0
            timeDiff1 = 0

#Right motor function            
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
        if (slots2 == 1000):
            slots2 = 0
            timeDiff2 = 0
            

'''
This function is used to calculate the current motor RPMS'S
first all required variables are set to 0
then the function is slept for 0.1 sec. this allows the function
to be paused but the encoder functions still run. This allows
for the number of revolutions of the motors to be recorded,
this value is then used to calculate the rpm of the left and
right motors. rpm1(left motor), rpm2(right motor)
'''
def calculateRPM():
    global prevTime1
    global slots1
    global rpm1
    global timeDiff1
    global prevTime2
    global slots2
    global rpm2
    global timeDiff2
    
    prevTime1 = 0.0
    slots1 = 0
    rpm1 = 0
    timeDiff1 = 0
    prevTime2 = 0.0
    slots2 = 0
    rpm2 = 0
    timeDiff2 = 0
    
    time.sleep(0.1)

    if(slots1 > 0):
        rpm1 = 60/(360*timeDiff1/slots1)
    if(slots2 > 0):
        rpm2 = 60/(360*timeDiff2/slots2)
