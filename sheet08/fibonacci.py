"""
@author: Christopher Hoellriegl, Marvin Schmitt
"""

#import numpy as np
import time


def fib1(n):                      # Funktion berechnet die n-te Fibonacci-Zahl
    if n <= 1: 
         return n                 # Rekursionsabschluss
    return fib1(n-1) + fib1(n-2)  # Baumrekursion


def fib3(n):
    def fib3Impl(n):
        if n == 0: 
            return 1, 0         # gebe die Fibonacci-Zahl von 1 und die davor zurück
        else:                          # rekursiver Aufruf
           f1, f2 = fib3Impl(n-1)      # f1 ist Fibonacci-Zahl von n, f2 die von (n-1)
           return f1 + f2, f1          # gebe neue Fibonacci-Zahl fn+1 = f1+f2 und die vorherige (fn = f1) zurück.
    
    f1, f2 = fib3Impl(n)    # Hilfsfunktion, f1 ist die Fibonacci-Zahl von (n+1) und f2 ist die Fibonacci-Zahl von n
    return f2




def fib5(n):
    f1, f2 = 1, 0                # f1 ist die Fibonaccizahl für n=1, f2 die für n=0
    while n > 0:
        f1, f2 = f1 + f2, f1     # berechne die nächste Fibonaccizahl in f1 und speichere die letzte in f2
        n -= 1
    return f2


def getMaxDepth(functions, max_t = 10):
    for func, step_size in functions.items():
        n = 0
        t = 0
        while 1:
            try:
                tic = time.time()
                func(n)
                toc = time.time()
                t = toc-tic
                if t>10:
                    break
            except RecursionError:
                t = "Recursion Error"
                break
            n += step_size
            
        t_print = f"{t:.2f} sec" if type(t)==float else t
        print(f"Function {func.__name__}:, max n = {n} ({t_print}), Stepsize {step_size}.")
            
        
    
getMaxDepth({
    fib1 : 1,
    fib3 : 1,
    fib5 : 100000
    })

# fib1: n = 38 (13.4 sec)
# fib3: n = 2954 (Recursion Error)
# fib5: n = 1M (12.3 sec, stepsize 100k)

        

# (b)
def mul2x2(A, B):
    # why not like this...
    # return np.matmul(A, B)
    return [
        A[0]*B[0] + A[1]*B[2],
        A[0]*B[1] + A[1]*B[3],
        A[2]*B[0] + A[3]*B[2],
        A[2]*B[1] + A[3]*B[3]
        ]
    
    

def fib6(n):
    F1 = [1,1,1,0]
    F = F1
    if n == 0: 
        return [1,0,0,1]
    for i in range(n-1):
        F = mul2x2(F,F1)
    return F[1]
    
assert fib6(10) == fib1(10)

getMaxDepth({fib6:100000})
# fib6: n = 300k (12.6sec, stepsize 100k)


#c
def exp2x2(X, N):
    # take a matrix X to the power N
    if N < 0:
        raise ValueError("N must be non-negative!")

    if N == 0:
        return [1,0,0,1]
    
    if N == 1:
        return X
    
    if N % 2 == 0:
        return exp2x2(mul2x2(X,X), N/2)
    
    if N % 2 == 1:
        return mul2x2(X,
                      exp2x2(mul2x2(X,X), (N-1)/2)
                      )
    
    

def fib7(n):
    F1 = [1,1,1,0]
    return exp2x2(F1, n)[1]
    
    
for i in range(1, 100):
    assert fib5(i) == fib7(i)
    
getMaxDepth({fib7:100000})
# fib7: n = 7.2M (10.65 sec, stepsize 100k)
