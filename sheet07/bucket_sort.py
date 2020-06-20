# -*- coding: utf-8 -*-
"""
Abgabe 07
Christopher Hoellriegl, Marvin Schmitt
"""

import random
from math import sqrt
import matplotlib.pyplot as plt
import copy

random.seed(42)

### InsertionSort for buckets (from internet)
def insertionSort(nlist):
   for index in range(1,len(nlist)):

     currentvalue = nlist[index]
     position = index

     while position>0 and nlist[position-1]>currentvalue:
         nlist[position]=nlist[position-1]
         position = position-1

     nlist[position]=currentvalue

################

def create_data(size):
    X, Y, R = [], [], []
    while len(R) < size:
        x, y = random.uniform(-1,1), random.uniform(-1,1)
        r = sqrt(x**2 + y**2)
        if r < 1.0:
            X.append(x)
            Y.append(y)
            R.append(r)
            
    return X, Y, R
    

def quantize(r, M, mode = "quadratic"):
    if mode == "naive":
        return [int(i*M) for i in r]
    
    if mode == "quadratic":    
        return [int(i**2 * M) for i in r]
    
    
# (b)
def chi_squared_test(r):
    def chi_squared(r, N, M):
        s = 0
        c = N/M
        for k in range(M):
            n_k = sum([i == k for i in r])
            s += (n_k-c)**2 / c
        return s
    
    N = len(r)
    M = len(set(r))
    
    tau = sqrt(2 * chi_squared(r, N, M)) - sqrt(2 * M - 3)
    
    
    return abs(tau) > 3
    


N = 1000
x, y, r = create_data(N)

M = 10

plt1 = plt.subplot(221, title="After naive quantization")
plt1.axis("off")
plt1.hist([int(i*M) for i in r], alpha = .5, bins=M)

plt2 = plt.subplot(222, title="After quadratic quantization")
plt2.axis("off")
plt2.hist(quantize(r, M), alpha = .5, bins=M)
plt2.axhline(y=N/M, color="darkgreen")
plt2.annotate("c=N/M", xy = [-2,N/M+10], color="darkgreen")

plt3 = plt.subplot(223, title="x/y distribution")
plt3.set_aspect(aspect='equal')
plt3.scatter(x,y, alpha=.1)

def test_chi_squared():
    for N in [10000, 100000]:
        _, _ , r = create_data(N)
        for M in [10, 100, 1000]:
            # Quadratic quantizer -> chi^2 test should be not significant (False)
            assert chi_squared_test(quantize(r, M)) == False
            
            # Naive quantizer -> chi^2 test should be significant (True)
            assert chi_squared_test(quantize(r, M, mode="naive")) == True
    
    
def bucket_sort(a, bucketMap = lambda x, M : int(x**2 * M), d = 6):
    N = len(a)
    M = int(N / float(d))  # Anzahl der Buckets festlegen
    
    # M leere Buckets erzeugen
    buckets = [[] for k in range(M)]
    
    # Daten auf die Buckets verteilen
    for k in range(len(a)):
        index = bucketMap(a[k], M) # Bucket-Index berechnen
        buckets[index].append(a[k])    # a[k] im passenden Bucket einfügen
    
    # Daten sortiert wieder in a einfügen
    start = 0                          # Anfangsindex des ersten Buckets 
    for k in range(M):
        insertionSort(buckets[k])      # Daten innerhalb des aktuellen Buckets sortieren
        end = start + len(buckets[k])  # Endindex des aktuellen Buckets
        a[start:end] = buckets[k]      # Daten an der richtigen Position in a einfügen
        start += len(buckets[k])       # Anfangsindex für nächsten Bucket aktualisieren
    


bucket_sort(r)
#print(r)   


def test_bucket_sort():
    _, _, r = create_data(1000)
    r_copy = copy.deepcopy(r)
    
    bucket_sort(r)
    for i in range(len(r)-1):
        assert r[i] <= r[i+1]
    
    
    r_copy.sort()
    assert r == r_copy



import timeit
quantizer_functions = {
    "naive":(lambda x, M: int(x*M)), 
    "squared" : (lambda x, M: int(x**2 * M))
    }

print("##### Timeit test with 100 runs each: #####")
for quantizer_name, quantizer in quantizer_functions.items():
    print(f"\nBucket Map {quantizer_name}:")
    for N in [10000, 20000, 30000, 100000, 200000]:
        _, _, r = create_data(N)
        time_passed = timeit.timeit(
            'bucket_sort(r, bucketMap = quantizer)', 
            number = 100,
            globals = globals()
            )
        print(f"N = {N:6d}, time = {time_passed:.5f}s, ratio = {time_passed/N}")
        
# Yep, linear runtime and bucket map doesn't matter too much.


