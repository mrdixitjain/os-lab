from determinent import *
def retCode(sym):
    # print(sym)
    if(sym.isalpha()):
        return ord(sym) - ord('a')
    else:
        return ord(sym) - ord('0') + 26 

def decryptHC(cipherText,keyMat):
    alphaSet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    keyMat = matrixInverse(keyMat)
    # print(keyMat)
    chunks = len(cipherText)
    chunk_size = len(keyMat)
    text = [cipherText[i:i+chunk_size] for i in range(0, chunks, chunk_size)]

    # print(text)

    asciiText = []

    for i in text:
        asciiText.append([])
        for j in i:
            # print(j)
            asciiText[-1].append(retCode(j))
    
    plainMat = mulMatrix(asciiText,keyMat)
    # print(mulMatrix(asciiText,keyMat))

    res = ''

    for i in range(len(plainMat)):
        for j in range((len(plainMat[0]))):
            res += alphaSet[plainMat[i][j]]
    # print(res)
    return res

if __name__ == "__main__":
    print(retCode('y'))