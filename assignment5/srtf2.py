# done by DIXIT KUMAR JAIN 
# on Jan 30 2020

from updateInput import *
from updateOutput import *

def updateReadySRTF(ready, processes, time): # function to update ready[]. if any new process came, it'll be added to it and again it will be sorted on the basis of arrival time.
	while(len(processes)>0 and processes[0]['arrivalTime']<=time): # to check if there is any process whose arrival time is less than current time i.e it should be ready to execute.
		ready.append(processes[0])
		del processes[0]
	ready=sorted(ready, key = lambda i: i['executionTime'])[:]
	return ready

def SRTF(processes): # main function which will implement SRTF scheduling process.
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

	# first process will be process which arrived first
	# as we sorted processes on the basis of arrival time 
	# processes[0] will be first process to come
	currentProcess=processes[0]
	time = currentProcess['arrivalTime']
	if(currentProcess['startTime']==-1):
		currentProcess['startTime']=time
	del processes[0]

	ready=[] # will hold those process which are in ready state.
	ready=updateReadySRTF(ready, processes, time)

	while(currentProcess!="none" or len(ready)>0 or len(processes)>0 or len(inputQueue)>0 or len(outputQueue)):
		time+=1
		updateInput(inputQueue, ready, inputRunning, time, endedProcess, outputQueue)
		updateOutput(outputQueue, ready, outputRunning, time, endedProcess, inputQueue)
		ready=updateReadySRTF(ready, processes, time)
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
						else:  # process is completed. Add it to endedProcess[] and check for new process to run on cpu
							currentProcess['endTime']=time
							endedProcess.append(currentProcess)
							# if there is a process to run on cpu than ok else currentProcess = "none"
							if(len(ready)>0):
								currentProcess=ready[0]
								if(currentProcess['startTime']==-1):
									currentProcess['startTime']=time
								del ready[0]
							else:
								currentProcess="none"
						continue
					

					else: # if there is another process on ready queue with shorter arrival time.

						# check if there is any other process in ready queue which has lower arrival time than current process.
						if(len(ready)>0 and currentProcess['executionTime']>ready[0]['executionTime']):
							# cpuRunning.append(currentProcess['pid'])
							ready.append(currentProcess)
							currentProcess=ready[0]
							if(currentProcess['startTime']==-1):
								currentProcess['startTime']=time
							del ready[0]
						continue
				else: # if current process is using input or output device
					cpuRunning.append('idle')
					if(currentProcess['execution'][0]=='I'): # will go for input
						# to complete current cycle of updateInput.
						inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
					if(currentProcess['execution'][0]=='O'):
						# to complete current cycle of updateOutput.
						outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
					# now another process will run on cpu if there is any.
					if(len(ready)>0):
						currentProcess=ready[0]
						if(currentProcess['startTime']==-1):
							currentProcess['startTime']=time
						del ready[0]
					else:
						currentProcess="none"
					continue
		else: # check if there is any process ready to run.
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

	# print(len(endedProcess))
	# for i in endedProcess:
	# 	print(i)
	# 	print()
	return endedProcess





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
	SRTF(processes)