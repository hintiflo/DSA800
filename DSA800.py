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
	dev = 0
	# ip = "169.254.63.149"
	ip = "192.168.0.3"
	port = 5555

	def setTimeout(self, time):				self.timeout = time

	def freeSpeckKeys(self):				specki.write(':SYSTem:COMMunicate:BRMT OFF|')
	def setSweepTime(self, period): 			specki.write(":SENSe:SWEep:TIME " + str(period));	freeSpeckKeys()
	def getSweepTime(self): 				resp = (specki.query(":SENSe:SWEep:TIME?")).strip();	freeSpeckKeys();	return resp 
	def setRBW(self, bw):			 			specki.write(":SENSe:BANDwidth:RESolution " + str(bw));	freeSpeckKeys()
	def getRBW(self):		 				resp = (specki.query(":SENSe:BANDwidth:RESolution?")).strip();	freeSpeckKeys();	return resp 
	def getMarkerState(self, marker): 		resp = (specki.query(":CALCulate:MARKer" + str(marker) + ":STATe?")).strip();	freeSpeckKeys();	return resp 
	def getMarkerFreq(self, marker):			resp = (specki.query(":CALCulate:MARKer" + str(marker) + ":X?")).strip();	freeSpeckKeys();	return resp 
	def setMarkerFreq(self, marker, freq):	specki.write(":CALCulate:MARKer" + str(marker) + ":X " + str(freq));	freeSpeckKeys()
	def getMarkerValue(self, marker): 		resp = (specki.query(":CALCulate:MARKer" + str(marker) + ":Y?")).strip();	freeSpeckKeys();	return resp
	def setMarkerOff(self, marker): 			specki.write(":CALCulate:MARKer" + str(marker) + ":STATe off");	freeSpeckKeys() 
	def setMarkerOn(self, marker): 			specki.write(":CALCulate:MARKer" + str(marker) + ":STATe on");	freeSpeckKeys() 
	def setMarkersOn(self):		 		
		specki.write(":CALCulate:MARKer1:STATe on");	
		specki.write(":CALCulate:MARKer2:STATe on");	
		specki.write(":CALCulate:MARKer3:STATe on");	
		specki.write(":CALCulate:MARKer4:STATe on");	
		freeSpeckKeys() 
	def setPreampOn(self):					specki.write(':SENSe:POWer:RF:GAIN:STATe ON');	freeSpeckKeys() 
	def setPreampOff(self):					specki.write(':SENSe:POWer:RF:GAIN:STATe OFF');	freeSpeckKeys() 
	def getPreampState(self):				resp = specki.query(':SENSe:POWer:RF:GAIN:STATe?').strip();	freeSpeckKeys(); return resp
	def setDetQuasiPeak(self): 				specki.write(":SENSe:DETector:FUNCtion QPEak");	freeSpeckKeys()
	def setDetRms(self):					specki.write(":SENSe:DETector:FUNCtion rms");	freeSpeckKeys()
	def setDetVav(self):					specki.write(":SENSe:DETector:FUNCtion vav");	freeSpeckKeys()
	def setDetPosPeak(self):				specki.write(":SENSe:DETector:FUNCtion pos");	freeSpeckKeys()
	def setUnitDbvu(self):					specki.write(":UNIT:POWer dbuv");				freeSpeckKeys()
	def setYScale(self, scale):
		if( 0.1 >= scale and scale <= 20): 
			specki.write(":DISPlay:WINdow:TRACe:Y:SCALe:PDIVision " + str(scale));				freeSpeckKeys()

	def setRefLevel(self, level):
		# if( 0.1 >= scale and scale <= 20): 
		if( True ): 
			specki.write(":DISPlay:WINdow:TRACe:Y:SCALe:RLEVel " + str(level));				freeSpeckKeys()

	def setNRefLevel(self, level):
		# if( 0.1 >= scale and scale <= 20): 
		if( True ): 
			specki.write(":DISPlay:WINdow:TRACe:Y:SCALe:NRLevel " + str(level));				freeSpeckKeys()

	def getFilterEmi(self):					resp = specki.query(":SENSe:BANDwidth:EMIFilter:STATe?").strip();	freeSpeckKeys(); return resp
	def setFilterEmi(self):					specki.write(":SENSe:BANDwidth:EMIFilter:STATe ON");				freeSpeckKeys()
	def setFilterGauss(self):				specki.write(":SENSe:BANDwidth:EMIFilter:STATe OFF");				freeSpeckKeys()
	def getContinous(self):					resp = specki.query(":INITiate:CONTinuous?").strip();	freeSpeckKeys(); return resp

	def screenshot(self, fn):
		# dev.connect((ip, 5555))
		aggregateSize = 1152066

		dev.send(b":PRIV:SNAP? BMP \n")
		bemp = dev.recv(4096)
		aggregateSize -= len(bemp)

		while aggregateSize > 0:
			rxData = dev.recv(4096)
			bemp += rxData
			aggregateSize -= len(rxData)

		with open(fn, "wb") as feil:
			feil.write(bemp[11:])

		cropDSA815screens(fn)
		# dev.shutdown(socket.SHUT_RDWR)
		# dev.close()
		
		freeSpeckKeys()
		
	# crop screenshots from Rigol DSA815 for reporting
	def cropDSA815screens(self, fn):	# 691 x 30
		from PIL import Image
		fn = fn.strip()
		# print(fn)
		# src = Image.open(fn.replace(".bmp",".png"))
		src = Image.open(fn)
		width, height = src.size

		left = 0
		top = 30
		right = 695
		bottom = height
		dest = src.crop((left, top, right, bottom))
		dest_fn = fn.replace(".bmp","_cropped.png")
		dest.save(dest_fn)
		return (dest_fn)

	def shootAndStop(self):		
		specki.write(":INITiate:CONTinuous 0");			
		sleep(float(getSweepTime()))
		print( "shootAndStop DONE" )
		freeSpeckKeys()
	def run(self):				specki.write(":INITiate:CONTinuous 1");			freeSpeckKeys()
	def disconnect(self):		self.dev.close()
	def connect(self):			self.dev.connect(self.ip, self.port)
	def getID(self):			
		# self.dev.send(b"*IDN?\n")
		# resp = str(self.dev.recv(4096).decode("utf-8"))
		# return resp
		return self.tcpTxRx("*IDN?")
	
	def tcpTx(self, cmd):			
		self.dev.send((cmd + '\n').encode("utf-8"))
	
	def tcpRx(self):			
		# resp = str(self.dev.recv(4096).decode("utf-8"))
		# resp = str(self.dev.recv(1024).decode("utf-8"))
		resp = str(self.dev.recv(100).decode("utf-8"))
		return resp
	
	def tcpTxRx(self, cmd):			
		self.tcpTx(cmd)
		return (+ self.tcpRx())
	
	
	def init(self):
		# rm = pyvisa.ResourceManager('@py')
		# visaAddress = "TCPIP0::" + ip + "::inst0::INSTR"
		# specki = rm.open_resource(visaAddress,chunk_size=8000,timeout=2000) # , delay=1.2)	# ... seconds
		self.dev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.dev.connect((self.ip, self.port))
		self.analyzerConnected = True
