#!/usr/bin/python
from picamera import PiCamera
from subprocess import Popen, PIPE
import threading
import os, fcntl
import spidev
import time
import os
import joystick
import gv 
import yolo
import ocr

#
#		Functions
#
def changeMode(type):
	global mode
	if type == 1 :
		if gv.mode == 0 :
			gv.mode = 1
			print ">>>> OCR Mode"
		else :
			gv.mode = 0
			print ">>>> Yolo Mode"
	elif type == 2 :
		if gv.mode == 0 :
			gv.mode = 1
			print ">>>> OCR Mode"
		else :
			gv.mode = 0
			print ">>>> Yolo Mode"

	joystick.stickReleased(spi)

	if gv.configReadText :
		if gv.mode == 0 :
			os.system("aplay -D sysdefault run_data/yolo_mode.wav")
		elif gv.mode == 1 :
			os.system("aplay -D sysdefault run_data/ocr_mode.wav")

		os.system("aplay -D sysdefault run_data/short_beep_small.wav")

	print ""
	print ">>> Ready"

def volumeAdjust(n):
	global volume
	
	print ">>>> VolumeAdjust"
	
	if n==8 and gv.volume!=10:
		gv.volume=gv.volume-10
	elif n==4 and gv.volume!=100:
		gv.volume=gv.volume+10
	os.system("amixer controls")
	os.system("amixer set 'Master' "+str(gv.volume)+"%")
	if gv.configReadText :
		os.system("aplay -D sysdefault run_data/short_beep_small.wav")
	joystick.stickReleased(spi)

	print ""
	print ">>> Ready"

#
#		Main
#
gv.mode=0			# 0 : yolo, 1 : ocr 

# Open SPI communication
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 50000

# Set Volume
os.system("amixer controls")
os.system("amixer set 'Master' 50%")

# Open Camera
camera = PiCamera()

#Yolo v3 is a full convolutional model. It does not care the size of input image, as long as h and w are multiplication of 32

camera.resolution = (gv.configScreenWidth, gv.configScreenHeight)

#spawn darknet process
yolo_proc = Popen([	"./darknet",
			"detect",
			"./cfg/yolov3-tiny.cfg",
			"./run_data/yolov3-tiny.weights",
			"-thresh","0.2"],
			stdin = PIPE, stdout = PIPE)

fcntl.fcntl(yolo_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

gv.idx = 0
gv.first = True

while True:
	if gv.configContMode == False:
		while True:
			js_value = joystick.readJoystick(spi)
			if js_value&1 == 1 :
				break;		# button pushed in single mode
			elif js_value/10 == 1 :
				changeMode(1)
			elif js_value/10 == 2 :
				changeMode(2)
			elif js_value/10 == 4 :
				volumeAdjust(4)			# Joystick up
			elif js_value/10 == 8 :
				volumeAdjust(8)			# Joystick down

		joystick.switchReleased(spi)	# Wait for sw released

	if gv.mode == 0 : 
		yolo.callYolo(yolo_proc, camera)
	else :
		ocr.callOCR(camera)
