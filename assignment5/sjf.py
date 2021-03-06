# done by DIXIT KUMAR JAIN 
# on Jan 30 2020

def updateReady(ready, processes, time): # function to update ready[]. if any new process came, it'll be added to it and again it will be sorted on the basis of arrival time.
	while(len(processes)>0 and processes[0]['arrivalTime']<=time): # to check if there is any process whose arrival time is less than current time i.e it should be ready to execute.
		ready.append(processes[0])
		del processes[0]
	ready=sorted(ready, key = lambda i: i['executionTime'])[:]
	return ready


def updateInput(inputQueue, ready, inputRunning, time, endedProcess, outputQueue): # to update inputQueue[] i.e. to check if any process has done it's work on input devices or if not than decrease it's time by 1.
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
				if(inputQueue[0]['execution'][0]=='P'):
					ready.append(inputQueue[0])
				elif(inputQueue[0]['execution'][0]=='O'):
					outputQueue.append(inputQueue[0])
				else:
					inputQueue.append(inputQueue[0])
			else:
				outputQueue[0]['endTime']=time
				endedProcess.append(outputQueue[0])
			del inputQueue[0]


def updateOutput(outputQueue, ready, outputRunning, time, endedProcess, inputQueue): # to update oututQueue[] i.e. to check if any process has done 
	if(len(outputQueue)<=0): 											 # it's work on output devices or if not than decrease it's time by 1.
		outputRunning.append('idle')
		return
	# print(outputQueue[0]['execution'])
	if(int(outputQueue[0]['execution'][1])>0):
		outputRunning.append(outputQueue[0]['pid'])
		outputQueue[0]['execution'][1]=str(int(outputQueue[0]['execution'][1])-1)
		if(outputQueue[0]['execution'][1]=="0"):
			outputQueue[0]['execution']=outputQueue[0]['execution'][2:]
			if(len(outputQueue[0]['execution'])>0):
				if(outputQueue[0]['execution'][0]=='P'):
					ready.append(outputQueue[0])
				elif(outputQueue[0]['execution'][0]=='O'):
					outputQueue.append(outputQueue[0])
				else:
					inputQueue.append(outputQueue[0])
			else:
				outputQueue[0]['endTime']=time
				endedProcess.append(outputQueue[0])

			del outputQueue[0]


def SJFNonPreEmptive(processes):# main function which will implement FCFS scheduling process.
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
		updateInput(inputQueue, ready, inputRunning, time, endedProcess, outputQueue)
		updateOutput(outputQueue, ready, outputRunning, time, endedProcess, inputQueue)
		ready=updateReady(ready, processes, time)
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
								inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
							if(currentProcess['execution'][0]=='O'):
								# to complete current cycle of updateOutput.
								outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
							# now another process will run on cpu.
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
					if(currentProcess['execution'][0]=='I'): # will go for input
						# to complete current cycle of updateInput.
						inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
					if(currentProcess['execution'][0]=='O'):
						# to complete current cycle of updateOutput.
						outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
					# now another process will run on cpu.
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

			if(len(ready)>0):
				currentProcess=ready[0]
				if(currentProcess['startTime']==-1):
					currentProcess['startTime']=time
				del ready[0]
			continue

	# print(len(cpuRunning), len(inputRunning), len(outputRunning))
	# print()
	# for i in range(len(cpuRunning)):
	# 	print(i, cpuRunning[i], inputRunning[i], outputRunning[i])

	return endedProcess