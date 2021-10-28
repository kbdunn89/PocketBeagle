#!/usr/bin/python

'''
final motor functions. This is the master version
'''

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time

#defines pins used for PWM and outputs for Motors
Dir_L = "P2_2"
Dir_R = "P2_6"
PWM_L = "P2_1"
PWM_R = "P2_3"
SLP_L = "P2_4"
SLP_R = "P2_8"

#possible macros? CHECK
FORWARD = 0
REVERSE = 1

#pins put into arrays for easier mass operations using for each loop
slp = [SLP_L, SLP_R]
diR = [Dir_L, Dir_R]
pwm = [PWM_L, PWM_R]


def Motors_Init():
	#sleep and direction pins set as GPIO
	GPIO.setup(Dir_L, GPIO.OUT)
	GPIO.setup(Dir_R, GPIO.OUT)
	GPIO.setup(SLP_L, GPIO.OUT)
	GPIO.setup(SLP_R, GPIO.OUT)
	
	#sets the direction to forward (0 is forward 1 is backward)	
	for pin in diR:
		GPIO.output(pin, GPIO.LOW)
	
	#starts PWM DOUBLE CHECK THE 100 HZ
	for pin in pwm:
		PWM.start(pin, 0, 100, 0) #(pin, pulse width, frequency, polarity)
		
	#enables sleep (sleep is negative logic)
	for pin in slp:
		GPIO.output(pin, GPIO.LOW)	
	
def Motors_Stop():
	#sets PWM to 0 duty cycle
	for pin in pwm:
		PWM.set_duty_cycle(pin, 0) #(pin, pulse width)
		
	#enables sleep (sleep is negative logic)
	for pin in slp:
		GPIO.output(pin, GPIO.LOW)	
	
def Motors_Start(left_duty, left_dir, right_duty, right_dir):
	#set left direction
	if (left_dir == FORWARD): #forward direction 
		GPIO.output(Dir_L, GPIO.LOW)
	else:					  #reverse direction
		GPIO.output(Dir_L, GPIO.HIGH)
		
	#set right direction
	if (right_dir == FORWARD): #forward direction 
		GPIO.output(Dir_R, GPIO.LOW)
	else:					  #reverse direction
		GPIO.output(Dir_R, GPIO.HIGH)
		
	#set PWM's
	PWM.set_duty_cycle(PWM_L, left_duty)
	PWM.set_duty_cycle(PWM_R, right_duty)
	
	#disables sleep (sleep is negative logic)
	for pin in slp:
		GPIO.output(pin, GPIO.HIGH)
	
def Motors_Left_Start(duty, diR):
	#set left direction
	if (diR == FORWARD): #forward direction 
		GPIO.output(Dir_L, GPIO.LOW)
	else:					  #reverse direction
		GPIO.output(Dir_L, GPIO.HIGH)
	
	#set PWM's
	PWM.set_duty_cycle(PWM_L, duty)
	
	#disables sleep (sleep is negative logic)
	GPIO.output(SLP_L, GPIO.HIGH)
	
def Motors_Right_Start(duty, diR):
	#set left direction
	if (diR == FORWARD): #forward direction 
		GPIO.output(Dir_R, GPIO.LOW)
	else:					  #reverse direction
		GPIO.output(Dir_R, GPIO.HIGH)
	
	#set PWM's
	PWM.set_duty_cycle(PWM_R, duty)
	
	#disables sleep (sleep is negative logic)
	GPIO.output(SLP_R, GPIO.HIGH)
	
def Motors_Left_Stop():
	#sets PWM to 0 duty cycle
	PWM.set_duty_cycle(PWM_L, 0) #(pin, pulse width)
		
	#enables sleep (sleep is negative logic)
	GPIO.output(SLP_L, GPIO.LOW)
	
def Motors_Right_Stop():
	#sets PWM to 0 duty cycle
	PWM.set_duty_cycle(PWM_R, 0) #(pin, pulse width)
		
	#enables sleep (sleep is negative logic)
	GPIO.output(SLP_R, GPIO.LOW)
	
def Motors_Cleanup():
	for pin in pwm:
		PWM.stop(pin)
	
	#enables sleep (sleep is negative logic)
	for pin in slp:
		GPIO.output(pin, GPIO.LOW)
		
	GPIO.cleanup()
	PWM.cleanup()
	
	
	
	
	
	
	
	
	
	
	
	
	