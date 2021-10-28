#!/usr/bin/python

'''
The goal of this file is to read rpm from the motors, and according to the current 
motor RPM and the desired RPM, the appropriate motor RPM is set. The logic used to
figure out the appropriate motor RPM is done by a PID controller. For now only the 
P part is being used.
'''

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
import Motor_Functions as MOTORS
import motorPID as motorPID

#Variable definition
ELeft = 0.0         #Error for Left motor PID calculation
EprevLeft = 0.0     #Placeholder for storing previous effort for Left motor
LeftPWM = 0         #Initialize RPM for Left motor

ERight = 0.0        #Error for Right motor PID calculation
EprevRight = 0.0    #Placeholder for storing previous effort for Right motor
RightPWM = 0        #Initialize RPM for Right motor

setRPM = 130    #Desired RPM for both motors

'''
this is the PID function. It is called every time the appropriate motor RPM 
needs to  be calculated 
'''
def controllerPID(E, Eprev, dT, Kp, Ki, Kd):
    P = Kp * E;
    I = Ki * (0.5 * (E + Eprev)) * dT
    D = Kd * (E - Eprev) / dT
    return(P + I + D)

#Left motor config        
GPIO.setup(motorPID.inPin1, GPIO.IN)
GPIO.add_event_detect(motorPID.inPin1, GPIO.RISING, callback = motorPID.risingEdge1)

#Right motor config
GPIO.setup(motorPID.inPin2, GPIO.IN)
GPIO.add_event_detect(motorPID.inPin2, GPIO.RISING, callback = motorPID.risingEdge2) 

print("test started ...")
MOTORS.Motors_Init() #inits motors
print("motors inited ...")
#MOTORS.Motors_Start(0, MOTORS.FORWARD, 0, MOTORS.FORWARD)
#time.sleep(1)

#gets the start time 
startTime = time.time()


'''
this loop consistently runs so that the appropriate motor RPM is constantly being 
calculated

to start the calculateRPM() function is called. This function calculates the current
motor RPM's. The values are stores in rpm1(left motor) and rpm2(right motor)

the value of the two motors RPM's are printed

the error between the set RPM and the current motor RPM is then calculated
this error value is passed to the PID function where it is used to calculate the P
value. This gets us the correct PID value to be used in the new motor RPM calculations

depending on the value of the set RPM, the designated left and right PWM values are set
if the set RPM is 0 then the set PWM is 0

if not then the left and right PWM values are calculated based on the current PWM and the 
calculation done for the variation needed in the PWM to get the desired RPM
'''
while ((time.time() - startTime) < 5): #only done for 5 seconds
    motorPID.calculateRPM()
    print(str(motorPID.rpm1) + "\t" + str(motorPID.rpm2))

    #print("Left motor RPM: " + str(motorPID.rpm1))
    #print("Right motor RPM: " + str(motorPID.rpm2))

    ELeft = setRPM - motorPID.rpm1
    ERight = setRPM - motorPID.rpm2
    #print("Eleft: " + str(ELeft))

    cPIDLeft = controllerPID(ELeft, EprevLeft, 0.1, 1, 0, 0)
    cPIDRight = controllerPID(ERight, EprevRight, 0.1, 1, 0, 0)
    #print("cPID: " + str(cPID))
    
    if(setRPM == 0):
        LeftPWM = 0
        RightPWM = 0
    else:
        LeftPWM = LeftPWM + (cPIDLeft/3)
        RightPWM = RightPWM + (cPIDRight/3)
        
    if (LeftPWM > 90):
        LeftPWM = 90
        
    if (LeftPWM < 10):
        LeftPWM = 10
        
    if (RightPWM > 90):
        RightPWM = 90
        
    if (RightPWM < 10):
        RightPWM = 10
        
    MOTORS.Motors_Start(LeftPWM, MOTORS.FORWARD, RightPWM, MOTORS.FORWARD)

    EprevLeft = ELeft
    EprevRight = ERight
    
MOTORS.Motors_Stop()
print("STOPPED")
MOTORS.Motors_Cleanup()
print("cleaned up")
