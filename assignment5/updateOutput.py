def updateOutput(outputQueue, ready, outputRunning, time, endedProcess, inputQueue): # to update outputQueue[] i.e. to check if any process has done it's work on output devices or if not than decrease it's time by 1.
	if(len(outputQueue)<=0):
		outputRunning.append('idle')
		return
	# print(ioQueue[0]['execution'])
	if(int(outputQueue[0]['execution'][1])>0):
		outputRunning.append(outputQueue[0]['pid'])
		outputQueue[0]['execution'][1]=str(int(outputQueue[0]['execution'][1])-1)
		if(outputQueue[0]['execution'][1]=="0"):
			outputQueue[0]['execution']=outputQueue[0]['execution'][2:]
			if(len(outputQueue[0]['execution'])>0):
				if(outputQueue[0]['execution'][0]=='P'):
					ready.append(outputQueue[0])
				elif(outputQueue[0]['execution'][0]=='O'):
					outputQueue.append(outputQueue[0])
				else:
					inputQueue.append(outputQueue[0])
			else:
				outputQueue[0]['endTime']=time
				endedProcess.append(outputQueue[0])
			del outputQueue[0]

