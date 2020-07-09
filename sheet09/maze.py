#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 13:59:38 2020

@author: marvin schmitt, christopher hoellriegl
"""

# (a)

# dict for less confusion
g = [
     {0:[1]},
     {1:[0,2,3]},
     {2:[1]},
     {3:[1,4,5]},
     {4:[3]},
     {5:[3,6,7]},
     {6:[5]},
     {7:[5,8,10]},
     {8:[7,9,10]},
     {9:[8]},
     {10:[7,8,11]},
     {11:[10,12,13]},
     {12:[11]},
     {13:[11,14,15]},
     {14:[13]},
     {15:[13]}
]


# Assure that neighbors are sorted descending
g = [{node:sorted(neighbors, reverse=True) for node, neighbors in u.items()} for u in g]


#print(g)


# Turn into adjascence list
gl = [list(*node.values()) for node in g]

#print(gl)



# (b)
def way_out(graph, startnode, targetnode):
    visited = [False]*len(graph)
    parents = [None]*len(graph)
    discovery_order = []
    finishing_order = []
    
    def visit(node, parent):
        if not visited[node]:
            visited[node] = True
            parents[node] = parent
            
            print(node)
            discovery_order.append(node)
            if node == targetnode: 
                print(f"target reached! Dead Ends: {len(finishing_order)}")
            for neighbor in graph[node]:
                visit(neighbor, parent=node)
            print(f"{parent}(backtrack)")
            finishing_order.append(node)
    visit(startnode, parent=None)
    


print("FINDING MY WAY OUT!")
#way_out(gl, 15, 0)
    


def way_out_stack(graph, startnode, targetnode):
    path = [startnode] # for detecting cycles
    s = list() # stack
    s.append([startnode, 0])
    n_dead_ends = 0

    while len(s) > 0:
        node, current_neighbor = s.pop()
        deg = len(graph[node]) # degree of current node
        
        if current_neighbor < deg:
            s.append([node, current_neighbor+1])

            current_neighbor = graph[node][current_neighbor]
            if current_neighbor not in path:
                path.append(current_neighbor)
                print(f"{current_neighbor}")
                if current_neighbor == targetnode:
                    print("target reached. dead end counter initialized... loading...")
                    break
    
                if len(graph[current_neighbor]) == 1:
                    n_dead_ends += 1
                    path.pop()
                    print(f"{node}(backtrack)")
                else:
                    s.append([current_neighbor, 0])

        elif current_neighbor == deg:
            path.pop() # finally remove it from actual path solution

    print(f"finished dead end calculation. Total of {n_dead_ends} dead ends.")
    print(f"\nidentified path ({len(path)-1} steps):\n{path}")
        
                

way_out_stack(gl, 15,0)
    

