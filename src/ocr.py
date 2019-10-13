#!/usr/bin/python
from picamera import PiCamera
from subprocess import Popen, PIPE
import threading
import os, fcntl
import cv2
import math
import time
import os
import itd
import gv
import post_processing
import numpy as np
from PIL import Image
import threading


def imgToString(filename):
	os.system("tesseract "+filename+" res")
	ans=open("temp_data/res.txt","r")

	results= ans.read()
	#print results
	ans.close()

	return results

def callOCR( camera ) :
	global first
	global idx
	
	print ">>> OCR called"

	# Take picture
	filename = 'temp_data/frame_ocr.jpg'
	camera.capture(filename)

	

    # Filter if true
	if gv.configOcrFilter:
		tempImg=cv2.imread(filename)
		
		#Grayscale
		tempImg=cv2.cvtColor(tempImg, cv2.COLOR_BGR2GRAY)
		
		#Gaussian Threshold
		tempImg=cv2.adaptiveThreshold(tempImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 2)
		
		#Sharpening
		kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
		tempImg = cv2.filter2D(tempImg, -1, kernel)
		
		#Median Blur
		tempImg=cv2.medianBlur(tempImg, 3)
		
		cv2.imwrite(filename,tempImg)

	try :
		if gv.configShowFig :
			cv2.imshow('ocr_figure',tempImg)
			cv2.moveWindow('ocr_figure',10,10)
			key = cv2.waitKey(1000) 
	except Exception:
		print "fail to open ",filename
		pass
	
	# Run OCR
	answer=imgToString(filename)
	
	#Text Processing (removing extraneous characters)
	answer=answer.replace("\n \n","\n")
	answer=answer.replace("\n\n","\n")
	answer=answer.replace("\n \n","\n")
	answer=answer.replace("\n\n","\n")
	answer=answer.replace("  "," ")
	temp=""
	for i in range(0,len(answer)):
		
		if (ord(answer[i])>=97 and ord(answer[i])<=122) or (ord(answer[i])>=65 and ord(answer[i])<=90) or ord(answer[i])==32 or ord(answer[i])==46 or ord(answer[i])==10 or (ord(answer[i])>=47 and ord(answer[i])<=57):
			
			temp=temp+answer[i]
			
	answer=temp
	print "=================================================================="
	print answer
	print "=================================================================="
	if len(answer)>=gv.configNumCharToRead:
			answer=answer[0:gv.configNumCharToRead-1]
	
	if gv.configReadText :
		os.system("pico2wave -w temp_data/ocr.wav \"" + answer +"\"")
		os.system("aplay -D sysdefault temp_data/ocr.wav")
		if gv.configRemoveWav :
			os.system("rm  temp_data/ocr.wav")

        if gv.configReadText :
            os.system("aplay run_data/short_beep_small.wav")

	print ""
	print ">>> Ready"

