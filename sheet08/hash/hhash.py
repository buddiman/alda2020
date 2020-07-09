'''
Christopher Höllriegl, Marvin Schmitt
Blatt08, Aufgabe 2
'''

def hhash(s): # s ist ein Schlüssel vom Typ string
    h = 0 # der Hashwert wird mit 0 initialisiert
    for k in s:
        h = 23*h + ord(k) # Aktualisieren des Hashs mit dem Zeichencode
    return h

def createPossibleKeys():
    '''
    create a list of all possible strings from 4 characters
    strings can consist of capital and small letters and numbers
    :return: list of possible strings
    '''
    alphabet = [chr(c) for c in range(48,123) if c not in range(91,97) and c not in range(58, 65)] # exclude non-characters
    result = []
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            for k in range(len(alphabet)):
                for l in range(len(alphabet)):
                    word = alphabet[i] + alphabet[j] + alphabet[k] + alphabet[l]
                    result.append(word)
    return result

def getKeysWithCollisionsLength(length):
    words = createPossibleKeys()
    seenHashes = []
    for word in words:
        wordHash = hhash(word)
        seenHashes.append((word, wordHash))
    sortedHashes = sorted(seenHashes, key=lambda x: x[1]) # (*)


    repeatedHashes = {}
    for i in range(len(sortedHashes)):
        prevHash, actualHash, actualWord,nextWord = sortedHashes[i-1][1], sortedHashes[i][1], sortedHashes[i-1][0], sortedHashes[i][0]
        if prevHash == actualHash: # (**)
            if not prevHash in repeatedHashes.keys():
                repeatedHashes[prevHash] = {actualWord, nextWord}
            else:
                repeatedHashes[prevHash].add(actualWord)
                repeatedHashes[prevHash].add(nextWord)
    return dict((key,value) for key,value in repeatedHashes.items() if len(value) == length) # (***)

def main():
    print(getKeysWithCollisionsLength(16))

if __name__ == "__main__":
    main()