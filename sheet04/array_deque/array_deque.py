###########################################################
#   Christopher Höllriegl / Marvin Schmitt
#   Blatt 04, Aufgabe 3
###########################################################

import doctest
import pytest
import copy

###########################################################

class array_deque:

    def __init__(self):
        '''Creates an empty deque array.
        At creation time memory is reserved for one element'''
        self._size = 0
        self._capacity = 1
        self._data = [None] * self._capacity
        
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
            self._capacity = self._capacity * 2
            temp_data = [None] * self._capacity
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

    def push(self, item):
        '''Add element at the end without doubling the capacity'''
        if self._capacity == self._size:
            self._capacity += 1                 # code to enlarge the memory by one
            temp_data = [None]  * self._capacity
            # Copy data in temp array
            for i in range(self._size):
                temp_data[i] = self._data[i]
            # Set original array to new array
            self._data = temp_data
        self._size += 1
        self._data[self._size - 1] = item

###########################################################

def test_array_deque():
    # create Array
    ar = array_deque()

    assert ar.size() == 0           # check size == 0
    check_size_seq_capacity(ar)     # check size <= capacity

    # test push
    temp_ar = copy.copy(ar)
    ar.push(1)
    check_after_push(ar, 1, temp_ar)
    check_when_not_empty(ar)

    # push some things to get a bigger array
    ar.push(5)
    ar.push(77)
    ar.push(23)
    ar.push(88)
    ar.push(999)
    ar.push(2)
    # test again
    temp_ar = copy.copy(ar)
    ar.push(12)
    check_after_push(ar, 12, temp_ar)
    check_when_not_empty(ar)

    # test c[k] = v
    temp_ar = copy.copy(ar)
    index = 5
    elem = 123
    ar[index] = elem
    check_assign_value(ar, index, elem, temp_ar)
    check_when_not_empty(ar)

    # test pop_last
    temp_ar = copy.copy(ar)
    ar.pop_last()
    check_pop_last(ar, temp_ar)
    check_when_not_empty(ar)

    # test pop_first
    temp_ar = copy.copy(ar)
    ar.pop_first()
    check_pop_first(ar, temp_ar)
    check_when_not_empty(ar)

    ar_empty = array_deque()

    with pytest.raises(RuntimeError):
        ar_empty.pop_first()

    with pytest.raises(RuntimeError):
        ar_empty.pop_last()

    # test slow array
    ar = slow_array_deque()
    temp_ar = copy.copy(ar)
    ar.push(22)
    check_after_push(ar, 22, temp_ar)
    check_when_not_empty(ar)

    # push some more
    ar.push(5)
    ar.push(77)
    ar.push(23)
    ar.push(88)
    temp_ar = copy.copy(ar)
    ar.push(99)
    check_after_push(ar, 99, temp_ar)
    check_when_not_empty(ar)



def check_size_seq_capacity(deque):
    '''Check if size is smaller of equal capacity'''
    assert deque.size() <= deque.capacity()

def check_after_push(deque, elem, original):
    assert deque.size() == original.size() + 1, "E: Axiom i wrong"  # (Axiome i)
    assert deque.last() == elem, "E: Axiom ii wrong"  # (Axiome ii)

    # (Axiome iii)
    if deque.size() >= 2:   # only if there >= 2 elements
        is_same = True
        for i in range(deque.size() - 1):
            if deque[i] != original[i]:
                is_same = False
        assert is_same, "E: Axiom iii wrong"

    # Axiome iv
    if original.size() == 0:
        assert deque.first() == elem, "E: Axiom iv wrong"
    else:
        assert deque.first() == original.first(), "E: Axiom iv wrong"

    # Axiome v
    deque.pop_last()
    assert deque == original, "E: pop_last did not work correct."

    # !!push again to not change the array!!
    deque.push(elem)

def check_when_not_empty(deque):
    assert deque.first() == deque[0]
    assert deque.last() == deque[deque.size() - 1]

def check_assign_value(deque, index, elem, original):
    assert deque.size() == original.size()
    assert deque[index] == elem

    is_same = True
    for i in range(deque.size() - 1):
        if i == index:
            continue
        if deque[i] != original[i]:
            is_same = False
    assert is_same

def check_pop_last(deque, original):
    assert deque.size() == original.size() - 1

    is_same = True
    for i in range(deque.size()):
        if deque[i] != original[i]:
            is_same = False
    assert is_same

def check_pop_first(deque, original):
    assert deque.size() == original.size() - 1

    is_same = True
    for i in range(deque.size()):
        if deque[i] != original[i]:
            is_same = False
    assert is_same