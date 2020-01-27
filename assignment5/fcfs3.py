def updateReady(ready, processes, time): # function to update ready[]. if any new process came, it'll be added to it and again it will be sorted on the basis of arrival time.
	while(len(processes)>0 and processes[0]['arrivalTime']<=time): # to check if there is any process whose arrival time is less than current time i.e it should be ready to execute.
		ready.append(processes[0])
		del processes[0]
	ready=sorted(ready, key = lambda i: i['arrivalTime'])[:]
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


def updateCurrentProcess(currentProcess, ready, inputQueue, outputQueue, inputRunning, outputRunning, cpuRunning, time):
	if(currentProcess!="none" and len(currentProcess['execution'])>0):
		if(currentProcess['execution'][0]=='P'):
			if(int(currentProcess['execution'][1])>0):
				pass
			else:
				currentProcess['execution']=currentProcess['execution'][2:]
				if(len(currentProcess['execution'])>0): # i.e. process is not completed yet.
					if(currentProcess['execution'][0]=='I'): # will go for input

						# to complete current cycle of updateInput.
						if(len(inputQueue)>0):
							updateInput(inputQueue, ready, inputRunning)
						else:
							inputRunning.append('idle')
						inputQueue.append(currentProcess)
						updateOutput(outputQueue, ready, outputRunning) # process added to inputQueue where it'll wait for it's turn.
					if(currentProcess['execution'][0]=='O'):
						# to complete current cycle of updateOutput.
						if(len(outputQueue)>0):
							updateOutput(outputQueue, ready, outputRunning)
						else:
							outputRunning.append('idle') 
						outputQueue.append(currentProcess)
						updateInput(inputQueue, ready, inputRunning) # process added to outputQueue where it'll wait for it's turn.
					# now another process will run on cpu.
					if(len(ready)>0):
						currentProcess=ready[0]
						del ready[0]
					else:
						cpuRunning.append('idle')
						currentProcess="none"
				else:
					if(len(ready)>0):
						currentProcess=ready[0]
						del ready[0]
					else:
						cpuRunning.append('idle')
						updateInput(inputQueue, ready, inputRunning)
						updateOutput(outputQueue, ready, outputRunning)
						currentProcess="none"
	else:
		if(len(ready)>0):
			currentProcess=ready[0]
			del ready[0]
		else:
			cpuRunning.append('idle')
			updateInput(inputQueue, ready, inputRunning)
			updateOutput(outputQueue, ready, outputRunning)
			currentProcess="none"
	ready=updateReady(ready, processes, time)
	# check if there is any other process in ready queue which has lower arrival time than current process.
	if(currentProcess=="none" and len(ready)>0):
		currentProcess=ready[0]
		del ready[0]
	if(len(ready)>0 and currentProcess['arrivalTime']>ready[0]['arrivalTime']):
		# cpuRunning.append(currentProcess['pid'])
		ready.append(currentProcess)
		currentProcess=ready[0]
		del ready[0]
	return currentProcess


def FCFS(processes): # main function which will implement FCFS scheduling process.
	prcs=processes[:]
	
	#sorted processes on the basis of arrival time
	processes = sorted(processes, key = lambda i: i['arrivalTime'])[:]

	# to store processes executing or waiting for input output devices
	inputQueue=[]
	outputQueue=[]

	# to keep track of processes running on cpu, input and output device.
	# here, index will work as time unit.
	cpuRunning=[]
	inputRunning=[]
	outputRunning=[]

	# all resources will stay idle till first process will arrive.
	if(processes[0]['arrivalTime']>0):
		for i in range(processes[0]['arrivalTime']):
			cpuRunning.append('idle')
			inputRunning.append('idle')
			outputRunning.append('idle')
		# print('0 - '+str(processes[0]['arrivalTime'])+' -> idle.')

	time=processes[0]['arrivalTime']

	currentProcess=processes[0] # currentProcess will hold process being run on cpu currently.
	del processes[0]
	
	# keep those process which are ready to be executed
	# it is also sorted on the basis of arrival time of process.
	ready=[]
	ready=updateReady(ready, processes, time)
	i=0
	while(currentProcess!="none" or len(ready)>0 or len(processes)>0 or len(inputQueue)>0 or len(outputQueue)):
		# print(currentProcess)
		time+=1
		print("->  ", end=" ")
		print(currentProcess)
		print()
		print(inputQueue)
		print()
		print(outputQueue)
		print()
		print(ready)
		print()
		print()

		if(currentProcess!="none"):
			if(len(currentProcess['execution'])>0 and currentProcess['execution'][0]=='P'): # i.e. it was working on cpu last.
				if(int(currentProcess['execution'][1])>0): # i.e. it's work on cpu is remaining.
					cpuRunning.append(currentProcess['pid'])
					currentProcess['execution'][1]=str(int(currentProcess['execution'][1])-1)
					currentProcess['executionTime']-=1
					pid=currentProcess['pid']
					currentProcess=updateCurrentProcess(currentProcess, ready, inputQueue, outputQueue, inputRunning, outputRunning, cpuRunning, time)
					# print(currentProcess['pid'], pid)
					if(currentProcess!="none" and currentProcess['pid']==pid):
						pass
					else:
						continue
			else:
				pid=currentProcess['pid']
				currentProcess=updateCurrentProcess(currentProcess, ready, inputQueue, outputQueue, inputRunning, outputRunning, cpuRunning, time)
				# print(currentProcess['pid'], pid)
				if(currentProcess!="none" and currentProcess['pid']==pid):
					pass
				else:
					continue
		else: # if current process is none that means that cpu will be idle.
			cpuRunning.append('idle')

		updateInput(inputQueue, ready, inputRunning)
		updateOutput(outputQueue, ready, outputRunning)

		# check if there is any other process in ready queue which has lower arrival time than current process.
		currentProcess=updateCurrentProcess(currentProcess, ready, inputQueue, outputQueue, inputRunning, outputRunning, cpuRunning, time)

	print(len(cpuRunning), len(inputRunning), len(outputRunning))
	print()
	for i in range(len(cpuRunning)):
		print(i, cpuRunning[i], inputRunning[i], outputRunning[i])





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
		j=4
		while(j<len(process)):
			if(process[j-1]=='P'):
				processes[i]['executionTime']+=int(process[j])
			j+=2
	print()
	FCFS(processes)