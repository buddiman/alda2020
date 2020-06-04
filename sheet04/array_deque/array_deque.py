import doctest
import pytest

###########################################################

class array_deque:

    def __init__(self):
        '''Creates an empty deque array.
        At creation time memory is reserved for one element'''
        self._size = 0
        self._capacity = 1
        self._data = [None]
        
    def size(self):
        '''returns the number of elements in the array'''
        return self._size
        
    def capacity(self):
        '''returns the size (possible number of elements) of the array'''
        return self._capacity
        
    def push(self, item):
        '''append item as element at the end to the array
        :parameter item element to append'''

        # Check if Memory is full
        if self._capacity == self._size:
            # double memory (stated in the requirements)
            self.capacity_ = self.capacity_ * 2
            temp_data = [None]
            # Copy data in temp array
            for i in range(self._size):
                temp_data[i] = self._data[i]
            # Set original array to new array
            self._data = temp_data

        # Append new item
        self._data[self._size] = item
        self._size += 1
        
    def pop_first(self):
        '''remove the first element of the array'''
        if self._size == 0:
            raise RuntimeError("pop_first() on empty container")
        self._size -= 1

        # move all elements to n - 1
        for n in range(self._size):
            self._data[n] = self._data[n + 1]
        
    def pop_last(self):
        '''remove the last element of the array'''
        if self._size == 0:
            raise RuntimeError("pop_last() on empty container")

        self._size -= 1     # trivial, just cut off the end.
        
    def __getitem__(self, index):         # __getitem__ implements v = c[index]
        '''Get the element at a position
        :parameter index position which you want returned
        :return the element at index'''
        if index < 0 or index >= self._size:
            raise RuntimeError("index out of range")
        return self._data[index]
        
    def __setitem__(self, index, v):
        '''Set the element at a position
        :parameter index the position where the data should be set
        :parameter v data to set at index'''
        if index < 0 or index >= self._size:
            raise RuntimeError("index out of range")
        self._data[index] = v
        
    def first(self):
        '''Get the first element of the Array
        :return the first element of the Array'''
        return self.__getitem__(0)
        
    def last(self):
        '''Returns the last element of the Array
        :return the last element of the Array'''
        return self.__getitem__(self._size - 1)
        
    def __eq__(self, other):
        '''returns True if self and other have same size and elements'''

        if self._size != other.size():
            return False

        for i in range(self._size):
            if self._data[i] != other[i]:
                return False

        return True

    def __ne__(self, other):
        '''returns True if self and other have different size or elements'''
        return not (self == other)

###########################################################

class slow_array_deque(array_deque):

    def push(self, item):                 # add item at the end
        if self._capacity == self._size:  # internal memory is full
            ...                           # code to enlarge the memory by one
        self._size += 1
        ...                               # your code to insert the new item

###########################################################

def test_array_deque():
    ...                                   # your tests here
