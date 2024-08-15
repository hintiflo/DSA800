#!/usr/bin/env python
# -*- coding: utf-8 -*-
# testDSA800.py

from DSA800 import DSA800
from time import sleep


# dsa = DSA800("192.168.0.3")
dsa = DSA800("192.168.0.103")
# dsa.init()
print(dsa.getID(), flush = True)
print(dsa.getSweepTime(), flush = True)
# dsa.disconnect()
# sleep(4)
# dsa.connect()
# print(dsa.getID())

# dsa.screenshot("toast")

dsa.setDetPosPeak()
sleep(1)
dsa.setDetQPeak()
sleep(1)
dsa.setDetRms()
sleep(1)
dsa.setDetVav()

