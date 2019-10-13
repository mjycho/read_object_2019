#!/usr/bin/python
import os, fcntl
import math
import os
import gv

def itdCall(angle):
	binaryfile=open("temp_data/before_itd.wav", "rb")
	myArr=binaryfile.read()
	binaryfile.close()

	# Get ChunkSize
	chunkSize=ord(myArr[4])+ord(myArr[5])*256+ord(myArr[6])*65536+ord(myArr[7])*16777216	

	# Get SubChunk2Size
	subChunk2Size=chunkSize-36

	# angle positve : from right, negative : from left
	d=gv.constHeadWidth*math.cos(math.radians(angle))

	shiftAmnt=int(d*46.6472)

	# Create ans list
	ans=list(myArr)

	# update subChunk2Size
	temp=int(2*(subChunk2Size+shiftAmnt*2))
	ans[43]=chr(temp/16777216)
	ans[42]=chr((temp%16777216)/65536)
	ans[41]=chr((temp%65536)/256)
	ans[40]=chr(temp%256)

	# Update chunkSize
	temp=temp+36
	ans[7]=chr(temp/16777216)
	ans[6]=chr((temp%16777216)/65536)
	ans[5]=chr((temp%65536)/256)
	ans[4]=chr(temp%256)

	# update BlockAlign
	ans[32]=chr(04)

	# update NumChannel 22
	ans[22]=chr(02)

	# remove data
	del ans [44:] 

	# Copy 1ch audio in myArr to 2 ch audio in ans
	if angle > 0 :
		l0r1 = 0
	else:
		l0r1 = 1
	for i in range(44,len(myArr)+shiftAmnt*2, 2):
		#left

		if((l0r1==0) and (i-shiftAmnt*2 < 44)) or ((l0r1==1) and (i>=len(myArr))):
			ans.append(chr(00))
			ans.append(chr(00))
		else:
			
			if l0r1==0 :
				tempNum=ord(myArr[i-shiftAmnt*2])+ord(myArr[i-shiftAmnt*2+1])*256   			
				if ord(myArr[i-shiftAmnt*2+1])/128 == 1:   
					tempNum = tempNum - 65536 	# negative number
				tempNum=int(tempNum*((gv.constAmpCoeff-1)/(gv.constHeadWidth)*d+1))
				if tempNum<0  :
					tempNum = tempNum + 65536
				ans.append(chr(tempNum%256))
				ans.append(chr(int(tempNum/256)))
			else :
				ans.append(myArr[i])
				ans.append(myArr[i+1])

		#right
		if((l0r1==1) and (i-shiftAmnt*2 < 44)) or ((l0r1==0) and (i>=len(myArr))):
			ans.append(chr(00))
			ans.append(chr(00))
		else:
			if l0r1==1 :
				tempNum=ord(myArr[i-shiftAmnt*2])+ord(myArr[i-shiftAmnt*2+1])*256   			
				if ord(myArr[i-shiftAmnt*2+1])/128 == 1:   
					tempNum = tempNum - 65536	# negative number
				tempNum=int(tempNum*((gv.constAmpCoeff-1)/(gv.constHeadWidth)*d+1))
				if tempNum<0  :
					tempNum = tempNum + 65536
				ans.append(chr(tempNum%256))
				ans.append(chr(int(tempNum/256)))
			else :
				ans.append(myArr[i])
				ans.append(myArr[i+1])

	# transition back to string
	for i in range(0,len(ans)):
		ans[i]=str(ans[i])

	# Write output wav
	fileWrite=open("temp_data/after_itd.wav", "wb")
	fileWrite.write("".join(ans))
	fileWrite.close()
