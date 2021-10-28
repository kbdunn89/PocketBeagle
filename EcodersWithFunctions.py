#!/usr/bin/python

'''
uses the encoder function in a seperate file to demo the encoders
'''

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
import Motor_Functions as MOTORS
import Encoder_Functions as ENCODERS

#Forward motor config        
GPIO.setup(ENCODERS.inPin1, GPIO.IN)
GPIO.add_event_detect(ENCODERS.inPin1, GPIO.RISING, callback = ENCODERS.risingEdge1)

#Back motor config
GPIO.setup(ENCODERS.inPin2, GPIO.IN)
GPIO.add_event_detect(ENCODERS.inPin2, GPIO.RISING, callback = ENCODERS.risingEdge2) 

print("test started")
MOTORS.Motors_Init() #inits motors
print("motors inited")
MOTORS.Motors_Start(90, MOTORS.FORWARD, 90, MOTORS.FORWARD)
time.sleep(3)
MOTORS.Motors_Stop()
print("STOPPED")
MOTORS.Motors_Cleanup()
print("cleaned up")
