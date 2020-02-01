def redistributeTickets(processes, tickets, currentShare):
	current=0
	for i in processes:
		j=int((i['cpuShare']/currentShare)*len(tickets))
		i['tickets']=j
		for k in range(j):
			tickets[k+current]=i['pid']
		current+=j

