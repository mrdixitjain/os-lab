def find(char,keyMat):
	for x in range(6):
		for y in range(6):
			if char == keyMat[x][y]:
				return x,y

def encryptPF(plainText,key):
	plainText.replace(" ","")
	alphaSet = 'abcdefghijklmnopqrstuvwxyz1234567890'
	if(len(plainText) % 2 == 1):
		plainText += 'z'
		print(plainText)
	#generate key matrix
	temp = ''
	for i in key:
		if i not in temp :
			temp += i

	for i in alphaSet:
		if i not in temp :
			temp += i
	
	keyMat = [['a' for i in range(6)] for j in range(6) ]
	i  = 0 
	for x in range(6):
		for y in range(6): 
			keyMat[x][y] = temp[i]
			i += 1
	# print(keyMat)


	# Dividing plaintext into length of 2 
	chunks = len(plainText)
	chunk_size = 2
	text = [plainText[i:i+chunk_size] for i in range(0, chunks, chunk_size)]

	# print(text)

	#ciphering
	res = ''
	for i in text:
		x1,y1 = find(i[0],keyMat)
		x2,y2 = find(i[1],keyMat)

		if y1 == y2:
			x1 = (x1 + 1)%6
			x2 = (x2 + 1)%6
			res += keyMat[x1][y1] + keyMat[x2][y2]
		elif x1 == x2:
			y1 = (y1 + 1)%6
			y2 = (y2 + 1)%6
			res += keyMat[x1][y1] + keyMat[x2][y2]
		else:
			res += keyMat[x1][y2] + keyMat[x2][y1]

	return res




if  __name__ == "__main__":

	print(encryptPF("rahu827635",'rahu3l'))