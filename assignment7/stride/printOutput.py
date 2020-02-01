def printOutput(endedProcess, scheduling):
	print(scheduling)
	endedProcess=sorted(endedProcess, key = lambda i: i['pid'])[:]
	print("Turn Around Time", end=" -> ")
	sumResponse=0
	for i in endedProcess:
		print("("+str(i['pid'])+", "+str(i['endTime']-0)+"),", end=" ")
		sumResponse+=i['endTime']-0
	print(sumResponse/len(endedProcess))

	print("Response Time", end=" -> ")
	sumResponse=0
	for i in endedProcess:
		print("("+str(i['pid'])+", "+str(i['startTime']-0)+"),", end=" ")
		sumResponse+=i['startTime']-0
	print(sumResponse/len(endedProcess))

	print("Waiting Time", end=" -> ")
	sumResponse=0
	for i in endedProcess:
		print("("+str(i['pid'])+", "+str(i['endTime']-0-i['totalBurst'])+"),", end=" ")
		sumResponse+=i['endTime']-0-i['totalBurst']
	print(sumResponse/len(endedProcess))
	return