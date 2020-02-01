from stride import *
from printOutput import *

if __name__=='__main__':
	file=open("lottery.dat", "r")
	data = file.readlines()
	totalTickets=int(data[0])
	n=int(data[1])
	tickets=[-1]*totalTickets
	processes= []
	number=int(data[2])
	current=0
	currentShare=0
	for i in range(n):
		process=data[i+3].split()
		a={}
		a['pid']=int(process[0])
		a['cpuShare']=float(process[1])
		a['execution']=process[2:len(process)-1]
		a['startTime']=-1
		a['endTime']=-1
		a['totalBurst']=0
		a['tickets']=0
		a['stride']=0
		currentShare+=a['cpuShare']
		a['pass']=0
		j=4
		while(j<len(process)):
			if(process[j-1]=='P'):
				a['totalBurst']+=int(process[j])
			j+=2
		processes.append(a)
	for i in processes:
		j=int((i['cpuShare']/currentShare)*totalTickets)
		i['tickets']=j
		i['stride']=int(number/i['tickets'])
	answer=Stride(processes, totalTickets, currentShare, number)
	printOutput(answer, "Stride")
