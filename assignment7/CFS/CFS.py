from updateInput import *
from updateOutput import *
from printOutput import *

def getNewProcess(processes, time):
	currentProcess='none'
	if(len(processes)>0):
		currentProcess=processes[0]
		if(currentProcess['startTime']==-1):
			currentProcess['startTime']=time
		del processes[0]
	return currentProcess

def CFS(processes):
	proc=[]
	for i in processes:
		proc.append(i)
	processes=sorted(processes, key = lambda i : i['vruntime'])
	currRunTime=0
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
	time=0
	currentProcess='none'
	currentProcess=processes[0]
	del processes[0]
	if(currentProcess['startTime']==-1):
		currentProcess['startTime']=time

	while(currentProcess!='none' or len(processes)>0 or len(inputQueue)>0 or len(outputQueue)>0):
		# print("-> ", end="")
		# print(currentProcess)
		# print()
		# print(processes)
		# print()
		# print(inputQueue)
		# print()
		# print(outputQueue)
		# print()
		updateInput(inputQueue, processes, inputRunning, time, endedProcess, outputQueue)
		updateOutput(outputQueue, processes, outputRunning, time, endedProcess, inputQueue)
		processes=sorted(processes, key = lambda i : i['vruntime'])
		time+=1
		if(currentProcess!="none"):
			if(len(currentProcess['execution'])>0):
				if(currentProcess['execution'][0]=='P'): # i.e. it was working on cpu last.
					if(int(currentProcess['execution'][1])>0):
						cpuRunning.append(currentProcess['pid'])
						currentProcess['execution'][1]=str(int(currentProcess['execution'][1])-1)
						currRunTime+=1

					if(int(currentProcess['execution'][1])==0): # if it's current execution on cpu is finished.
						currentProcess['execution']=currentProcess['execution'][2:]
						if(len(currentProcess['execution'])>0): # i.e. process is not completed yet.
							if(currentProcess['execution'][0]=='I'): # will go for input
								currentProcess['vruntime']+=(1024/currentProcess['weight'])*currRunTime
								# to complete current cycle of updateInput.
								inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
							if(currentProcess['execution'][0]=='O'):
								# to complete current cycle of updateOutput.
								currentProcess['vruntime']+=(1024/currentProcess['weight'])*currRunTime
								outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
							# now another process will run on cpu.
							currRunTime=0
							currentProcess=getNewProcess(processes, time)
						
						else: # process is completed. Add it to endedProcess[] and check for new process to run on cpu
							currentProcess['endTime']=time
							endedProcess.append(currentProcess)

							# if there is a process to run on cpu than ok else currentProcess = "none"
							currRunTime=0
							currentProcess=getNewProcess(processes, time)
					elif(currRunTime>=currentProcess['slice']):
						currentProcess['vruntime']+=(1024/currentProcess['weight'])*currRunTime
						processes.append(currentProcess)
						processes=sorted(processes, key = lambda i : i['vruntime'])
						currRunTime=0
						currentProcess=getNewProcess(processes, time)

				else: # if current process is using input or output device
					cpuRunning.append('idle')
					currentProcess['vruntime']+=(1024/currentProcess['weight'])*currRunTime
					if(currentProcess['execution'][0]=='I'): # will go for input
						# to complete current cycle of updateInput.
						inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
					if(currentProcess['execution'][0]=='O'):
						# to complete current cycle of updateOutput.
						outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
					# now another process will run on cpu if there is any.
					currRunTime=0
					currentProcess=getNewProcess(processes, time)
		else: # check if there is any process processes to run.
			cpuRunning.append('idle')
			currRunTime=0
			currentProcess=getNewProcess(processes, time)
	# for i in range(len(cpuRunning)):
	# 	print(i, cpuRunning[i], inputRunning[i], outputRunning[i])
	return endedProcess

if __name__=="__main__":
	file = open('cfs.dat', 'r')
	data = file.readlines()
	schedLatency=int(data[0])
	minGranularity=int(data[1])
	weights=[88761, 71755, 56483, 46273, 36291, 29154, 23254, 18705, 14949, 11916, 9548, 7620, 6100, 4904, 3906, 3121, 2501, 1991, 1586, 1277,
	1024, 820, 655, 526, 423, 335, 272, 215, 172, 137, 110, 87, 70, 56, 45, 36, 29, 23, 18, 15]
	processes=[]
	totalWeight=0
	for i in range(2, len(data)):
		processes.append({})
		process=data[i].split()
		processes[i-2]['pid']=int(process[0])
		processes[i-2]['niceness']=int(process[1])
		processes[i-2]['weight']=weights[int(process[1])+20]
		totalWeight+=processes[i-2]['weight']
		processes[i-2]['execution']=process[2:len(process)-1]
		processes[i-2]['startTime']=-1
		processes[i-2]['endTime']=-1
		processes[i-2]['totalBurst']=0
		processes[i-2]['vruntime']=0
		j=3
		while(j<len(process)):
			if(process[j-1]=='P'):
				processes[i-2]['totalBurst']+=int(process[j])
			j+=2
	for i in processes:
		i['slice']=max((i['weight']/totalWeight)*schedLatency, minGranularity)
	answer=CFS(processes)
	printOutput(answer, "CFS")