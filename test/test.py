def gaussian_elimination(L, C):
    return [t[0] for t in L]

def P5(C):
    n = len(C)
    L = [[0]*n for _ in range(n)]
    L[0][0]=1
    L[0][1]=1
    for i in range(1,n-1):
        L[i][i-1] = 1
        L[i][i] = 1
        L[i][i+1] =1
    L[n-1][n-2] = 1
    L[n-1][n-1] = 1
    x = gaussian_elimination(L, C)
    for i in range(n):
        if x[i] < 0:
            return None
    for i in range(n):
        x[i] = int(x[i])
    return x

if __name__ == "__main__":
    pass