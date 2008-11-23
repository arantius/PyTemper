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
		self.startIic()
		self.writeStream('10011111')

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
		self.stopIic()

		# Convert bit list into (centigrade) temperature
		temp=reduce(lambda x,y: int(x)*2 + y, buf[1:11])/8.0
		
		# Convert to fahrenheit?
		if self.mode=='f':
			temp=( temp * 9.0/5.0 )+32;

		return temp

if '__main__'==__name__:
	print Temper(0, 0).read()
