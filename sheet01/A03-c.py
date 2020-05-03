# In welchem Modul befindet sich die Funktion sqrt() für die Quadratwurzel, und wie importiert und verwendet man diese Funktion?
# Im Modul math
from math import sqrt

# Was passiert, wenn man sqrt() mit einer negativen Zahl aufruft?
# sqrt(-1) # Throws ValueError: math domain error 

# Implementieren Sie eine Funktion mysqrt(), die stattdessen die Ausgabe „mysqrt() funktioniert nicht für negative Zahlen, du Dussel!“ anzeigt (zwei Antworten: benutzen Sie if: ... else: sowie try: ... except: )!
def mysqrt(i, mode = "ifelse"):
    if mode == "ifelse":
        if i < 0:
            return "mysqrt() funktioniert nicht für negative Zahlen, du Dussel!"
        else:
            return sqrt(i)

    elif mode == "tryexcept":
        try:
            return sqrt(i)
        except ValueError:
            return "mysqrt() funktioniert nicht für negative Zahlen, du Dussel!"
    else:
        return "invalid mode..."


print(mysqrt(4))
print(mysqrt(-1))
print(mysqrt(-1, mode = "tryexcept"))

## Schreiben Sie eine Schleife, die die Variable i von -10 bis +10 (inklusive) inkrementiert, und geben Sie bei jeder Iteration den Wert i sowie das Ergebnis von i % 5 („i modulo 5“) aus. Erklären Sie die Ausgabe (d.h. die Funktionsweise des Modulo-Operators).
print([[i, i%5] for i in range(-10, 11)]) 
# Der Modulo-Operator gibt den Rest bei Ganzzahldivision aus. Er ist mit "x mod n, x aus Z" eine elegante Implementierung des Rings Z/nZ

## Wann sollte man einen String in dreifache Anführungszeichen (''') einschließen?
myAnswer = '''
Wenn man einen String
über mehrere Zeilen
strecken will, um ihn lesbarer
für
Menschen 
zu 
machen, nutzt man drei 
A
n
f
ü
h
r
u
n
g
s
z
e
i
c
h
e
n.
'''
print(myAnswer)

## Worin besteht der Unterschied zwischen der Klasse list und der Klasse dict?
# list: einfaches Array bzw. Stack bzw. Heap
# dict: assoziatives Array

## Wozu dient die __init__()-Funktion einer Klasse und wie benutzt man sie?
# Konstruktur der Klasse. Nutzung im Code über myCarObject = Car(a, b, c)