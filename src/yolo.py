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

def callYolo( yolo_proc, camera ) :
	global first
	global idx

	print ">>> Yolo called"

	if gv.first :
		if gv.configContMode :
			time.sleep(30)
		while True :
			temp = yolo_proc.stdout.read()
			if 'Enter Image Path' in temp:		# The result is printed
				gv.first = False
				break	
	
	filename = 'temp_data/frame'+str(gv.idx)+'.jpg'
	camera.capture(filename)
	yolo_proc.stdin.write(filename+'\n')

	stdout = ""
	while True :
		try :
			temp = yolo_proc.stdout.read()
		except Exception : 
			pass
		else :
			stdout = stdout + temp
			if 'Enter Image Path' in temp:		# The result is printed
				break	

	strList = stdout.split("\n")
	if gv.configDebugText :
		print strList

	if(len(strList)>1) :

		# Open figure
		try:
			if gv.configShowFig :
#				while os.path.isfile('./predictions.png') == False :
#					print "x"
				im = cv2.imread('predictions.png')
				cv2.imshow('yolo_figure',im)
				cv2.moveWindow('yolo_figure',10,10)
				#print(im.shape)
				key = cv2.waitKey(1000) 
		except Exception:
			print "fail to open predictions.png"
			pass

		if strList[1]>0:				
			results=[]
			item = 0
			i = 3 
			while i < len(strList)-1 :
				if strList[i].find(':') != -1 :
				  	# label, %, x1, y1, x2, y2, angle	
					results.append(["",0, 0, 0, 0, 0, 0])
					holder=strList[i]
					results[item][0] = holder[:holder.find(":")]
					results[item][1] = int(holder[holder.find(":")+2:holder.find("%")]) 
					i = i +1	
					if '%' in strList[i] :	# Case that same box has two items
						i = i+1
					results[item][2] = int(strList[i])
					i = i +1	
					results[item][3] = int(strList[i])
					i = i +1	
					results[item][4] = int(strList[i])
					i = i +1	
					results[item][5] = int(strList[i])
					results[item][6] = int(((float(results[item][4]+results[item][2])/gv.configScreenWidth)*90.0)-90.0)
					item = item +1
				else :
					i = i + 1
			post_processing.overlap_elimination(item, results)

			for i in range(0,item):
				if "!" not in results[i][0] :
					print i, " ", results[i][0], results[i][1], "% A",results[i][6]," X1", results[i][2], " Y1", results[i][3], "X2", results[i][4], "Y2", results[i][5]
					if gv.configReadText :
						os.system("pico2wave -w temp_data/before_itd.wav \"" + results[i][0] +"\"")
						itd.itdCall(results[i][6])
						#print ">>> ITD Called"
						os.system("aplay -D sysdefault temp_data/after_itd.wav")
						if gv.configRemoveWav :
							os.system("rm  temp_data/after_itd.wav temp_data/before_itd.wav")



		# Move predition.png
		cmd = 'mv predictions.png temp_data/predictions'+str(gv.idx)+'.png'
		os.system(cmd)

		gv.idx = gv.idx + 1

		if gv.configReadText :
			os.system("aplay -D sysdefault run_data/short_beep_small.wav")

		print ""
		print ">>> Ready"

