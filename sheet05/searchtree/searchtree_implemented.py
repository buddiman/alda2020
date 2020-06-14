import pytest
import ipytest
ipytest.autoconfig()

class SearchTree:
    class Node:
        def __init__(self, key, value):
            self._key = key
            self._value = value
            self._left = self._right = None
            
        def display(self):
            lines, _, _, _ = self._display_aux()
            return '\n'.join(lines)

        ### Display from https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python/34014370
        def _display_aux(self):
            """Returns list of strings, width, height, and horizontal coordinate of the root."""
            # No child.
            if self._right is None and self._left is None:
                line = '%s' % self._key
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            # Only left child.
            if self._right is None:
                lines, n, p, x = self._left._display_aux()
                s = '%s' % self._key
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            # Only right child.
            if self._left is None:
                lines, n, p, x = self._right._display_aux()
                s = '%s' % self._key
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            # Two children.
            left, n, p, x = self._left._display_aux()
            right, m, q, y = self._right._display_aux()
            s = '%s' % self._key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
            return lines, n + m + u, max(p, q) + 2, n + u // 2



    def __init__(self):
        self._root = None
        self._size = 0
        
    def __str__(self):
        return "Empty SearchTree!" if self._root is None else self._root.display()
    
    
    def __len__(self):
        return self._size
        
    def __getitem__(self, key):          # implements 'value = tree[key]'
        result = SearchTree._tree_find(self._root, key)
        if result is not None:
            return result._value
        else:
            return None

    def __setitem__(self, key, value):   # implements 'tree[key] = value'
        if self._root is None:
            self._root = SearchTree.Node(key, value)
            self._size += 1
        else:
            result = SearchTree._tree_find(self._root, key)
            if result is not None:
                result._value = value
            else:
                SearchTree._tree_insert(self._root, key, value)
                self._size += 1
        
            

    def __delitem__(self, key):          # implements 'del tree[key] '
        if SearchTree._tree_remove(self._root, key):
            self._size -= 1

    @staticmethod
    def _tree_find(node, key):           # internal implementation
        if node is None:
            return None
        if node._key == key:
            return node
        if node._key < key:
            return SearchTree._tree_find(node._right, key)
        if node._key > key:
            return SearchTree._tree_find(node._left, key)

    @staticmethod
    def _tree_insert(node, key, value):  # internal implementation
        if node is None:      # richtiger Platz gefunden
            return SearchTree.Node(key, value)  # => neuen Knoten einfügen
        if node._key == key:   # schon vorhanden
            return node       # => nichts tun
        elif key < node._key:     
            node._left = SearchTree._tree_insert(node._left, key, value) # im linken Teilbaum einfügen
        else:
            node._right = SearchTree._tree_insert(node._right, key, value) # im rechten Teilbaum einfügen
        return node

    @staticmethod
    def _tree_remove(node, key):         # internal implementation
        if node is None:   # key nicht vorhanden
            return node    # => nichts tun
        if key < node._key: 
            node._left = SearchTree._tree_remove(node._left, key)
        elif key > node._key:
            node._right = SearchTree._tree_remove(node._right, key)
        else:              # key gefunden
            if node._left is None and node._right is None:     # Fall 1
                node = None            
            elif node._left is None:     # Fall 2
                node = node._right       # +
            elif node._right is None:    # Fall 2
                node = node._left
            else:                       # Fall 3
                pred = SearchTree._treePredecessor(node)
                node._key = pred._key
                node._left = SearchTree._tree_remove(node._left, pred._key)
        return node

        
    @staticmethod
    def _treePredecessor(node):
        node = node._left
        while node._right is not None:
            node = node._right
        return node
        
def test_search_tree():
    t = SearchTree()
    assert len(t) == 0

    t[4] = "vier"
    assert len(t) == 1

    t[6] = "sechs"
    assert len(t) == 2
    assert t[6] == "sechs"

    t[2] = "zwei"
    assert len(t) == 3

    t[3] = "drei"

    t[5] = "fünf"
    len_before_delete = len(t)
    del t[2]    
    assert len(t) == (len_before_delete - 1)
    
    # Can't overwrite _root yet. But printing works..
    del t[4]
    assert t._root._value != "vier"
    

def pretty_print():
    t = SearchTree()
    assert len(t) == 0

    t[4] = "vier"
    assert len(t) == 1

    t[6] = "sechs"
    assert len(t) == 2
    assert t[6] == "sechs"

    t[2] = "zwei"
    assert len(t) == 3

    t[3] = "drei"

    t[5] = "fünf"
    print(t)
    del t[4]
    print(t)
pretty_print()

doctest.testmod()
ipytest.run()
