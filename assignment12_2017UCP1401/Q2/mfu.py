import random
class page :
	def __init__(self, value) :
		self.value = value
		self.freq = 0

def printf(pages):
	print("[", end="")
	for i in pages:
		print("(", end=" ")
		print(i.value, i.freq, end=" ")
		print("),", end=" ")
	print("]")

if __name__=="__main__" :
	file = open("reference.dat")
	lines = file.readlines()
	lines_1 = []
	for line in lines:
		lines_1.append(list(map(int, line.split())))
	
	size = lines_1[0][0]
	lines = []
	for i in lines_1[1]:
		lines.append(page(i))
	pages = []
	hits = 0
	miss = 0
	find = False
	for i in lines:
		# print(i)
		find = False
		for k in pages:
			if(k.value==i.value):
				find = True
				hits+=1
				k.freq += 1
				break
		if(not find): 
			miss+=1
			if(len(pages)<size):
				pages.append(i)
			else:
				max1 = 0
				j = 1
				while(j<size):
					if(pages[max1].freq < pages[j].freq):
						max1 = j
					j+=1
				if(max1 == 0):
					del pages[max1]
					pages.append(i)
				else:
					pages[max1] = i
		printf(pages)
	print("total hits = " + str(hits))
	print("total miss = " + str(miss))
	print("hit ratio = " + str(hits/(miss+hits)))
