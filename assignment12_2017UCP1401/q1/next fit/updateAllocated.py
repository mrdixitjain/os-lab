from freeMemory import *

def updateAllocated(allocated, memory, n):
	i = 0
	while(i<len(allocated)):
		allocated[i].maxTime-=1
		if(allocated[i].maxTime<=0):
			n = freeMemory(allocated[i], memory, n)
			del allocated[i]
			i-=1
		i+=1
	return n
