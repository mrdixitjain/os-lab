from determinent import *
def retCode(sym):
	if(sym.isalpha()):
		return ord(sym) - ord('a')
	else:
		return ord(sym) - ord('0') + 26 
	
def encryptHC(plainText,keyMat):
	plainText.replace(" ","")
	alphaSet = 'abcdefghijklmnopqrstuvwxyz0123456789'
	
	while(len(plainText)%len(keyMat) != 0):
		plainText += 'z'

	chunks = len(plainText)
	chunk_size = len(keyMat)
	text = [plainText[i:i+chunk_size] for i in range(0, chunks, chunk_size)]

	# print(text)

	asciiText = []

	for i in text:
		asciiText.append([])
		for j in i:
			asciiText[-1].append(retCode(j))
	# print(asciiText)
	cipherMat = mulMatrix(asciiText,keyMat)

	# print(cipherMat)
	res = ''

	for i in range(len(cipherMat)):
		for j in range((len(cipherMat[0]))):
			res += alphaSet[cipherMat[i][j]]
	# print(res)
	return res