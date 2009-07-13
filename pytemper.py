#!/usr/bin/env python

"""
The MIT License

Copyright (c) 2008 Anthony Lieuallen ( http://arantius.com/ )

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__version__ = '1.0.2'

import serial
from time import sleep

class TemperReadError(Exception): pass

class Temper:
	def __init__(self, port, offset, mode='f'):
		self.offset=offset
		self.mode=mode

		self.port=serial.Serial('/dev/ttyUSB'+`port`, rtscts=1)
	
	def startIic(self):
		self.sdOut(1)
		self.sclk(1)
		self.sdOut(0)
		self.sclk(0)

	def stopIic(self):
		self.sdOut(0)
		self.sclk(1)
		self.sdOut(1)

	def sdIn(self):
		self.sdOut(1)
		return self.port.getCTS()

	def sdOut(self, n):
		self.port.setRTS(n)
		sleep(0.001)
	
	def sclk(self, n):
		self.port.setDTR(n)

	def hiLoSclk(self):
		self.sclk(1)
		self.sclk(0)

	def writeStream(self, stream):
		for b in stream:
			self.sdOut(int(b))
			self.hiLoSclk()
	
	def read(self):
		# Init
		self.sdOut(1)
		self.sdIn()
		self.sdOut(0)
		self.sdIn()
		self.startIic()
		self.writeStream('10011111')
		self.sclk(1)

		# Wait for ready
		i=0
		while self.sdIn() and i<0xC350:
			sleep(0.001)
		
		# Check status
		tt=self.sdIn()
		self.hiLoSclk()
		if (1==tt):
			raise TemperReadError

		# Read data into buffer
		buf=[]
		for i in range(16):
			s=self.sdIn()
			self.hiLoSclk()
			buf.append(s)

			if i==7:  # don't ask me why!
				self.sdIn()
				self.hiLoSclk()
		self.sclk(0)
		self.hiLoSclk()
		self.stopIic()

		# Convert bit list into (centigrade) temperature
		temp=reduce(lambda x,y: int(x)*2 + y, buf[0:11])
		if buf[0]:
			temp-=2048
		temp/=8.0
		
		# Convert to fahrenheit?
		if self.mode=='f':
			temp=( temp * 9.0/5.0 )+32

		return temp+self.offset

if '__main__'==__name__:
	print Temper(0, 0).read()
