#!/usr/bin/python

from BLDC import *
import time

bldc = BLDC()

bldc.start()

for i in range(50000):
    bldc.run()
    bldc.printDCValues()
    time.sleep(0.1)

bldc.stop()