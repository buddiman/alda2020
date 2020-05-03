from math import sqrt

def sieve(n):
    A = {i : True for i in range(2, n+1)}
    for i in range(2, int(sqrt(n))+1):
        if A[i] : 
            for j in [i**2 + k*i for k in range(0, n+1)]:
                if j > n:
                    break
                A[j] = False

    return [k for (k, v) in A.items() if v==True]