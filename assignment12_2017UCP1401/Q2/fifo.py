import random
if __name__=="__main__" :
	file = open("reference.dat")
	lines_1 = file.readlines()
	lines = []
	for line in lines_1:
		lines.append(list(map(int, line.split())))
	
	size = lines[0][0]
	pages = []
	hits = 0
	miss = 0
	for i in lines[1]:
		if i in pages:
			hits+=1
		else: 
			miss+=1
			if(len(pages)<size):
				pages.append(i)
			else:
				del pages[0]
				pages.append(i)
		print(pages)
	print("total hits = " + str(hits))
	print("total miss = " + str(miss))
	print("hit ratio = " + str(hits/(miss+hits)))
