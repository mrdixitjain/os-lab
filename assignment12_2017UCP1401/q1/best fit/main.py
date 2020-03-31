from proc import *
from printf import *
from updateAllocated import *
from freeMemory import *
from updateWaiting import *
from allocateMemory import *

if __name__ == "__main__":
	memory = []
	succReq = 0
	totalReq = 0
	maxMem = 0

	file = open("alloc.dat", "r");
	lines_1 = file.readlines();
	lines = []
	for line in lines_1:
		lines.append(list(map(int, line.split())))

	# print(lines[0:-1])

	memory.append([0, lines[0][0]*1000-1])
	maxMem = lines[0][0]*1000

	allocated = []
	# waiting = []
	processes = []

	for line in lines[1:-1]:
		processes.append(proc(line[0],line[2],line[1]))

	time = 0

	while(len(processes) > 0 or len(allocated) > 0 ):#or len(waiting) > 0):
		updateAllocated(allocated, memory)
		# updateWaiting(allocated, waiting, memory, succReq, totalReq)
		i = 0
		while(i<len(processes)):
			if(processes[i].arrivalTime > time):
				break
			totalReq += 1
			if(allocateMemory(processes[i], memory)):
				allocated.append(processes[i])
				processes.remove(processes[i])
				succReq += 1
				pass
			else:
				# waiting.append(process)
				# print(processes[i].arrivalTime, processes[i].maxTime, processes[i].memSize, processes[i].startMem, processes[i].endMem)
				# print("upper request is rejected due to low space.")
				del processes[i]
		time+=1
		if((time-1)%50==0):
			print("time = " + str(time - 1))
			if(totalReq>0):
				print("successful rate = " + str((succReq/totalReq)*100) +"%")

			else:
				print("no requsets made so far")
			print("external fragmentation : ")
			print(memory)
			print("free memory: ", end="")
			freeMem = 0
			for i in memory:
				freeMem += i[1]-i[0]+1
			print(freeMem, end="B, ")
			print((str((freeMem/maxMem)*100)) + "%")
			print()
			print()
		# print("time = " + str(time - 1))
		# print()
		# print("printing allocated")
		# printf(allocated)
		# print()
		# print()
		# # print("printing waiting")
		# # printf(waiting)
		# # print()
		# # print()
		# print("printing processes")
		# printf(processes)
		# print()
		# print()
		# print(memory)
		# print("==============================================================================================================")

