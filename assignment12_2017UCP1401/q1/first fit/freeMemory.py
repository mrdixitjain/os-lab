def freeMemory(process, memory):
	s = process.startMem
	e = process.endMem
	i = 0

	if(len(memory)==0):
		memory.append([s, e])
		return

	# if chunk is from end of the memory
	if(memory[-1][1] < s):
		if(memory[-1][1]==s-1):
			memory[-1][1] = e
		else:
			memory.append([s, e])

	# if chunk belongs to start of the memory
	elif(memory[0][0]>e):
		if(memory[0][0]==e+1):
			memory[0][0] = s
		else:
			memory.insert(0, [s, e])

	# if chunk resides somewhere in-middle
	else:
		i = 0
		while(i<len(memory)):		
			if(memory[i][0]>e):
				# print(s, e, i)
				if(memory[i][0]==e+1):
					memory[i][0] = s
					if(memory[i-1][1]==s-1):
						memory[i-1][1] = memory[i][1]
						del memory[i]
					return

				
				if(memory[i-1][1]==s-1):
					memory[i-1][1] = e
					return
				
				memory.insert(i, [s, e])
				return
			i+=1
	return