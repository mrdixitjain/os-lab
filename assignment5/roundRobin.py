# done by DIXIT KUMAR JAIN 
# on Jan 30 2020

from updateInput import *
from updateOutput import *
from getNewProcess import *

def updateReadyRR(ready, processes, time): # function to update ready[]. if any new process came, it'll be added to it and again it will be sorted on the basis of arrival time.
	while(len(processes)>0 and processes[0]['arrivalTime']<=time): # to check if there is any process whose arrival time is less than current time i.e it should be ready to execute.
		ready.append(processes[0])
		del processes[0]
	# ready=sorted(ready, key = lambda i: i['arrivalTime'])[:]
	return ready

def RoundRobin(processes, quanta):# main function which will implement FCFS scheduling process.
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
	del processes[0]
	currentQuanta=0

	ready=[] # will hold those process which are in ready state.
	ready=updateReadyRR(ready, processes, time)

	while(currentProcess!="none" or len(ready)>0 or len(processes)>0 or len(inputQueue)>0 or len(outputQueue)):
		time+=1

		updateInput(inputQueue, ready, inputRunning, time, endedProcess, outputQueue)
		updateOutput(outputQueue, ready, outputRunning, time, endedProcess, inputQueue)
		ready=updateReadyRR(ready, processes, time)



		if(currentProcess!="none" and currentQuanta<quanta):
			currentQuanta+=1
			if(len(currentProcess['execution'])>0):
				if(currentProcess['execution'][0]=='P'): # i.e. it was working on cpu last.
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
							currentProcess=getNewProcess(ready, time)
							currentQuanta=0
							continue
					
						else: # process is completed. Add it to endedProcess[] and check for new process to run on cpu
							currentProcess['endTime']=time
							endedProcess.append(currentProcess)

							# if there is a process to run on cpu than ok else currentProcess = "none"
							currentProcess=getNewProcess(ready, time)
							currentQuanta=0
						continue
				

					elif(currentQuanta==quanta): # if there is another process on ready queue with shorter arrival time.
						ready.append(currentProcess)


						# check if there is any other process in ready queue which has lower arrival time than current process.
						currentProcess=getNewProcess(ready, time)
						currentQuanta=0
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
					currentProcess=getNewProcess(ready, time)
					currentQuanta=0
					continue
		else: # check if there is any process ready to run.
			cpuRunning.append('idle')

			currentProcess=getNewProcess(ready, time)
			currentQuanta=0
			continue


	return endedProcess