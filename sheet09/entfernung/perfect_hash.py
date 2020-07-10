'''
Christopher Höllriegl, Marvin Schmitt
Blatt09, Aufgabe 3
'''

import json
import random
from typing import List # Int Lists, don't forget ^.^

class PerfectHash:
    '''
    Create a dictionary of city names and their "perfect" hashes
    '''
    graph = []
    edges = dict()
    t1: List[int] = []
    t2: List[int] = []

    n = 0
    length = 0
    helper = []

    def __init__(self, names):
        '''
        Constructor for the PerfectHash class
        :param names: city names, here from json
        '''

        # set the length and the max size
        self.length = len(names)
        self.n = int(self.length * 2 + 1)

        # create the acyclic graph
        self.createAcyclyc(names)

        # Traverse like described in the pdf
        self.traverse()

    # Call Method
    def __call__(self, name):
        '''
        Return the hash for a city
        :param name: city the hash is for
        :return: the hash of the city
        '''
        u = self.f1(name)
        v = self.f2(name)
        return (self.g(u) + self.g(v)) % self.length

    # f1 and f2 from the PDF
    def f1(self, w):
        u = 0
        for i in range(len(w)):
            u += self.t1[i] * ord(w[i])
        return u % self.n

    def f2(self, w):
        v = 0
        for i in range(len(w)):
            v += self.t2[i] * ord(w[i])
        return v % self.n

    # helper function
    def g(self, node):
        return self.helper[node]


    # from pseudo code from the ?book/pdf?
    def traverse(self):
        '''
        go through the graph
        '''
        self.helper = [0] * self.n
        visited = [False] * len(self.graph)

        # AlDa Wiki / Stackoverflow says it's ok to declare functions in functions, much easier recursion. never seen this before
        def visit(node):
            if not visited[node]:
                visited[node] = True
                for w in self.graph[node]:
                    if not visited[w]:
                        h = 0
                        if (node, w) in self.edges:
                            h = self.edges[(node, w)]
                        else:
                            h = self.edges[(w, node)]
                        self.helper[w] = (h - self.g(node)) % self.length

                        visit(w)

        for node in range(len(self.graph)):
            if not visited[node] and (len(self.graph[node]) > 0):
                visit(node)

    def createAcyclyc(self, w):
        '''
        create an acyclic graph
        :param w: names for the graph
        '''
        # As long as graph is acyclic
        while PerfectHash.isAcyclyc(self.graph):
            self.graph = [[] for i in range(self.n)]
            self.edges = dict()
            self.t1 = generateRandomTable(self.n, 40)
            self.t2 = generateRandomTable(self.n, 40)
            for i in range(len(w)):
                # calculate f1 and f2
                u = self.f1(w[i])
                v = self.f2(w[i])

                if v == u and v not in self.graph[u]:
                    if u not in self.graph[v]:
                        self.graph = []
                        break   # Abbruchbedingung

                # Append to the graph and update the edges!
                # fixed, just had to do this inside the for loop q.q
                self.graph[u].append(v)
                self.graph[v].append(u)
                self.edges[(u, v)] = i % self.length

    # from Alda wiki, topological_sort, modified
    def isAcyclyc(g):
        '''
        returns wheter a graph is acyclic or not
        :param g: graph to check
        '''
        if len(g) == 0:
            return True
        visited = [False] * len(g)

        def visit(node, from_node):
            if not visited[node]:
                visited[node] = True
                for neighbor in g[node]:
                    if neighbor == from_node:
                        continue
                    if visit(neighbor, node):
                        return True
                return False
            else:
                return True

        for node in range(len(g)):
            if not visited[node] and len(g[node]) > 0:
                if visit(node, node):
                    return True
        return False

# thanks to Stackoverflow
def generateRandomTable(n, c):
    '''
    create a list with random integers between 0 and n
    :param n: max
    :param c: count
    :return: list with random integers
    '''
    return [random.randint(0, n - 1) for i in range(c)]


def main():
    # Load JSON File
    entfernungen = json.load(open('entfernungen.json', 'r', encoding="utf-8"))

    # create a List of the names as we only need them
    cities = [key for key, value in entfernungen.items()]

    # create the "perfect" hash object
    hash = PerfectHash(cities)

    # Print all cities
    print("All cities with their hashes: ")
    for i in range(len(cities)):
        print(hash(cities[i]), " - ", cities[i])
        #if hash(cities[i]) == 11:
           #print("Gibts gar nicht!!")

    testCity = "Mannheim"

    print("Hash for ", testCity, " : ", hash(testCity))
    print("Get the city from the hash of ", testCity, " : ", cities[hash("Mannheim")])

if __name__ == "__main__":
    main()