# done by DIXIT KUMAR JAIN 
# on Jan 30 2020

from updateInput import *
from updateOutput import *

def updateReadyPPE(ready, processes, time): # function to update ready[]. if any new process came, it'll be added to it and again it will be sorted on the basis of arrival time.
	while(len(processes)>0 and processes[0]['arrivalTime']<=time): # to check if there is any process whose arrival time is less than current time i.e it should be ready to execute.
		ready.append(processes[0])
		del processes[0]
	ready=sorted(ready, key = lambda i: i['priority'], reverse=True)[:]
	return ready

def PriorityPreEmptive(processes):
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
	ready=updateReadyPPE(ready, processes, time)

	while(currentProcess!="none" or len(ready)>0 or len(processes)>0 or len(inputQueue)>0 or len(outputQueue)):
		time+=1
		updateInput(inputQueue, ready, inputRunning, time, endedProcess, outputQueue)
		updateOutput(outputQueue, ready, outputRunning, time, endedProcess, inputQueue)
		ready=updateReadyPPE(ready, processes, time)
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
						# check if there is any other process in ready queue which has lower arrival time than current process.
						if(len(ready)>0 and currentProcess['priority']<ready[0]['priority']):
							# cpuRunning.append(currentProcess['pid'])
							ready.append(currentProcess)
							currentProcess=ready[0]
							if(currentProcess['startTime']==-1):
								currentProcess['startTime']=time
							del ready[0]
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

