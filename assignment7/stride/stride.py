# done by DIXIT KUMAR JAIN 
# on Jan 30 2020

from updateInput import *
from updateOutput import *
from main import *

def Stride(processes, totalTickets, currentShare, number):# main function which will implement FCFS scheduling process.
	prcs=processes[:]
	
	# to store processes executing or waiting for input output devices
	inputQueue=[]
	outputQueue=[]

	# to keep track of processes running on cpu, input and output device.
	# here, index will work as time unit.
	cpuRunning=[]
	inputRunning=[]
	outputRunning=[]

	endedProcess=[]# keep track of all processes which completed their execution.

	# first process will be process which arrived first
	# as we sorted processes on the basis of arrival time 
	# processes[0] will be first process to come

	currentProcess='none'
	time=0

	while(currentProcess!="none" or len(processes)>0 or len(inputQueue)>0 or len(outputQueue)):
		currentProcess='none'
		if(len(processes)>0):
			processes=sorted(processes, key = lambda i : i['pass'])[:]
			currentProcess=processes[0]
			if(currentProcess['startTime']==-1):
				currentProcess['startTime']=time
			del processes[0]
		# print('->', end=" ")
		# print(currentProcess)
		# print()
		# print(processes)
		# print()
		# print(inputQueue)
		# print()
		# print(outputQueue)
		# print()
		time+=1
		# currentProcess='none'
		# if(len(processes)>0):
		# 	processes=sorted(processes, key = lambda i : i['pass'])[:]
		# 	currentProcess=processes[0]
		# 	if(currentProcess['startTime']==-1):
		# 		currentProcess['startTime']=time
		# 	del processes[0]
		currentShare=updateInput(inputQueue, processes, inputRunning, time, endedProcess, outputQueue, currentShare, totalTickets, number)
		currentShare=updateOutput(outputQueue, processes, outputRunning, time, endedProcess, inputQueue, currentShare, totalTickets, number)

		if(currentProcess!="none"):
			if(len(currentProcess['execution'])>0):
				if(currentProcess['execution'][0]=='P'): # i.e. it was working on cpu last.
					if(int(currentProcess['execution'][1])>0):
						cpuRunning.append(currentProcess['pid'])
						currentProcess['execution'][1]=str(int(currentProcess['execution'][1])-1)
						currentProcess['pass']+=currentProcess['stride']


					if(int(currentProcess['execution'][1])==0): # if it's current execution on cpu is finished.
						currentProcess['execution']=currentProcess['execution'][2:]
						if(len(currentProcess['execution'])>0): # i.e. process is not completed yet.
							if(currentProcess['execution'][0]=='I'): # will go for input
								# to complete current cycle of updateInput.
								currentShare-=currentProcess['cpuShare']
								redistributeTickets(processes, currentShare, totalTickets, number)
								inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
							if(currentProcess['execution'][0]=='O'):
								# to complete current cycle of updateOutput.
								currentShare-=currentProcess['cpuShare']
								redistributeTickets(processes, currentShare, totalTickets, number)
								outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
							# now another process will run on cpu.
						
						else: # process is completed. Add it to endedProcess[] and check for new process to run on cpu
							currentProcess['endTime']=time
							currentShare-=currentProcess['cpuShare']
							redistributeTickets(processes, currentShare, totalTickets, number)

							endedProcess.append(currentProcess)
					else:
						processes.append(currentProcess)			

				else: # if current process is using input or output device
					cpuRunning.append('idle')
					if(currentProcess['execution'][0]=='I'): # will go for input
						# to complete current cycle of updateInput.
						currentShare-=currentProcess['cpuShare']
						redistributeTickets(processes, currentShare, totalTickets, number)
						inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
					if(currentProcess['execution'][0]=='O'):
						# to complete current cycle of updateOutput.
						currentShare-=currentProcess['cpuShare']
						redistributeTickets(processes, currentShare, totalTickets, number)
						outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.

		else: # check if there is any process ready to run.
			cpuRunning.append('idle')

	# print(len(cpuRunning), len(inputRunning), len(outputRunning))
	# # print()
	# for i in range(len(cpuRunning)):
	# 	print(i, cpuRunning[i], inputRunning[i], outputRunning[i])

	return endedProcess

