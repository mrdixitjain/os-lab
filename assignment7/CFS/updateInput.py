def updateInput(inputQueue, processes, inputRunning, time, endedProcess, outputQueue): # to update inputQueue[] i.e. to check if any process has done it's work on input devices or if not than decrease it's time by 1.
	if(len(inputQueue)<=0):
		inputRunning.append('idle')
		return
	# print(ioQueue[0]['execution'])
	
	if(int(inputQueue[0]['execution'][1])>0):
		inputRunning.append(inputQueue[0]['pid'])
		inputQueue[0]['execution'][1]=str(int(inputQueue[0]['execution'][1])-1)
		if(inputQueue[0]['execution'][1]=="0"):
			inputQueue[0]['execution']=inputQueue[0]['execution'][2:]
			if(len(inputQueue[0]['execution'])>0):
				if(inputQueue[0]['execution'][0]=='P'):
					if(len(processes)>0):
						inputQueue[0]['vruntime']=processes[0]['vruntime']
					processes.append(inputQueue[0])
				elif(inputQueue[0]['execution'][0]=='O'):
					outputQueue.append(inputQueue[0])
				else:
					inputQueue.append(inputQueue[0])
			else:
				inputQueue[0]['endTime']=time
				endedProcess.append(inputQueue[0])
			del inputQueue[0]

