def updateReady(ready, processes, time):
	while(len(processes)>0 and processes[0]['arrivalTime']<=time):
		ready.append(processes[0])
		del processes[0]
	ready=sorted(ready, key = lambda i: i['priority'], reverse=True)[:]
	return ready


def updateInput(inputQueue, ready, inputRunning): # to update inputQueue[] i.e. to check if any process has done it's work on input devices or if not than decrease it's time by 1.
	if(len(inputQueue)<=0):
		inputRunning.append('idle')
		return
	# print(ioQueue[0]['execution'])
	if(int(inputQueue[0]['execution'][1])>0):
		inputRunning.append(inputQueue[0]['pid'])
		inputQueue[0]['execution'][1]=str(int(inputQueue[0]['execution'][1])-1)
		if(inputQueue[0]['execution'][1]=="0"):
			inputQueue[0]['execution']=inputQueue[0]['execution'][2:]
			if(len(inputQueue[0]['execution'])>0):
				ready.append(inputQueue[0])
			del inputQueue[0]


def updateOutput(outputQueue, ready, outputRunning): # to update oututQueue[] i.e. to check if any process has done it's work on output devices or if not than decrease it's time by 1.
	if(len(outputQueue)<=0):
		outputRunning.append('idle')
		return
	# print(ioQueue[0]['execution'])
	if(int(outputQueue[0]['execution'][1])>0):
		outputRunning.append(outputQueue[0]['pid'])
		outputQueue[0]['execution'][1]=str(int(outputQueue[0]['execution'][1])-1)
		if(outputQueue[0]['execution'][1]=="0"):
			outputQueue[0]['execution']=outputQueue[0]['execution'][2:]
			if(len(outputQueue[0]['execution'])>0):
				ready.append(outputQueue[0])
			del outputQueue[0]


def SRTF(processes):
	prcs=processes[:]
	
	#sorted processes on the basis of arrival time
	processes = sorted(processes, key = lambda i: i['arrivalTime'])[:]#it will hold those process which are yet to be processed.

	# to store processes executing or waiting for input output devices
	inputQueue=[]
	outputQueue=[]

	# to keep track of processes running on cpu, input and output device.
	# here, index will work as time unit.
	cpuRunning=[]
	inputRunning=[]
	outputRunning=[]

	endedProcess=[]

	# all resources will stay idle till first process will arrive.
	if(processes[0]['arrivalTime']>0):
		for i in range(processes[0]['arrivalTime']):
			cpuRunning.append('idle')
			inputRunning.append('idle')
			outputRunning.append('idle')

	currentProcess=processes[0]
	time = currentProcess['arrivalTime']
	if(currentProcess['startTime']==-1):
		currentProcess['startTime']=time
	del processes[0]

	ready=[]
	ready=updateReady(ready, processes, time)

	while(currentProcess!="none" or len(ready)>0 or len(processes)>0 or len(inputQueue)>0 or len(outputQueue)):
		time+=1
		if(currentProcess!="none"):
			if(len(currentProcess['execution'])>0):
				if(currentProcess['execution'][0]=='P'): # i.e. it was working on cpu last.
					if(int(currentProcess['execution'][1])>0):
						cpuRunning.append(currentProcess['pid'])
						currentProcess['execution'][1]=str(int(currentProcess['execution'][1])-1)
						currentProcess['executionTime']-=1

					if(int(currentProcess['execution'][1])==0):
						currentProcess['execution']=currentProcess['execution'][2:]
						if(len(currentProcess['execution'])>0): # i.e. process is not completed yet.
							if(currentProcess['execution'][0]=='I'): # will go for input
								# to complete current cycle of updateInput.
								updateInput(inputQueue, ready, inputRunning)
								inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
								updateOutput(outputQueue, ready, outputRunning)
							if(currentProcess['execution'][0]=='O'):
								# to complete current cycle of updateOutput.
								updateOutput(outputQueue, ready, outputRunning)
								outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
								updateInput(inputQueue, ready, inputRunning)
							# now another process will run on cpu.
							ready=updateReady(ready, processes, time)
							if(len(ready)>0):
								currentProcess=ready[0]
								if(currentProcess['startTime']==-1):
									currentProcess['startTime']=time
								del ready[0]
							else:
								currentProcess="none"
						else:
							currentProcess['endTime']=time
							endedProcess.append(currentProcess)
							updateInput(inputQueue, ready, inputRunning)
							updateOutput(outputQueue, ready, outputRunning)
							ready=updateReady(ready, processes, time)
							if(len(ready)>0):
								currentProcess=ready[0]
								if(currentProcess['startTime']==-1):
									currentProcess['startTime']=time
								del ready[0]
							else:
								currentProcess="none"
						continue
					

					else:
						updateInput(inputQueue, ready, inputRunning)
						updateOutput(outputQueue, ready, outputRunning)
						ready=updateReady(ready, processes, time)

						# check if there is any other process in ready queue which has lower arrival time than current process.
						# if(len(ready)>0 and currentProcess['priority']<ready[0]['priority']):
						# 	# cpuRunning.append(currentProcess['pid'])
						# 	ready.append(currentProcess)
						# 	currentProcess=ready[0]
						# 	if(currentProcess['startTime']==-1):
						# 		currentProcess['startTime']=time
						# 	del ready[0]
						continue
				else:
					cpuRunning.append('idle')
					if(currentProcess['execution'][0]=='I'): # will go for input
						# to complete current cycle of updateInput.
						updateInput(inputQueue, ready, inputRunning)
						inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
						updateOutput(outputQueue, ready, outputRunning)
					if(currentProcess['execution'][0]=='O'):
						# to complete current cycle of updateOutput.
						updateOutput(outputQueue, ready, outputRunning)
						outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
						updateInput(inputQueue, ready, inputRunning)
					# now another process will run on cpu.
					updateReady(ready, processes, time)
					if(len(ready)>0):
						currentProcess=ready[0]
						if(currentProcess['startTime']==-1):
							currentProcess['startTime']=time
						del ready[0]
					else:
						currentProcess="none"
					continue
		else:
			cpuRunning.append('idle')
			updateInput(inputQueue, ready, inputRunning)
			updateOutput(outputQueue, ready, outputRunning)
			ready=updateReady(ready, processes, time)

			if(len(ready)>0):
				currentProcess=ready[0]
				if(currentProcess['startTime']==-1):
					currentProcess['startTime']=time
				del ready[0]
			continue

	print(len(cpuRunning), len(inputRunning), len(outputRunning))
	print()
	for i in range(len(cpuRunning)):
		print(i, cpuRunning[i], inputRunning[i], outputRunning[i])

	print(len(endedProcess))
	for i in endedProcess:
		print(i)
		print()





if __name__=='__main__':
	n=int(input())
	quanta=int(input())
	processes=[]
	for i in range(n):
		processes.append({})
		process=input().split()
		processes[i]['pid']=int(process[0])
		processes[i]['priority']=int(process[1])
		processes[i]['arrivalTime']=int(process[2])
		processes[i]['execution']=process[3:len(process)-1]
		processes[i]['executionTime']=0
		processes[i]['startTime']=-1
		processes[i]['endTime']=-1
		processes[i]['totalBurst']=0
		j=4
		while(j<len(process)):
			if(process[j-1]=='P'):
				processes[i]['executionTime']+=int(process[j])
			processes[i]['totalBurst']+=int(process[j])
			j+=2
	for i in processes:
		print(i)
		print()
	print()
	SRTF(processes)