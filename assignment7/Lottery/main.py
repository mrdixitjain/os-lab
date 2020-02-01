from lotteryScheduling import *
from printOutput import *
if __name__=='__main__':
	file=open("lottery.dat", "r")
	data = file.readlines()
	totalTickets=int(data[0])
	n=int(data[1])
	tickets=[-1]*totalTickets
	processes=[]
	current=0
	currentShare=0
	for i in range(n):
		process=data[i+2].split()
		processes.append({})
		processes[i]['pid']=int(process[0])
		processes[i]['cpuShare']=float(process[1])
		processes[i]['execution']=process[2:len(process)-1]
		processes[i]['startTime']=-1
		processes[i]['endTime']=-1
		processes[i]['totalBurst']=0
		currentShare+=processes[i]['cpuShare']
		j=4
		while(j<len(process)):
			if(process[j-1]=='P'):
				processes[i]['totalBurst']+=int(process[j])
			j+=2

	for i in processes:
		j=int((i['cpuShare']/currentShare)*totalTickets)
		i['tickets']=j
		for k in range(j):
			tickets[k+current]=i['pid']
		current+=j
	answer=Lottery(processes, tickets, currentShare)
	printOutput(answer, 'Lottery')
