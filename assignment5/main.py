from fcfsn import *
from sjfNonPreEmptive import *
from priorityNonPreemptive import *
from priorityPreemptive import *
from srtf2 import *
from printOutPut import *
from roundRobin import *

if __name__=='__main__':
	file=open("input.dat", "r")
	data = file.readlines()
	n=int(data[0])
	quanta=int(data[1])
	processes0=[]
	processes1=[]
	processes2=[]
	processes3=[]
	processes4=[]
	processes5=[]
	for i in range(n):
		process=data[i+2].split()
		processes0.append({})
		processes0[i]['pid']=int(process[0])
		processes0[i]['priority']=int(process[1])
		processes0[i]['arrivalTime']=int(process[2])
		processes0[i]['execution']=process[3:len(process)-1]
		processes0[i]['executionTime']=0
		processes0[i]['startTime']=-1
		processes0[i]['endTime']=-1
		processes0[i]['totalBurst']=0
		j=4
		while(j<len(process)):
			if(process[j-1]=='P'):
				processes0[i]['executionTime']+=int(process[j])
			processes0[i]['totalBurst']+=int(process[j])
			j+=2
		processes1.append({})
		processes1[i]['pid']=int(process[0])
		processes1[i]['priority']=int(process[1])
		processes1[i]['arrivalTime']=int(process[2])
		processes1[i]['execution']=process[3:len(process)-1]
		processes1[i]['executionTime']=0
		processes1[i]['startTime']=-1
		processes1[i]['endTime']=-1
		processes1[i]['totalBurst']=0
		j=4
		while(j<len(process)):
			if(process[j-1]=='P'):
				processes1[i]['executionTime']+=int(process[j])
			processes1[i]['totalBurst']+=int(process[j])
			j+=2
		processes2.append({})
		processes2[i]['pid']=int(process[0])
		processes2[i]['priority']=int(process[1])
		processes2[i]['arrivalTime']=int(process[2])
		processes2[i]['execution']=process[3:len(process)-1]
		processes2[i]['executionTime']=0
		processes2[i]['startTime']=-1
		processes2[i]['endTime']=-1
		processes2[i]['totalBurst']=0
		j=4
		while(j<len(process)):
			if(process[j-1]=='P'):
				processes2[i]['executionTime']+=int(process[j])
			processes2[i]['totalBurst']+=int(process[j])
			j+=2
		processes3.append({})
		processes3[i]['pid']=int(process[0])
		processes3[i]['priority']=int(process[1])
		processes3[i]['arrivalTime']=int(process[2])
		processes3[i]['execution']=process[3:len(process)-1]
		processes3[i]['executionTime']=0
		processes3[i]['startTime']=-1
		processes3[i]['endTime']=-1
		processes3[i]['totalBurst']=0
		j=4
		while(j<len(process)):
			if(process[j-1]=='P'):
				processes3[i]['executionTime']+=int(process[j])
			processes3[i]['totalBurst']+=int(process[j])
			j+=2
		processes4.append({})
		processes4[i]['pid']=int(process[0])
		processes4[i]['priority']=int(process[1])
		processes4[i]['arrivalTime']=int(process[2])
		processes4[i]['execution']=process[3:len(process)-1]
		processes4[i]['executionTime']=0
		processes4[i]['startTime']=-1
		processes4[i]['endTime']=-1
		processes4[i]['totalBurst']=0
		j=4
		while(j<len(process)):
			if(process[j-1]=='P'):
				processes4[i]['executionTime']+=int(process[j])
			processes4[i]['totalBurst']+=int(process[j])
			j+=2
		processes5.append({})
		processes5[i]['pid']=int(process[0])
		processes5[i]['priority']=int(process[1])
		processes5[i]['arrivalTime']=int(process[2])
		processes5[i]['execution']=process[3:len(process)-1]
		processes5[i]['executionTime']=0
		processes5[i]['startTime']=-1
		processes5[i]['endTime']=-1
		processes5[i]['totalBurst']=0
		j=4
		while(j<len(process)):
			if(process[j-1]=='P'):
				processes5[i]['executionTime']+=int(process[j])
			processes5[i]['totalBurst']+=int(process[j])
			j+=2
	for i in processes0:
		print(i)
	answer=FCFS(processes0)
	printOutput(answer, "FCFS")
	print()
	answer=SJFNonPreEmptive(processes1)
	printOutput(answer, "SJFNonPreEmptive")
	print()
	answer=SRTF(processes2)
	printOutput(answer, "SRTF")
	print()
	answer=PriorityPreEmptive(processes3)
	printOutput(answer, "PriorityPreEmptive")
	print()
	answer=PriorityNonPreEmptive(processes4)
	printOutput(answer, "PriorityNonPreEmptive")
	print()
	answer=RoundRobin(processes5, quanta)
	printOutput(answer, "Round Robin")
	print()

# from fcfsn import *
# from sjfNonPreEmptive import *
# from priorityNonPreemptive import *
# from priorityPreemptive import *
# from srtf2 import *
# from printOutPut import *
# from roundRobin import *

# if __name__=='__main__':
# 	file=open("input.dat", "r")
# 	data = file.readlines()
# 	n=int(data[0])
# 	quanta=int(data[1])
# 	processes=[]
# 	for i in range(n):
# 		processes.append({})
# 		process=data[i+2].split()
# 		processes[i]['pid']=int(process[0])
# 		processes[i]['priority']=int(process[1])
# 		processes[i]['arrivalTime']=int(process[2])
# 		processes[i]['execution']=process[3:len(process)-1]
# 		processes[i]['executionTime']=0
# 		processes[i]['startTime']=-1
# 		processes[i]['endTime']=-1
# 		processes[i]['totalBurst']=0
# 		j=4
# 		while(j<len(process)):
# 			if(process[j-1]=='P'):
# 				processes[i]['executionTime']+=int(process[j])
# 			processes[i]['totalBurst']+=int(process[j])
# 			j+=2
# 	# for i in processes:
# 	# 	print(i)
# 	answer=FCFS(processes)
# 	printOutput(answer, "FCFS")
# 	print()
# 	answer=SJFNonPreEmptive(processes)
# 	printOutput(answer, "SJFNonPreEmptive")
# 	print()
# 	answer=SRTF(processes)
# 	printOutput(answer, "SRTF")
# 	print()
# 	answer=PriorityPreEmptive(processes)
# 	printOutput(answer, "PriorityPreEmptive")
# 	print()
# 	answer=PriorityNonPreEmptive(processes)
# 	printOutput(answer, "PriorityNonPreEmptive")
# 	print()
# 	answer=RoundRobin(processes, quanta)
# 	printOutput(answer, "Round Robin")
# 	print()
		
		