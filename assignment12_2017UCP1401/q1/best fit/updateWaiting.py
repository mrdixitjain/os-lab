from allocateMemory import *

def updateWaiting(allocated, waiting, memory, succReq, totalReq):
	for i in waiting:
		totalReq += 1
		if(allocateMemory(i, memory)):
			allocated.append(i)
			succReq += 1
			waiting.remove(i)