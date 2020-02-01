def getNewProcess(ready, time):
	currentProcess="none"
	if(len(ready)>0):
		currentProcess=ready[0]
		if(currentProcess['startTime']==-1):
			currentProcess['startTime']=time
		del ready[0]
	return currentProcess