def updateReady(ready, processes, time):
	while(len(processes)>0 and processes[0]['arrivalTime']<=time):
		ready.append(processes[0])
		del processes[0]
	ready=sorted(ready, key = lambda i: i['executionTime'])[:]

	
	return ready

def SRTF(processes):
	currExecutionTime=0
	currStartTime=0

	processes = sorted(processes, key = lambda i: i['arrivalTime'])[:]
	
	if(processes[0]['arrivalTime']>0):
		print('0 - '+str(processes[0]['arrivalTime'])+' -> idle.')
		print()

	time=processes[0]['arrivalTime']
	ready=[]
	ready=updateReady(ready, processes, time)
	currentProcess=ready[0]
	currStartTime=time
	currExecutionTime=currentProcess['executionTime']
	del ready[0]
	# print(currentProcess)
	# print()
	i=0
	while(len(ready)>0 or len(processes)>0):
		time+=1
		currentProcess['executionTime']-=1
		currExecutionTime-=1
		ready=updateReady(ready, processes, time)
		# print(currentProcess)
		# print()
		if(currExecutionTime<=0):
			print(str(currStartTime)+' - '+str(time)+' -> '+'P'+str(currentProcess['pid']))
			print()
			if(len(ready)>0):
				currentProcess=ready[0]
				currStartTime=time
				currExecutionTime=currentProcess['executionTime']
				del ready[0]
			elif(len(processes)>0):
				print(str(time)+' - '+str(time+processes[0]['arrivalTime'])+' -> idle.')
				print()
				time=processes[0]['arrivalTime']
				currentProcess=processes[0]
				currStartTime=time
				currExecutionTime=currentProcess['executionTime']
				del processes[0]
			else:
				break

		if(len(ready)>0):
			if(ready[0]['executionTime']<currExecutionTime):
				print(str(currStartTime)+' - '+str(time)+' -> '+'P'+str(currentProcess['pid']))
				print()
				ready.append(currentProcess)
				currentProcess=ready[0]
				del ready[0]
				currExecutionTime=currentProcess['executionTime']
				currStartTime=time

		# elif(len(processes)>0):
		# 	print(str(time)+' - '+str(time+processes[0]['arrivalTime'])+' -> idle.')
		# 	time=processes[0]['arrivalTime']
		# else:
		# 	break
	print(str(currStartTime)+' - '+str(time+currExecutionTime)+' -> '+'P'+str(currentProcess['pid']))


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
	SRTF(processes)
