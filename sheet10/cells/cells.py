#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 14:45:21 2020

@author: marvin
"""

hints = '''
 write_pgm(width, height, data, 'mein_bild.pgm')
 value = data[x + y*width]
 data[x + y*width] = value
 index = x + y*width
 x, y = index % width, index // width # ... und Pixelindex
 '''

from pgm import read_pgm, write_pgm
from itertools import compress
import numpy as np



def create_mask(width, height, data, threshold):
    # return list of same length with threshold-filter
    # multiply each value with 255 so that {0,1} -> {0,255}
    return [(p > threshold)*255 for p in data]

def create_graph(width, height, mask):
    # Initialize adjacence list
    graph = [[] for p in mask]
    
    # iterate over each pixel and build graph
    for index in range(len(graph)):
        x, y = index % width, index//width # get x,y
        value = mask[index] # get value
        
        # check pixels in 4-neighborhood
        # top
        if y > 0:
            index2 = x + (y-1)*width
            value2 = mask[index2]
            if value==value2: graph[index].append(index2)
            
        # left
        if x > 0:
            index2 = (x-1) + y*width
            value2 = mask[index2]
            if value==value2: graph[index].append(index2)
        
        # right
        if x < (width-1):   
            index2 = (x+1) + y*width
            value2 = mask[index2]
            if value==value2: graph[index].append(index2)
        
        # bottom
        if y < (height-1):
            index2 = x + (y+1)*width
            value2 = mask[index2]
            if value==value2: graph[index].append(index2)
    
    return graph



def components(graph):

    
    def unionFindConnectedComponents(graph):
        def findAnchor(anchors, node):
            start = node                   # wir merken uns den Anfang der Kette
            while node != anchors[node]:   # wenn node kein Anker ist
                 node = anchors[node]       # ... verfolge die Ankerkette weiter
            anchors[start] = node          # Pfadkompression: aktualisiere den Eintrag am Anfang der Kette
            return node
        
        
        
        anchors = list(range(len(graph)))  # Initialisierung der property map: jeder Knoten ist sein eigener Anker
        for node in range(len(graph)):     # iteriere über alle Knoten
            for neighbor in graph[node]:   # ... und über deren ausgehende Kanten
                if neighbor < node:        # ignoriere Kanten, die in falscher Richtung verlaufen
                    continue
                # hier landen wir für jede Kante des Graphen genau einmal
                a1 = findAnchor(anchors, node)       # finde Anker ...
                a2 = findAnchor(anchors, neighbor)   # ... der beiden Endknoten
                if a1 < a2:                          # Verschmelze die beiden Teilgraphen
                    anchors[a2] = a1                 # (verwende den kleineren der beiden Anker als Anker des
                elif a2 < a1:                        #  entstehenden Teilgraphen. Falls node und neighbor 
                    anchors[a1] = a2                 #  den gleichen Anker haben, waren sie bereits im gleichen
                                                     #  Teilgraphen, und es passiert hier nichts.)
        # Bestimme jetzt noch die Labels der Komponenten
        labels = [None]*len(graph)         # Initialisierung der property map für Labels
        current_label = 0                  # die Zählung beginnt bei 0
        for node in range(len(graph)):
            a = findAnchor(anchors, node)  # wegen der Pfadkompression zeigt jeder Knoten jetzt direkt auf seinen Anker
            if a == node:                  # node ist ein Anker
                labels[a] = current_label  # => beginne eine neue Komponente
                current_label += 1         # und zähle Label für die nächste ZK hoch
            else:
                labels[node] = labels[a]   # node ist kein Anker => setzte das Label des Ankers
                                           # (wir wissen, dass labels[a] bereits gesetzt ist, weil 
                                           #  der Anker immer der Knoten mit der kleinsten Nummer ist)
        return anchors, labels
    
    anchors, labeling = unionFindConnectedComponents(graph)
    count = len(set(labeling))
    return labeling, count


def get_size(labeling):
    sizes = [None] * len(set(labeling))
    for i in range(len(set(labeling))):
        sizes[i] = labeling.count(i)
        
    return sizes


def get_max_intensity(data, labeling):
    intensities = [None] * len(set(labeling))
    for i in range(len(set(labeling))):
        component_mask = [p==i for p in labeling]
        pixel_values = list(compress(data, component_mask))
        intensities[i] = max(pixel_values)
        #intensities[i] = max(data[component_mask])
        
    return intensities

def segment(labeling, size, intensity):
    # finally use numpy for convenient bool slicing...
    labeling = np.array(labeling)
    segmentation = np.array([None] * len(labeling))
    
    # iterate over labels, slie
    for label in range(len(set(labeling))):
        if label == 0: 
            segmentation[labeling==label] = 0
        elif size[label] < 30: 
            segmentation[labeling==label] = 255
            
        elif intensity[label] > 220: 
            segmentation[labeling==label] = 160
            
        else:
            segmentation[labeling==label] = 80
    
    return segmentation

if __name__ == '__main__':
    width, height, data = read_pgm('cells.pgm') 
    
    print(f"First 50 entries of data:\n{data[:50]}\n\n")
    

    
    mask = create_mask(width, height, data, 60)
    print(f"Some 50 entries of mask:\n{mask[4700:4750]}\n\n")
    write_pgm(width, height, mask, 'mask.pgm')
    
    g = create_graph(width, height, mask)
    
    g_labeling, g_count = components(g)
    print(f"There is one background component and {g_count-1} other (cell) components.\n")
    write_pgm(width, height, g_labeling, 'labeling.pgm')

    
    g_size = get_size(g_labeling)
    print(f"Component sizes:\n{g_size}\n")
    
    g_intensity = get_max_intensity(data, g_labeling)
    print(f"Max Intensities:\n{g_intensity}\n")
    
    print("Image stats:")
    print(f"{g_size[0]/len(data) * 100:.1f}% are background.")
    print(f"There are {sum([s<30 for s in g_size])} regions with less than 30 pixels.")
    print(f"There are {sum([i>220 for i in g_intensity])} regions with max intensity > 220 (white cores).")

    g_segmentation = segment(g_labeling, g_size, g_intensity)
    write_pgm(width, height, g_segmentation, 'segmentation.pgm')

    