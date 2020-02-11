from encrypt import *
from decrypt import *

file = open('input.dat','r')

plainText = file.readline()
key = file.readline()

file.close()

plainText = plainText[0:-1]
key.replace(" ","")

cipherText = encryptPF(plainText,key)
# print(cpiherText)

file = open("cipher.dat","w")
file.write(cipherText)
file.close()


file = open("cipher.dat","r")
cipherText = file.readline()
cipherText = cipherText[0:-1]
pText = decryptPF(cpiherText,key)
print(pText)