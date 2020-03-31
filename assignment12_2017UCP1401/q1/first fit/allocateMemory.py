def allocateMemory(process, memory):
	i = 0
	while(i<len(memory)):
		if(memory[i][1]-memory[i][0]+1 >= process.memSize):
			process.startMem = memory[i][0]
			process.endMem = memory[i][0]+process.memSize-1
			memory[i][0]=process.endMem+1
			if(memory[i][0]>=memory[i][1]):
				del memory[i]
			return True
		i+=1

	else:
		return False