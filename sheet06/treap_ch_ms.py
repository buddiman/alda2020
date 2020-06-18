import pytest
import random

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
        
    def __getitem__(self, key):
        node = SearchTree._tree_find(self._root, key)
        if node is None:
            raise KeyError(key)
        return node._value
        
    def __setitem__(self, key, value):
        self._root, key_is_new = SearchTree._tree_insert(self._root, key, value)
        if key_is_new:
            self._size += 1
        
    def __delitem__(self, key):
        self._root = SearchTree._tree_remove(self._root, key)
        self._size -= 1
    
    @staticmethod
    def _tree_find(node, key):
        if node is None:
            return None
        if key == node._key:
            return node
        if key < node._key:
            return SearchTree._tree_find(node._left, key)
        else:
            return SearchTree._tree_find(node._right, key)
    
    @staticmethod
    def _tree_insert(node, key, value):
        if node is None:
            node = SearchTree.Node(key, value)
            key_is_new = True
        elif key == node._key:
            node._value = value
            key_is_new = False
        elif key < node._key:
            node._left, key_is_new = SearchTree._tree_insert(node._left, key, value)
        else:
            node._right, key_is_new = SearchTree._tree_insert(node._right, key, value)
        return node, key_is_new
    
    
    @staticmethod
    def _tree_predecessor(node):
        node = node._left
        while node._right is not None:
            node = node._right
        return node
        
    @staticmethod
    def _tree_remove(node, key):
        if node is None:
            raise KeyError(key)
        if key < node._key: 
            node._left = SearchTree._tree_remove(node._left, key)
        elif key > node._key:
            node._right = SearchTree._tree_remove(node._right, key)
        else: 
            if node._left is None and node._right is None: 
                node = None            
            elif node._left is None: 
                node = node._right 
            elif node._right is None: 
                node = node._left
            else:
                pred = SearchTree._tree_predecessor(node)
                node._key = pred._key
                node._value = pred._value
                node._left = SearchTree._tree_remove(node._left, pred._key)
        return node
    
    @staticmethod
    def _tree_rotate_left(node):
        newRoot = node._right
        node._right = newRoot._left
        newRoot._left = node
        return newRoot
        
    @staticmethod
    def _tree_rotate_right(node):
        newRoot = node._left
        node._left = newRoot._right
        newRoot._right = node
        return newRoot
    
    def depth(self):
        """
        Gibt die Tiefe des Baumens (d.h. Abstand Wurzel z. tiefsten Blatt) aus
        """
    
        def _depth(rootnode):
            """
            Hilfsfunktion fuer depth: die Tiefe des aktuellen 'rootnode'
            ist um eins groesser als die Tiefe seines groessten Unterbaums.
            """
            if rootnode is None:
                return 0
            return max(_depth(rootnode._left), _depth(rootnode._right)) + 1
    
        if self._root is None:
            raise RuntimeError("depth(): tree is empty.")
        
        result = _depth(self._root)
        
        # eins abziehen, da wir die Kanten zaehlen und nicht die Knoten
        return result - 1


class TreapBase(SearchTree):
    class Node(SearchTree.Node):
        def __init__(self, key, value, is_in_dynamic_treap):
            super().__init__(key, value)
            if is_in_dynamic_treap:
                self._priority = 1
            else:
                self._priority = random.random() * 10
        
        def display(self):
            lines, _, _, _ = self._display_aux()
            return '\n'.join(lines)
            
        def _display_aux(self):
            """Returns list of strings, width, height, and horizontal coordinate of the root."""
            # No child.
            if self._right is None and self._left is None:
                line = '{}({:.2f})'.format(self._key, self._priority)
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            # Only left child.
            if self._right is None:
                lines, n, p, x = self._left._display_aux()
                s = '{}({:.2f})'.format(self._key, self._priority)
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            # Only right child.
            if self._left is None:
                lines, n, p, x = self._right._display_aux()
                s = '{}({:.2f})'.format(self._key, self._priority)
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            # Two children.
            left, n, p, x = self._left._display_aux()
            right, m, q, y = self._right._display_aux()
            s = '{}({:.2f})'.format(self._key, self._priority)
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
        super().__init__()
        self._is_dynamic_treap = False
        
    def __setitem__(self, key, value):
        self._root, key_is_new = TreapBase._tree_insert(self._root, key, value, self._is_dynamic_treap)
        if key_is_new:
            self._size += 1
            
            
    def __getitem__(self, key):
        node = TreapBase._tree_find(self._root, key)
        if node is None:
            raise KeyError(key)
            
        # very inefficient, but this secures heap property :)
        if self._is_dynamic_treap:
            TreapBase._tree_insert(self._root, key, node._value, self._is_dynamic_treap)
        return node._value
    
    def __str__(self):
        return "Empty Treap!" if self._root is None else "\n"+self._root.display()+"\n"
    
    @staticmethod        
    def _tree_insert(node, key, value, is_dynamic_treap):
        # Suchbaum insert
        if node is None:
            node = TreapBase.Node(key, value, is_dynamic_treap)
            key_is_new = True
            
        elif key == node._key:
            node._value = value
            key_is_new = False
            if is_dynamic_treap:
                node._priority += 1
                
        elif key < node._key:
            node._left, key_is_new = TreapBase._tree_insert(node._left, key, value, is_dynamic_treap)
            node = TreapBase._upheap(node)

                
        else:
            node._right, key_is_new = TreapBase._tree_insert(node._right, key, value, is_dynamic_treap)
            node = TreapBase._upheap(node)
            
        # Repariere Heap auf Rückweg der Rekursion
                
        return node, key_is_new
        
    @staticmethod
    def _upheap(node):
        if node._left is not None and node._left._priority > node._priority:
            node = SearchTree._tree_rotate_right(node)
        if node._right is not None and node._right._priority > node._priority:
                node = SearchTree._tree_rotate_left(node)
        return node
        
                
        

        
        
 
