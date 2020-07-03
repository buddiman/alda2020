#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: christopher hoellriegl, marvin schmitt
"""
from math import sqrt, pi
import numpy as np



# Exercise (a) and (b)
def koch_snowflake(level): 
    
    # auxilary function takes contour vector and returns new contour
    def koch_snowflake_aux(_points):
        
        # auxilary^2 function takes line and returns new points
        # Exercise (a)
        def koch_divide(A, B):
            v = B-A
            u = np.array([v[1], -v[0]])
            P1 = A + (1/3) * v
            P2 = A + (2/3) * v
            P3 = A + (1/2) * v + (1/3) * np.sin(2*pi / 6) * u # sin(60°)
            return [A, P1, P3, P2, B]
        
        points_new = []
        n = len(_points)
    
        for i in range(n):
            points_new.extend(koch_divide(_points[i], _points[(i+1)%n]))
        return points_new
     
    # starting points -> given triangle
    points = [
        np.array([0,0]),
        np.array([1,0]),
        np.array([1/2,sqrt(3)/2])
        ]
    
    # advance
    for i in range(level):
        points = koch_snowflake_aux(points)
    
    # return as points_x, points_y
    return [list(c) for c in zip(*points)]



points_x, points_y = koch_snowflake(5)



# Exercise (b)
with open("snowflake.txt", 'w') as f:
    for x, y in zip(points_x, points_y):    
        f.write(f"{x} {y}\n")


# Exercise (c)
import matplotlib.pyplot as plt
plt.plot(points_x, points_y) # zeichne die Punkte aus Teilaufgabe b) 
plt.gca().set_aspect('equal') # skaliere x- und y-Achse gleich 
plt.savefig('snowflake.svg') # speichere die Zeichnung
