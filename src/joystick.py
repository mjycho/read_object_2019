#!/usr/bin/python
import spidev

def readChannel(spi, channel):
        adc=spi.xfer2([1,(8+channel)<<4,0])
        data=((adc[1]&3)<<8)+adc[2]
        return data

def readJoystick(spi):
	switch  = readChannel(spi, 0)
	vry_pos = readChannel(spi, 1)
	vrx_pos = readChannel(spi, 2)
	if switch < 100 : 
		joystick = 1		# pushed
	else :
		joystick = 0		# not pusehd
	if vrx_pos < 300 :
		joystick += 10		# left
	elif vrx_pos > 1000 :
		joystick += 20		# right
	elif vry_pos < 300 : 
		joystick += 40		# up
	elif vry_pos > 1000 :
		joystick += 80 		# down
	return joystick

def switchReleased(spi):
	while True :
		if(readChannel(spi, 0)>100) : 
			break

def stickReleased(spi):
	while True :
		ch1 = readChannel(spi,1)
		ch2 = readChannel(spi,2)
		if ch1 < 800 and ch1 > 400 and ch2 < 800 and ch2 > 400 :
			break
