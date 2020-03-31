def allocateMemory(process, memory, n):
	n = n%len(memory)
	i = n
	# print(n)
	if(i == 0):
		n = len(memory)+1
	t = max(len(memory), n)
	# print(t==n)
	while(i!=n-1):
		if(memory[i][1]-memory[i][0]+1 >= process.memSize):
			process.startMem = memory[i][0]
			process.endMem = memory[i][0]+process.memSize-1
			memory[i][0]=process.endMem+1
			if(memory[i][0]>=memory[i][1]):
				del memory[i]
			n = i
			return [True, n]
		i+=1
		i%=t

	else:
		return [False, n]