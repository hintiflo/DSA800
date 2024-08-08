#!/usr/bin/env python
# -*- coding: utf-8 -*-
# scripted tools for EMI 
# latest edit: 13.06.2024

import pyvisa
import socket
from time import sleep

# >>> from DSA800 import DSA800
# >>> dsa = DSA800()

class DSA800:
	analyzerConnected = False
	timeout = 0
	def setTimeout(self, time):				self.timeout = time

	def shootAndStop(self):		
		specki.write(":INITiate:CONTinuous 0");			
		sleep(float(getSweepTime()))
		print( "shootAndStop DONE" )
		freeSpeckKeys()
	def run(self):				specki.write(":INITiate:CONTinuous 1");			freeSpeckKeys()
	def disconnect(self):		specki.close()
	def connect(self):			specki.open()
	def getID(self):			resp = (specki.query("*IDN?")).strip();		freeSpeckKeys();	return resp
	def init(self):
		rm = pyvisa.ResourceManager('@py')
		ip = "169.254.63.149"
		visaAddress = "TCPIP0::" + ip + "::inst0::INSTR"
		specki = rm.open_resource(visaAddress,chunk_size=8000,timeout=2000) # , delay=1.2)	# ... seconds
		dev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		dev.connect((ip, 5555))
		analyzerConnected = True
