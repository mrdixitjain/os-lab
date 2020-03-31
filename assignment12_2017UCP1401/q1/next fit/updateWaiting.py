from allocateMemory import *

def updateWaiting(allocated, waiting, memory, succReq, totalReq, n):
	for i in waiting:
		totalReq += 1
		a = allocateMemory(i, memory, n)
		n = a[1]
		if(a[0]):
			allocated.append(i)
			succReq += 1
			waiting.remove(i)
	return n