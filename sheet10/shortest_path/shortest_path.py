'''
Christopher Höllriegl, Marvin Schmitt
Blatt 10, Aufgabe 3
'''

import json
import heapq
import math

'''
Dijkstra-Algorithm: Aachen to Passau : 367 nodes visited.
A-Star-Algorithm:   Aachen to Passau : 138 nodes visited.
Dijkstra-Algorithm: Saarbrücken to Leipzig : 309 nodes visited.
A-Star-Algorithm:   Saarbrücken to Leipzig : 51 nodes visited.
Dijkstra-Algorithm: München to Greifswald : 350 nodes visited.
A-Star-Algorithm:   München to Greifswald : 53 nodes visited.
Dijkstra-Algorithm: Konstanz to Kassel : 152 nodes visited.
A-Star-Algorithm:   Konstanz to Kassel : 60 nodes visited.

A-Star muss über 50% weniger Knoten als Dijkstra besuchen.
'''


# Aufgabe a)
def createGraph(distanceDict):
    '''
    :param distanceDict: data from json file
    :return: graph: "Adjazenzlist" of the graph
    :return: names: property map with nodes assigned to names
    :return: weights: property map "Kantengewicht"
    '''


    # Return values
    graph = []
    names = {}
    weights = {}

    # convert cities to numbers
    n = 0
    for stadt in distanceDict:
        names[n] = stadt
        n += 1

    # numbers is the inverted names
    numbers = {}
    for number in names:
        numbers[names[number]] = number

    # read JSON and build graph
    for stadt in distanceDict:
        neighbours = []
        for neighbour in distanceDict[stadt]['Nachbarn'].keys():
            neighbours.append(numbers[neighbour])
        graph.append(neighbours)

    # initialise weights that it is practically infinite (careful, it isn't)
    for i in range(len(names)):
        for j in range(len(names)):
            weights[(i, j)] = 10000000000000

    # read JSON for weights
    for stadt in distanceDict:
        for neighbour in distanceDict[stadt]['Nachbarn']:
            weights[(numbers[stadt], numbers[neighbour])] = distanceDict[stadt]['Nachbarn'][neighbour]

    # Aufgabe c)
    air_line = {}       # "Luftlinie"

    # get the air line between the cities
    for i in range(len(names)):
        for j in range(len(names)):
            air_line[(i, j)] = air_line_distance(distanceDict[names[i]], distanceDict[names[j]])

    return graph, names, weights, numbers, air_line


# Aufgabe b)
def dijkstra(graph, weights, startnode, destination):
    '''
    Implementation of the Dijkstra algorithm
    :param startnode: where to start
    :param destination: destination
    :return: path and the distance
    '''
    parents = [None] * len(graph)

    q = []  # using a heap
    heapq.heappush(q, (0.0, startnode, startnode))

    n = 0   # Helper for number of nodes

    while len(q) > 0:  # iterate over all nodes
        n += 1

        distance, node, predecessor = heapq.heappop(q)  # get nodes from the heap

        # check if parent is alreade set
        if parents[node] is not None:
            continue

        # set the parent node
        parents[node] = predecessor

        if node == destination:
            break  # end because destination is reached

        for neighbor in graph[node]:
            if parents[neighbor] is None:
                newLength = distance + weights[(node, neighbor)]  # calculate distance to neighbours
                heapq.heappush(q, (newLength, neighbor, node))

    # create the path
    path = [destination]
    while path[-1] != startnode:
        path.append(parents[path[-1]])
    path.reverse()  # reverse to order from start to end

    print('Dijkstra-Algorithm:', names[startnode], 'to', names[destination], ':', n, 'nodes visited.')

    return path, distance


# helper funtion to print the path for b)
def print_path(graph, weights, numbers, start, ziel):
    '''
    print the path from start to ziel
    :param start: starting city
    :param ziel: destination
    '''
    path, length = dijkstra(graph, weights, numbers[start], numbers[ziel])
    print(start, 'to', ziel, ':', length, 'km')
    for i in range(len(path)):
        print(names[path[i]], end=' ')
        if i < len(path) - 1:
            print('=>', end=' ')
            print(weights[path[i], path[i + 1]], 'km', end=' ')
            print('=>', end=' ')
    print('(overall:', length, 'km)', '\n')