class RandomTreap(TreapBase):
    pass
        
        
class DynamicTreap(TreapBase):  
    def __init__(self):
        super().__init__()
        self._is_dynamic_treap = True
    

# Tests
def test_search_tree():
    t = SearchTree()
    assert len(t) == 0
    
    t[1] = 1
    assert len(t) == 1
    assert t[1] == 1
    with pytest.raises(KeyError):
        v = t[2]
    
    t[0] = 0
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 1
    
    t[1] = 11                # overwrite value of existing key
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 11
    
    t[2] = 2
    assert len(t) == 3
    assert t[0] == 0
    assert t[1] == 11
    assert t[2] == 2
    
    del t[2]                 # delete leaf
    assert len(t) == 2
    assert t[0] == 0
    assert t[1] == 11
    with pytest.raises(KeyError):
        v = t[2]
        
    del t[1]                 # replace node with left child
    assert len(t) == 1
    assert t[0] == 0
    with pytest.raises(KeyError):
        v = t[1]

    with pytest.raises(KeyError):
        del t[1]             # delete invalid key
        
    t = SearchTree()
    t[0]=0
    t[3]=3
    t[1]=1
    t[2]=2
    t[4]=4
    assert len(t) == 5
    for k in [0, 1, 2, 3, 4]:
        assert t[k] == k
        
    del t[3]                 # replace node with predecessor
    with pytest.raises(KeyError):
        v = t[3]
    assert len(t) == 4
    for k in [0, 1, 2, 4]:
        assert t[k] == k
        
    del t[2]                 # replace node with predecessor
    with pytest.raises(KeyError):
        v = t[2]
    assert len(t) == 3
    for k in [0, 1, 4]:
        assert t[k] == k
        
    del t[1]                 # replace node with right child
    with pytest.raises(KeyError):
        v = t[1]
    assert len(t) == 2
    for k in [0, 4]:
        assert t[k] == k
        
    del t[4]                 # remove leaf
    with pytest.raises(KeyError):
        v = t[4]
    assert len(t) == 1
    assert t[0] == 0
        
    del t[0]                 # remove leaf
    with pytest.raises(KeyError):
        v = t[0]
    assert len(t) == 0
    
def test_depth():
    t1 = SearchTree()
    
    with pytest.raises(RuntimeError):
        t1.depth()
    
    t1[1] = 10
    assert t1.depth() == 0
    
    t1[2] = 20
    t1[3] = 30
    assert t1.depth() == 2
    
    t2 = SearchTree()
    t2[6] = 60
    t2[3] = 30
    t2[1] = 10
    t2[4] = 42
    t2[8] = 8
    assert t2.depth() == 2
    
def try_rotate():
    t = SearchTree()
    t[2] = 2
    t[6] = 6
    t[10] = 10
    t[3] = 3
    t[7] = 7
    print(t)
    print("rotating")
    t._root._right = SearchTree._tree_rotate_left(t._root._right)
    print(t)
    
    

if __name__ == '__main__':
    test_search_tree()
    test_depth()
    #try_rotate()
    
    t = DynamicTreap()
    t[2] = 2
    t[6] = 6
    t[10] = 10
    t[4] = 4
    t[5] = 5
    print(t)
    t[5] = 6
    print(t)
    t[5] = 7
    print(t)
    
    