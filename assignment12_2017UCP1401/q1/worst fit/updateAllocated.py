from freeMemory import *

def updateAllocated(allocated, memory):
	i = 0
	while(i<len(allocated)):
		allocated[i].maxTime-=1
		if(allocated[i].maxTime<=0):
			freeMemory(allocated[i], memory)
			del allocated[i]
			i-=1
		i+=1