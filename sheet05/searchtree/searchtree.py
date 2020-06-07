import pytest

class SearchTree:
    class Node:
        def __init__(self, key, value):
            self._key = key
            self._value = value
            self._left = self._right = None

    def __init__(self):
        self._root = None
        self._size = 0
        
    def __len__(self):
        return self._size
        
    def __getitem__(self, key):          # implements 'value = tree[key]'
        ... # your code here

    def __setitem__(self, key, value):   # implements 'tree[key] = value'
        ... # your code here

    def __delitem__(self, key):          # implements 'del tree[key] '
        ... # your code here

    @staticmethod
    def _tree_find(node, key):           # internal implementation
        ... # your code here

    @staticmethod
    def _tree_insert(node, key, value):  # internal implementation
        ... # your code here

    @staticmethod
    def _tree_remove(node, key):         # internal implementation
        ... # your code here

    # Aufgabe b)
    def depth(self, node):
        # If there are no more elements return 0
        if node == None:    # garbage python... null = None wtf
            return 0
        else:
            # get the left and the right side, recursive
            l = self.depth(node._left)
            r = self.depth(node._right)

            # return the max of left and right
            return max(l, r) + 1    # don't forget the + 1

def test_search_tree():
    t = SearchTree()
    assert len(t) == 0
    
    ... # your code here
