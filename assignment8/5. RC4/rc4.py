import numpy as np

def readData(fileName):
	file=open(fileName,"r")
	s=file.read().split(" ")
	text,key=s[0],s[1]
	#print(s)
	return text,key

def writeData(fileName,data):
	file=open(fileName,"a")
	file.write(data)

def Key_Sceduling_Algo(key):
	length=len(key)
	s=list(range(256))
	#print(s)
	j=0
	for i in range(256):
		j=(j+s[i]+key[i%length])%256
		s[i],s[j]=s[j],s[i]

	return s

def PRGA(s,n):
	i=0
	j=0
	k=[]
	while n>0:
		n=n-1
		i=(i+1)%256
		j=(j+s[i])%256
		s[i],s[j]=s[j],s[i]

		t=s[(s[i]+s[j])%256]

		k.append(t)
	return k

def key_array(s):
	return [ord(c) for c in s]


def encryption(text1,key1):
	text=text1
	key=key1
	key=key_array(key)
	#print(key)

	s=Key_Sceduling_Algo(key)

	stream=np.array(PRGA(s,len(text)))

	#print(stream)

	text=np.array([ord(i) for i in text])



	cipher=stream^text

	ab=[chr(c) for c in cipher]

	#print([chr(c) for c in plainText])

	cipherText="".join(ab)

	#print(cipher)

	#cipher=cipher.astype(np.uint8).data.hex()
	return cipherText

def decryption(cipher,key):
	print("decryption")
	key=key_array(key)
	#print(key)
	s=Key_Sceduling_Algo(key)

	stream=np.array(PRGA(s,len(cipher)))
	#print(stream)

	cipher=np.array([ord(i) for i in cipher])

	plainText=stream^cipher


	#print(plainText%256)

	Plain=[chr(c) for c in plainText]

	#print([chr(c) for c in plainText])

	Plain="".join(Plain)

	#print(Plain)

	#=plainText.astype(np.uint8).data.hex()
	return Plain


def main():
	text,key=readData("in.dat")
	# text="Mission Accomplished"
	# key="KAREEM"
	print(text)
	print(key)

	cipherText=encryption(text,key)
	print("cipher Text is:")
	print(cipherText)
	writeData("op.dat",cipherText)


	#print(b)

	#print(type(cipherText))

	#cipherText=bytes.fromhex(cipherText)
	#print(type(cipherText))
	#print(bytes.fromhex(cipherText))
	# cipherText=cipherText.decode("hex")

	# print(cipherText)


	plainText=decryption(cipherText,key)

	print("decrypted text is:")

	print(plainText)


main()