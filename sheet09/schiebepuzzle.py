#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 14:30:28 2020

@author: marvin schmitt, christopher hoellriegl
"""

import random

class Schiebepuzzle:
    '''
    Schiebepuzzle is a 4x4 handler for the given list representation.
    Indexes are 1-based: x = 1-4, y = 1-4
    '''
    
    def __init__(self, data):
        self._data = data
        self._last_action = None
    
    def __setitem__(self, xy, value):
        x,y = xy
        self._data[4*(y-1) + (x-1)] = value

        
    def __getitem__(self, xy):
        x, y = xy
        return self._data[4*(y-1) + (x-1)]
    
    def __str__(self): 
        s = ""
        for y in range(1,5):
            for x in range(1,5):
                s+= f"{self[(x,y)]:>3}"
            s+="\n"
            
        return s
    
    def swap(self, xy1, xy2):
        x1, y1 = xy1
        x2, y2 = xy2
        self[(x1, y1)], self[(x2, y2)] = self[(x2, y2)], self[(x1, y1)]
    
    def get_space(self):
        return Schiebepuzzle.to_tuple_index(self._data.index(" "))
    
    @staticmethod
    def to_tuple_index(idx):
        return idx%4+1, idx//4+1
        
    def up(self):
        x, y = self.get_space()
        if y == 1 or self._last_action=="down":
            return False
        self.swap((x, y), (x, y-1))
        self._last_action = "up"
        return True
        
    def down(self):
        x, y = self.get_space()
        if y == 4 or self._last_action=="up":
            return False
        self.swap((x, y), (x, y+1))
        self._last_action = "down"
        return True
        
    def left(self):
        x, y = self.get_space()
        if x == 1 or self._last_action=="right":
            return False
        self.swap((x, y), (x-1, y))
        self._last_action = "left"
        return True
        
    def right(self):
        x, y = self.get_space()
        if x == 4 or self._last_action=="left":
            return False
        self.swap((x, y), (x+1, y))
        self._last_action = "right"
        return True
        
        
    def shuffle_pos(self, N, log=False):
        for i in range(N):
            success = False
            while not success:
                move_name = ["up", "left", "down", "right"][random.randint(0,3)]
                move_func = getattr(Schiebepuzzle, move_name)
                success = move_func(self)
                
                if log:
                    success_log = "SUCCESS" if success else "FAIL"
                    print(f"Move: {move_name} ({success_log})")
                    if success: print(self)

        

p = Schiebepuzzle([1,2,3,4,5,6,7,8,9,10,11,12,13,14,' ', 15])

print(p)
p.shuffle_pos(20, log=True)
print(p)