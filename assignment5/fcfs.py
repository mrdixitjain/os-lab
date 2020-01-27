def updateReady(ready, processes, time):
	while(len(processes)>0 and processes[0]['arrivalTime']<=time):
		ready.append(processes[0])
		del processes[0]
	ready=sorted(ready, key = lambda i: i['arrivalTime'])[:]
	return ready


def FCFS(processes):
	processes = sorted(processes, key = lambda i: i['arrivalTime'])[:]

	print(processes)
	print()

	if(processes[0]['arrivalTime']>0):
		print('0 - '+str(processes[0]['arrivalTime'])+' -> idle.')

	time=processes[0]['arrivalTime']

	print(str(time)+' - '+str(time+processes[0]['executionTime'])+' -> '+'P'+str(processes[0]['pid']))

	time+=processes[0]['executionTime']
	
	del processes[0]
	
	ready=[]
	ready=updateReady(ready, processes, time)
	i=0
	while(len(ready)>0 or len(processes)>0):
		if(len(ready)>0):
			print(str(time)+' - '+str(time+ready[0]['executionTime'])+' -> '+'P'+str(ready[0]['pid']))
			time+=ready[0]['executionTime']
			del ready[0]
		else:
			print(str(time)+' - '+str(processes[0]['arrivalTime'])+' -> idle.')
			time=processes[0]['arrivalTime']
		ready=updateReady(ready, processes, time)

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
			if(int(process[j])==-1):
				break
			processes[i]['executionTime']+=int(process[j])
			j+=2
	print()
	FCFS(processes)

