def mulMatrix(A,B):
    # print(A,B)
    C = [[0 for i in range( len( B[0] ))] for j in range(len(A))]
    # print(C)
    for i in range(len(A)): 
        # iterating by coloum by B  
        for j in range(len(B[0])): 
            # iterating by rows of B 
            for k in range(len(A[0])): 
                # print(i,j,k)
                # print(C[i][j])
                C[i][j] += A[i][k] * B[k][j]
            C[i][j] %= 36
    return C

def zeros_matrix(rows, cols):
    A = []
    for i in range(rows):
        A.append([])
        for j in range(cols):
            A[-1].append(0)

    return A

def copy_matrix(M):
    rows = len(M)
    cols = len(M[0])

    MC = zeros_matrix(rows, cols)

    for i in range(rows):
        for j in range(rows):
            MC[i][j] = M[i][j]

    return MC

def determinant(A):
    total=0
    indices = list(range(len(A)))
     
    
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return val

    for fc in indices: 
        As = copy_matrix(A) 
        As = As[1:] 
        height = len(As) 
 
        for i in range(height):
            As[i] = As[i][0:fc] + As[i][fc+1:] 
 
        sign = (-1) ** (fc % 2)
        sub_det = determinant(As)        
        total += sign * A[0][fc] * sub_det 
 
    return total%36

def getMatrixMinor(m,i,j):
    # print([row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])])
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]


def mulInverse(num):

    if num == 1:
        return 1
    temp = 0
    while(temp % 36 != 1 ):
        temp += num

    return temp // num

def transpose(A):
    B = [[0 for x in range(len(A))] for y in range(len(A[0]))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            B[i][j] = A[j][i]
    return B

def matrixInverse(A):
    A = transpose(A)
    # print(determinant( A))
    mulInv = mulInverse(determinant(A)) 
    # print(mulInv)
    B = [[0 for x in range(len(A))] for y in range(len(A[0]))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            B[i][j] = determinant(getMatrixMinor(A,i,j))
            B[i][j] *= (-1)**(i+j)
            B[i][j] *= mulInv
            B[i][j] %= 36
    return B


if __name__ == "__main__":
    A = [[1,2,1],[1,1,2],[1,1,1]]
    print(matrixInverse(A))