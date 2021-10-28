from ctypes import *
from time import sleep

sensor = CDLL("./sensor.so")
sensor.init()
leds = CDLL("./leds.so")
leds.init()

delayVal = 600
for i in range(200):
    leds.turnOn()
    val = sensor.readSensor(delayVal)
    leds.turnOff()
    #if not (i % 25):
        #delayVal = delayVal + 25
    for x in range(8):
        print("val[", x, "]: ", val>>x & 0x01)
    print(delayVal, "\n\n")
    sleep(0.1)
sensor.release()
leds.turnOff()
leds.release()

print("All done")