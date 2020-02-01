from MLFQ import *
from printOutPut import *

class queue:
	def __init__(self, quanta, priority):
		self.quanta=quanta
		self.priority=priority
		self.processBuffer=[]

if __name__=='__main__':
	file=open("MLFQ.dat", "r")
	data = file.readlines()
	q=int(data[0])
	quantas=list(map(int, data[1].split()))
	queues=[]
	for i in range(q):
		queues.append(queue(quantas[i-4], i))
	processes=[]
	t1=int(data[2])
	t2=int(data[3])
	for i in range(4, len(data)):
		process=data[i].split()
		processes.append({})
		processes[i-4]['pid']=int(process[0])
		processes[i-4]['priority']=int(process[1])
		processes[i-4]['arrivalTime']=int(process[2])
		processes[i-4]['execution']=process[3:len(process)-1]
		processes[i-4]['startTime']=-1
		processes[i-4]['endTime']=-1
		processes[i-4]['totalBurst']=0
		processes[i-4]['currentQueue']=-1
		processes[i-4]['degradeTime']=0
		processes[i-4]['quanta']=0
		j=4
		while(j<len(process)):
			if(process[j-1]=='P'):
				processes[i-4]['totalBurst']+=int(process[j])
			j+=2
	# for i in processes:
	# 	print(i)
	answer=MLFQ(processes, queues, t1, t2)
	printOutput(answer, "MLFQ")
	print()
		
		