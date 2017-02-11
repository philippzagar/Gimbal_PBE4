#!/usr/bin/python

from BLDC import *
import time

bldc = BLDC()

bldc.start_BLDC()

for i in range(3000):
    bldc.run_BLDC()
    bldc.printDCValues()
    time.sleep(0.01)

bldc.stop_BLDC()

bldc.__del__()