# Helper function for air line (actual the calculation takes place here)
def air_line_distance(city_1, city_2):
    a1, b1 = city_1['Koordinaten']['Breite'].split('N')
    B1 = (float(a1) + (float(b1) / 60)) / 180 * math.pi

    c1, d1 = city_1['Koordinaten']['Länge'].split('E')
    L1 = (float(c1) + (float(d1) / 60)) / 180 * math.pi

    a2, b2 = city_2['Koordinaten']['Breite'].split('N')
    B2 = (float(a2) + (float(b2) / 60)) / 180 * math.pi

    c2, d2 = city_2['Koordinaten']['Länge'].split('E')
    L2 = (float(c2) + (float(d2) / 60)) / 180 * math.pi

    a = math.sin(B1) * math.sin(B2)
    b = math.cos(B1) * math.cos(B2) * math.cos(L2 - L1)

    # HACK I had an math error when testing things. This manual fix should prevent the error
    if (a + b) > 1:
        c = 1
    else:
        c = a + b

    return 6378.137 * math.acos(c)


def a_star(graph, weights, air_distance, startnode, destination):
    '''
    Implementation of the a-star algorithm
    :param air_distance:
    :param startnode:
    :param destination:
    :return: path and the distance
    '''
    parents = [None] * len(graph)

    q = []  # q as Heap again
    heapq.heappush(q, (0.0, 0.0, startnode, startnode))
    n = 0   # Helper

    while len(q) > 0:
        n += 1

        priority, distance, node, predecessor = heapq.heappop(q)

        if parents[node] is not None:
            continue

        parents[node] = predecessor  # set parent

        if node == destination:
            break  # destination reached, cancel

        for neighbor in graph[node]:
            if parents[neighbor] is None:
                new_length = distance + weights[(node, neighbor)]  # calculate distance to neighbor
                new_priority = new_length + air_distance[(neighbor, destination)]
                heapq.heappush(q, (new_priority, new_length, neighbor, node))

    # create the path
    path = [destination]
    while path[-1] != startnode:
        path.append(parents[path[-1]])

    path.reverse()  # reverse to order from start to end
    print('A-Star-Algorithm:  ', names[startnode], 'to', names[destination], ':', n, 'nodes visited.')
    return path, distance


# helper function to print path for a-star
def print_path_astar(graph, weights, air_distance, numbers, start, ziel):
    path, length = a_star(graph, weights, air_distance, numbers[start], numbers[ziel])

    print(start, 'to', ziel, ':', length, 'km')

    for i in range(len(path)):
        print(names[path[i]], end=' ')
        if i < len(path) - 1:
            print('=>', end=' ')
            print(weights[path[i], path[i + 1]], 'km', end=' ')
            print('=>', end=' ')

    print('(overall:', length, 'km)', '\n')


if __name__ == '__main__':

    # Open json file
    entfernungen = json.load(open('entfernungen.json', encoding="utf-8"))

    # create data from
    graph, names, weights, numbers, air_distance = createGraph(entfernungen)

    # print paths with dijkstra algorithm
    print_path(graph, weights, numbers, 'Aachen', 'Passau')
    print_path(graph, weights, numbers, 'Saarbrücken', 'Leipzig')
    print_path(graph, weights, numbers, 'München', 'Greifswald')
    print_path(graph, weights, numbers, 'Konstanz', 'Kassel')

    # print paths with a-star algorithm
    print_path_astar(graph, weights, air_distance, numbers, 'Aachen', 'Passau')
    print_path_astar(graph, weights, air_distance, numbers,  'Saarbrücken', 'Leipzig')
    print_path_astar(graph, weights, air_distance, numbers,  'München', 'Greifswald')
    print_path_astar(graph, weights, air_distance, numbers,  'Konstanz', 'Kassel')

    # Assert that the same way for the routes are found with both algorithms
    path_1, length_1 = dijkstra(graph, weights, numbers['Aachen'], numbers['Passau'])
    path_2, length_2 = a_star(graph, weights, air_distance, numbers['Aachen'], numbers['Passau'])
    assert (path_1 == path_2), "Route is not the same!"
    path_1, length_1 = dijkstra(graph, weights, numbers['Saarbrücken'], numbers['Leipzig'])
    path_2, length_2 = a_star(graph, weights, air_distance, numbers['Saarbrücken'], numbers['Leipzig'])
    assert (path_1 == path_2), "Route is not the same!"
    path_1, length_1 = dijkstra(graph, weights, numbers['München'], numbers['Greifswald'])
    path_2, length_2 = a_star(graph, weights, air_distance, numbers['München'], numbers['Greifswald'])
    assert (path_1 == path_2), "Route is not the same!"
    path_1, length_1 = dijkstra(graph, weights, numbers['Konstanz'], numbers['Kassel'])
    path_2, length_2 = a_star(graph, weights, air_distance, numbers['Konstanz'], numbers['Kassel'])
    assert (path_1 == path_2), "Route is not the same!"

    print("\n\nIf you can read this, it is assured that both algorithms are using the same route!")

