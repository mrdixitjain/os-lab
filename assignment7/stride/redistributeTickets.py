def redistributeTickets(processes, currentShare, totalTickets, number):
	for i in processes:
		j=int((i['cpuShare']/currentShare)*totalTickets)
		i['tickets']=j
		i['stride']=int(number/i['tickets'])