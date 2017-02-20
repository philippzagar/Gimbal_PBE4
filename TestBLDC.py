#!/usr/bin/python

from BLDC import *
import time

bldc = BLDC()

#bldc.start()
bldc.start_pigpio()

while 1:
    #bldc.run()
    bldc.run_pigpio()
    # bldc.printDCValues()
    time.sleep(0.001)

bldc.stop()