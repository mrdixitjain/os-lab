import random

def predict(index, pr, pages):
	farthest = 0
	l = 0
	i = 0
	while(i<len(pages)):
		for j in range(index+1, len(pr)):
			if(pages[i]==pr[j]):
				if(j>l):
					l = j
					farthest = i
				break
		if(l==0):
			return i
		i+=1
	return farthest

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
	k=0
	index = 0
	for i in lines[1]:
		if i in pages:
			hits+=1
		else: 
			miss+=1
			if(len(pages)<size):
				pages.append(i)
			else:
				k = predict(index, lines[1], pages)
				# print(k)
				pages[k] = i
		index+=1
		print(pages)
	print("total hits = " + str(hits))
	print("total miss = " + str(miss))
	print("hit ratio = " + str(hits/(miss+hits)))
