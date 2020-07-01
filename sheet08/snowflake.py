#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: christopher hoellriegl, marvin schmitt
"""
from math import sqrt
import numpy as np

def koch_snowflake(level):
    def length(v):
        return sqrt(v[0]**2 + v[1]**2)
        
    points = [
        np.array([0,0]),
        np.array([1,0]),
        np.array([1/2,sqrt(3)/2]),
        np.array([0,0])
        ]
    
    return [list(c) for c in zip(*points)]


#points_x, points_y = koch_snowflake(1)
    
a = np.array([1,0])
b = np.array([1/2,sqrt(3)/2])

points_x, points_y = [list(c) for c in zip(*[a,b])]



import matplotlib.pyplot as plt
plt.plot(points_x, points_y) # zeichne die Punkte aus Teilaufgabe b) 
plt.gca().set_aspect('equal') # skaliere x- und y-Achse gleich 
#plt.savefig('snowflake.svg') # speichere die Zeichnung
