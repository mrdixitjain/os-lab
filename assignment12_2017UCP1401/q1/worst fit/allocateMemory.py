def allocateMemory(process, memory):
	i = 0
	output=[]
	while(i<len(memory)):
		if(memory[i][1]-memory[i][0]+1 >= process.memSize):
			output.append([memory[i][1]-memory[i][0]+1, i])
		i+=1
	if(len(output) > 0):
		k = max(output)
		i = k[1]
		process.startMem = memory[i][0]
		process.endMem = memory[i][0]+process.memSize-1
		memory[i][0]=process.endMem+1
		if(memory[i][0]>=memory[i][1]):
			del memory[i]
		return True

	else:
		return False