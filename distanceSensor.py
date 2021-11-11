#!/usr/bin/python

import time
from ctypes import *

sensor = CDLL("./sensor.so")
sensor.init()
sensor.argtype = None
sensor.MeasureInCentimeters.restype = c_float
sensor.MeasureInInches.restype = c_float
d = sensor.MeasureInCentimeters()
i = sensor.MeasureInInches()
sensor.release()
print(d, " cm")
print(i, " in")
