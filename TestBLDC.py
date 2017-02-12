#!/usr/bin/python

from BLDC import *
import time

bldc = BLDC()

bldc.start()

for i in range(1000):
    bldc.run()
    bldc.printDCValues()
    time.sleep(0.01)

bldc.stop()