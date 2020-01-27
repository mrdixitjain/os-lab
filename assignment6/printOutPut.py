def printOutput(endedProcess, scheduling):
	print(scheduling)
	endedProcess=sorted(endedProcess, key = lambda i: i['pid'])[:]
	print("Turn Around Time", end=" -> ")
	sumResponse=0
	for i in endedProcess:
		print("("+str(i['pid'])+", "+str(i['endTime']-i['arrivalTime'])+"),", end=" ")
		sumResponse+=i['endTime']-i['arrivalTime']
	print(sumResponse/len(endedProcess))

	print("Response Time", end=" -> ")
	sumResponse=0
	for i in endedProcess:
		print("("+str(i['pid'])+", "+str(i['startTime']-i['arrivalTime'])+"),", end=" ")
		sumResponse+=i['startTime']-i['arrivalTime']
	print(sumResponse/len(endedProcess))

	print("Waiting Time", end=" -> ")
	sumResponse=0
	for i in endedProcess:
		print("("+str(i['pid'])+", "+str(i['endTime']-i['arrivalTime']-i['totalBurst'])+"),", end=" ")
		sumResponse+=i['endTime']-i['arrivalTime']-i['totalBurst']
	print(sumResponse/len(endedProcess))
	return