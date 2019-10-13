#/usr/bin/python
import gv

# label, %, x1, y1, x2, y2, angle	

def overlap_elimination(item, results) :
	for i in range(0,item):
		for j in range(i,item):
			if i!=j and results[i][0]==results[j][0]:
				kx=max(results[i][2],results[j][2])
				zx=min(results[i][4],results[j][4])
				
				ky=max(results[i][3],results[j][3])				
				zy=min(results[i][5],results[j][5])
				
				if kx-zx<0 and ky-zy<0:
					areaI=(results[i][4]-results[i][2])*(results[i][5]-results[i][3])
					areaJ=(results[j][4]-results[j][2])*(results[j][5]-results[j][3])
					overlapArea=(zx-kx)*(zy-ky)
					if overlapArea/min(areaI,areaJ)>=gv.configOverlapThreshold:
						if areaI>areaJ:
							results[j][0]=results[j][0]+"!"
							k = j;
						else:
							results[i][0]=results[i][0]+"!"
							k = i;
						if gv.configDebugText :
							print "REMOVED :", k, results[k][0], results[k][1], "% A",results[k][6]," X1", results[k][2], " Y1", results[k][3], "X2", results[k][4], "Y2", results[k][5]
