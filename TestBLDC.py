#!/usr/bin/python

from BLDC import *
import time

bldc = BLDC()

bldc.start_pigpio()
#bldc.test_BLDC()
bldc.changeSpeed(0.1)

while 1:
    time.sleep(0.01)
    bldc.run_pigpio()
    bldc.printDCValues()
