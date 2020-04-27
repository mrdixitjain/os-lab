# file_entropy.py
#
# Shannon Entropy of a file
# = minimum average number of bits per character
# required for encoding (compressing) the file
#
# So the theoretical limit (in bytes) for data compression:
# Shannon Entropy of the file * file size (in bytes) / 8
# (Assuming the file is a string of byte-size (UTF-8?) characters
# because if not then the Shannon Entropy value would be different.)
# FB - 201011291
import sys
import math
if len(sys.argv) != 2:
    print("Usage: file_entropy.py [path]filename")
    sys.exit()

with open(sys.argv[1], "rb") as file1:
	data = file1.read()



print('File size in bytes:')
fileSize=len(data)
print(fileSize)
print()

freqList = []
for b in range(256):
    ctr = 0
    for byte in data:
        if byte == b:
            ctr += 1
    freqList.append(float(ctr) / fileSize)
# print 'Frequencies of each byte-character:'
# print freqList
# print

# Shannon entropy
ent = 0.0
for freq in freqList:
    if freq > 0:
        ent = ent + freq * math.log(freq, 2)
ent = -ent
print('Shannon entropy (min bits per byte-character):')
print(ent)







