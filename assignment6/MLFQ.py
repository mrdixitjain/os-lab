import operator
from updateOutput import *
from updateInput import *
def updateQueue0(queue, processes, time): # function to update ready[]. if any new process came, it'll be added to it and again it will be sorted on the basis of arrival time.
	while(len(processes)>0 and processes[0]['arrivalTime']<=time): # to check if there is any process whose arrival time is less than current time i.e it should be ready to execute.
		processes[0]['currentQueue']=0
		queue.processBuffer.append(processes[0])
		del processes[0]
	# ready=sorted(ready, key = lambda i: i['arrivalTime'])[:]

def isAllQueueEmpty(queues):
	for i in queues:
		if(len(i.processBuffer)>0):
			return False
	return True

def getNextProcessQueue(queues):
	for i in range(len(queues)):
		if(len(queues[i].processBuffer)>0):
			return i
	return -1

def printQueues(queues):
	for i in range(len(queues)):
		print(queues[i].processBuffer)
		print()

def upgradeQueues(queues):
	for i in range(len(queues)-1):
		while(len(queues[i+1].processBuffer)):
			queues[i+1].processBuffer[0]['quanta']=0
			queues[i+1].processBuffer[0]['currentQueue']-=1
			queues[i].processBuffer.append(queues[i+1].processBuffer[0])
			del queues[i+1].processBuffer[0]
	# print('upgraded')

def degradeQueues(queues):
	for i in range(len(queues)-1, -1, -1):
		while(len(queues[i-1].processBuffer)):
			queues[i-1].processBuffer[0]['quanta']=0
			queues[i-1].processBuffer[0]['currentQueue']+=1
			queues[i].processBuffer.append(queues[i-1].processBuffer[0])
			del queues[i-1].processBuffer[0]
	# print('degraded')

def getNextProcess(queues, time):
	n=getNextProcessQueue(queues)
	if(n>=0):
		currentProcess=queues[n].processBuffer[0]
		if(currentProcess['startTime']==-1):
			currentProcess['startTime']=time
		del queues[n].processBuffer[0]
	else:
		currentProcess="none"
	return currentProcess


def MLFQ(processes, queues, t1, t2):
	queues.sort(key=operator.attrgetter('priority'))
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

	endedProcess=[]# keep track of all processes which completed their execution.

	# all resources will stay idle till first process will arrive.
	if(processes[0]['arrivalTime']>0):
		for i in range(processes[0]['arrivalTime']):
			cpuRunning.append('idle')
			inputRunning.append('idle')
			outputRunning.append('idle')

	# first process will be process which arrived first
	# as we sorted processes on the basis of arrival time 
	# processes[0] will be first process to come

	currentProcess=processes[0]
	time = currentProcess['arrivalTime'] # it will keep track of time.
	if(currentProcess['startTime']==-1):
		currentProcess['startTime']=time
		currentProcess['currentQueue']=0
	del processes[0]
	upgradeTime=time
	degradeTime=time

	updateQueue0(queues[0], processes, time)

	while(currentProcess!="none" or isAllQueueEmpty(queues)==False or len(inputQueue)>0 or len(outputQueue)>0 or len(processes)>0):
		time+=1
		upgradeTime+=1
		degradeTime+=1
		updateInput(inputQueue, queues, inputRunning, time, endedProcess, outputQueue)
		updateOutput(outputQueue, queues, outputRunning, time, endedProcess, inputQueue)
		updateQueue0(queues[0], processes, time)
		if(currentProcess!="none"):
			if(currentProcess['execution'][0]=='P'): # i.e. it was working on cpu last.
				currentProcess['quanta']+=1
				if(int(currentProcess['execution'][1])>0):
					cpuRunning.append(currentProcess['pid'])
					currentProcess['execution'][1]=str(int(currentProcess['execution'][1])-1)
					currentProcess['executionTime']-=1

				if(int(currentProcess['execution'][1])==0): # if it's current execution on cpu is finished.
					currentProcess['execution']=currentProcess['execution'][2:]
					if(len(currentProcess['execution'])>0): # i.e. process is not completed yet.
						if(currentProcess['execution'][0]=='I'): # will go for input
							# to complete current cycle of updateInput.
							inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
						if(currentProcess['execution'][0]=='O'):
							# to complete current cycle of updateOutput.
							outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
						# now another process will run on cpu.
						currentProcess=getNextProcess(queues, time)
						
					
					else: # process is completed. Add it to endedProcess[] and check for new process to run on cpu
						currentProcess['endTime']=time
						endedProcess.append(currentProcess)

						# if there is a process to run on cpu than ok else currentProcess = "none"
						currentProcess=getNextProcess(queues, time)
						
				elif(currentProcess['quanta']>=queues[currentProcess['currentQueue']].quanta):
					if(currentProcess['currentQueue']<len(queues)-1):
						currentProcess['currentQueue']+=1
					currentProcess['quanta']=0
					queues[currentProcess['currentQueue']].processBuffer.append(currentProcess)
					currentProcess=getNextProcess(queues, time)
					
				else:
					n=getNextProcessQueue(queues)
					if(n>=0 and n<currentProcess['currentQueue']):
						queues[currentProcess['currentQueue']].processBuffer.insert(0, currentProcess)
						currentProcess=queues[n].processBuffer[0]
						if(currentProcess['startTime']==-1):
							currentProcess['startTime']=time
						del queues[n].processBuffer[0]

			else: # if current process is using input or output device
				cpuRunning.append('idle')
				if(currentProcess['execution'][0]=='I'): # will go for input
					# to complete current cycle of updateInput.
					inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
				if(currentProcess['execution'][0]=='O'):
					# to complete current cycle of updateOutput.
					outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
				# now another process will run on cpu if there is any.
				currentProcess=getNextProcess(queues, time)
				
		else: # check if there is any process ready to run.
			cpuRunning.append('idle')
			currentProcess=getNextProcess(queues, time)

		if(upgradeTime==t2):
			if(currentProcess!='none'):
				queues[currentProcess['currentQueue']].processBuffer.insert(0, currentProcess)
			upgradeQueues(queues)
			currentProcess=getNextProcess(queues, time)
			
			upgradeTime=0

		if(degradeTime==t1):
			if(currentProcess!='none'):
				queues[currentProcess['currentQueue']].processBuffer.insert(0, currentProcess)
			degradeQueues(queues)
			currentProcess=getNextProcess(queues, time)
			
			degradeTime=0

	# elif(degradeTime==t2):
	# 	degrade(queues)
	# print(len(cpuRunning), len(inputRunning), len(outputRunning))
	# print()
	# for i in range(len(cpuRunning)):
	# 	print(i, cpuRunning[i], inputRunning[i], outputRunning[i])
	return endedProcess






