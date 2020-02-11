from encrypt import *
from decrypt import *
from determinent import *

file = open('input.dat','r')
plainText = file.readline()
plainText = plainText[0:-1]


keyMat = []
data = file.readline()
keyMat.append( list(map(int,data.split())))

for i in range(len(keyMat[0]) - 1):
	data = file.readline()
	keyMat.append( list(map(int,data.split())))
# print(keyMat)
file.close()
prime = [1,5,7,11,13,17,19,23,25,29,31,35]

# print(keyMat)
if determinant(keyMat)%36 not in prime:
	print("error Key matrix invalid determinant should be 1,5,7,11,13,17,19,23,25,29,31 or 35 modulo 36.")
	exit(0)

cipherText = encryptHC(plainText,keyMat)
# print(cipherText)
file = open("cipher.dat","w")
file.write(cipherText)
file.close()


file = open("cipher.dat","r")
cipherText = file.readline()
# cipherText = cipherText[0:-1]
pText = decryptHC(cipherText,keyMat)
print(pText)