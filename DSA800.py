#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Class to encapsulate a Rigol DSA800 spectrum analyzer
# with scpi commands via TCP connection

import pyvisa
import socket
from time import sleep

class DSA800:
	analyzerConnected = False
	timeout = 0
	dev = 0
	ip = ""
	port = 5555

	def __init__(self, IP):
		self.ip = IP
	# def init(self):
		self.dev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.dev.connect((self.ip, self.port))
		self.analyzerConnected = True

	def tcpTx(self, cmd):			
		self.dev.sendall((cmd + '\n').encode("utf-8"))
	
	def tcpRx(self):			
		# resp = str(self.dev.recv(4096).decode("utf-8"))
		# resp = str(self.dev.recv(1024).decode("utf-8"))
		resp = str(self.dev.recv(100).decode("utf-8"))
		return resp
	
	def tcpTxRx(self, cmd):			
		self.tcpTx(cmd)
		return (self.tcpRx())
	
	def disconnect(self):		
		self.dev.close()
		self.analyzerConnected = False

	def connect(self):			
		self.dev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.dev.connect((self.ip, self.port))
		self.analyzerConnected = True
	
	def setTimeout(self, time):				self.timeout = time

	def freeSpeckKeys(self):				self.tcpTx(':SYSTem:COMMunicate:BRMT OFF|')
	def setSweepTime(self, period): 		self.tcpTx(":SENSe:SWEep:TIME " + str(period));	self.freeSpeckKeys()
	def getSweepTime(self): 				resp = (self.tcpTxRx(":SENSe:SWEep:TIME?")).strip();	self.freeSpeckKeys();	return resp 
	def setRBW(self, bw):			 		self.tcpTx(":SENSe:BANDwidth:RESolution " + str(bw));	self.freeSpeckKeys()
	def getRBW(self):		 				resp = (self.tcpTxRx(":SENSe:BANDwidth:RESolution?")).strip();	self.freeSpeckKeys();	return resp 
	def getMarkerState(self, marker): 		resp = (self.tcpTxRx(":CALCulate:MARKer" + str(marker) + ":STATe?")).strip();	self.freeSpeckKeys();	return resp 
	def getMarkerFreq(self, marker):		resp = (self.tcpTxRx(":CALCulate:MARKer" + str(marker) + ":X?")).strip();	self.freeSpeckKeys();	return resp 
	def setMarkerFreq(self, marker, freq):	self.tcpTx(":CALCulate:MARKer" + str(marker) + ":X " + str(freq));	self.freeSpeckKeys()
	def getMarkerValue(self, marker): 		resp = (self.tcpTxRx(":CALCulate:MARKer" + str(marker) + ":Y?")).strip();	self.freeSpeckKeys();	return resp
	def setMarkerOff(self, marker): 		self.tcpTx(":CALCulate:MARKer" + str(marker) + ":STATe off");	self.freeSpeckKeys() 
	def setMarkerOn(self, marker): 			self.tcpTx(":CALCulate:MARKer" + str(marker) + ":STATe on");	self.freeSpeckKeys() 
	def setMarkersOn(self):		 		
		self.tcpTx(":CALCulate:MARKer1:STATe on");	
		self.tcpTx(":CALCulate:MARKer2:STATe on");	
		self.tcpTx(":CALCulate:MARKer3:STATe on");	
		self.tcpTx(":CALCulate:MARKer4:STATe on");	
		self.freeSpeckKeys() 
	def setPreampOn(self):					self.tcpTx(':SENSe:POWer:RF:GAIN:STATe ON');	self.freeSpeckKeys() 
	def setPreampOff(self):					self.tcpTx(':SENSe:POWer:RF:GAIN:STATe OFF');	self.freeSpeckKeys() 
	def getPreampState(self):				resp = self.tcpTxRx(':SENSe:POWer:RF:GAIN:STATe?').strip();	self.freeSpeckKeys(); return resp
	def setDetQPeak(self): 					self.tcpTx(":SENSe:DETector:FUNCtion QPEak");	self.freeSpeckKeys()
	def setDetRms(self):					self.tcpTx(":SENSe:DETector:FUNCtion rms");		self.freeSpeckKeys()
	def setDetVav(self):					self.tcpTx(":SENSe:DETector:FUNCtion vav");	self.freeSpeckKeys()
	def setDetPosPeak(self):				self.tcpTx(":SENSe:DETector:FUNCtion pos");	self.freeSpeckKeys()
	def setUnitDbvu(self):					self.tcpTx(":UNIT:POWer dbuv");				self.freeSpeckKeys()
	def setYScale(self, scale):
		if( 0.1 >= scale and scale <= 20): 
			self.tcpTx(":DISPlay:WINdow:TRACe:Y:SCALe:PDIVision " + str(scale));				self.freeSpeckKeys()

	def setRefLevel(self, level):
		# if( 0.1 >= scale and scale <= 20): 
		if( True ): 
			self.tcpTx(":DISPlay:WINdow:TRACe:Y:SCALe:RLEVel " + str(level));				self.freeSpeckKeys()

	def setNRefLevel(self, level):
		# if( 0.1 >= scale and scale <= 20): 
		if( True ): 
			self.tcpTx(":DISPlay:WINdow:TRACe:Y:SCALe:NRLevel " + str(level));				self.freeSpeckKeys()

	def getFilterEmi(self):					resp = self.tcpTxRx(":SENSe:BANDwidth:EMIFilter:STATe?").strip();	self.freeSpeckKeys(); return resp
	def setFilterEmi(self):					self.tcpTx(":SENSe:BANDwidth:EMIFilter:STATe ON");				self.freeSpeckKeys()
	def setFilterGauss(self):				self.tcpTx(":SENSe:BANDwidth:EMIFilter:STATe OFF");				self.freeSpeckKeys()
	def getContinous(self):					resp = self.tcpTxRx(":INITiate:CONTinuous?").strip();	self.freeSpeckKeys(); return resp

	def screenshot(self, fn):
		fn = fn + ".bmp"
		aggregateSize = 1152066

		self.tcpTx(":PRIV:SNAP? BMP")
		bemp = self.dev.recv(4096)
		aggregateSize -= len(bemp)

		while aggregateSize > 0:
			rxData = self.dev.recv(4096)
			bemp += rxData
			aggregateSize -= len(rxData)

		with open(fn, "wb") as feil:
			feil.write(bemp[11:])

		self.cropDSA815screens(fn)
		self.freeSpeckKeys()
		
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
		self.tcpTx(":INITiate:CONTinuous 0");			
		sleep(float(getSweepTime()))
		print( "shootAndStop DONE" )
		self.freeSpeckKeys()
	def run(self):				self.tcpTx(":INITiate:CONTinuous 1");			self.freeSpeckKeys()
	def getID(self):			return self.tcpTxRx("*IDN?").strip()

