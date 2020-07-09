'''
Christopher Höllriegl, Marvin Schmitt
Blatt 7
'''

import json
import random
import re

ignore_list = [
    # Decoration-Meme? :D
    "cocktailkirsche",
    "cocktailtomate",
    "rosenblüte", # yo, wtf xD
    "kaffeebohnen",
    "stielkirsche",
    # zu allgemein:
    "wasser",
    "pfeffer",
    "salz",
    "zucker",
    "obst",
    "fruechte",
    "likoer",
    "saftvontropischenfruechten",
    "fruchtsaft",
    "beeren",
    "sirup",
    "suessigkeiten",
    "schnaps",
    # Dinge die nicht nötig sind oder leicht zu ersetzen:
    "kekse",
    "waffeln",
    "kokosnuss",
    "limettenscheibe",
    "orangenschale",
    "orangenscheibe",
    "salzstangen",
    "staudensellerie", # WER TRINKT SOLCHE DINGE?!?
    "zitronengras",

]

#aufgabe a)
def normalizeString(s):
    '''
        normalizes a string
        :param s: string to normalize
        :return: normalized string
        '''

    # remove things in brackets
    s = s.split(" (")[0]

    # make lowercase
    s = s.lower()

    # remove special characters with regex
    re.sub(r"[^a-zA-Z0-9äüöÄÜÖß]+", ' ', s)

    return s

def all_ingredients(recipes):
    '''
    Create a list of all ingredients
    :param recipes: recipes
    :return: list of ingredients
    '''
    ingredients = []

    for key_1, value_1 in recipes.items():
        for key_2, value_2 in value_1.items():
            if key_2 == "ingredients":
                for key_3, value_3 in value_2.items():
                    key = normalizeString(key_3)
                    if key not in ingredients:
                        ingredients.append(key)
    return ingredients

#Aufgabe b)
def cocktails_inverse(recipes):
    '''
    Inverse the cocktail list so that the key is now 'ingredient'
    :param recipes: List of recipes
    :return: Inversed recipe list
    '''
    inverse = {}


    for key_1, value_1 in recipes.items():
        for key_2, value_2 in value_1.items():
            if key_2 == "ingredients":
                for key_3, value_3 in value_2.items():
                    key = normalizeString(key_3)
                    # initialise the list if a new ingredient is found
                    if key not in inverse:
                        inverse[key] = []
                    # check if there are duplicates, just in case.
                    if key_1 not in inverse[key]:
                        inverse[key].append(key_1)
    return inverse

#aufgabe c)
def possible_cocktails(inverse_recipes, available_ingredients):
    '''
    Find the cocktails you can make with the available ingredients
    :param inverse_recipes: Inverse recipe list
    :param available_ingredients: ingredients which are available
    :return: list ok possible cocktails
    '''
    temp = []
    invalid = []
    possible = []

    # make a list with cocktails with >= 1 available ingredients
    for key1 in available_ingredients:
        for cocktail in inverse_recipes[key1]:

            # make sure there are not duplicates
            if cocktail not in temp:
                temp.append(cocktail)

    # Now make a list with ingredients that are NOT available
    for key2, value2 in inverse_recipes.items():
        if key2 not in available_ingredients:
            for t in temp:
                # If we now check if a cocktail has an ingredient, which is NOT available, we can create a list with
                # cocktails that are not possible
                if t in value2:
                    if t not in invalid:
                        invalid.append(t)

    # now create the final list with possible cocktails
    for t in temp:
        if t not in invalid:
            possible.append(t)

    return possible


# Aufgabe d)
def optimal_ingredients(inverse_recipes):
    '''
    try to find the optimal ingredients to have for cocktails
    :param inverse_recipes: inverse recipe list
    '''
    counter = 0
    counter_max = 0
    possible_max = []
    ingredients = list(inverse_recipes.keys())
    ingredients_max = []

    # TODO Abbruchbedingung auf 30.000 gesetzt.
    cancel = 30000

    # loop
    while counter < cancel:
        # print the counter
        if not counter % 250:
            print("Still working: {} / {} checks done.".format(counter, cancel))
        # get new randomized ingredients
        available_ingredients = randomize(ingredients, 5)

        # work with former function
        possible = possible_cocktails(inverse_recipes, available_ingredients)

        # compare the length to set a new possible max and increate the counter
        if len(possible) > len(possible_max):
            possible_max = possible
            ingredients_max = available_ingredients
            counter_max = counter
        # increase the loop counter
        counter = counter + 1
    # print a solution because we don't work further with the data.
    print(counter_max, ingredients_max, possible_max)

def randomize(inverse, n):
    '''
    Helper function to randomize the ingredients to test
    '''
    available = []
    secure_random = random.SystemRandom()

    for i in range(0, n):
        available.append(secure_random.choice(inverse))
    return available


def main():
    # Load the json, don't forget encoding!!
    recipes = json.load(open('cocktails.json', 'r', encoding="utf-8"))

    # Number of all ingredients
    print("Number of ingredients overall: ", len(all_ingredients(recipes)))

    # Print all ingredients
    print(all_ingredients(recipes))

    # instruction from the sheet
    inverse_recipes = cocktails_inverse(recipes)

    # dump the data as a json file
    json.dump(inverse_recipes, open('cocktails_inverse.json', 'w', encoding='utf-8'))


    # Remove the things from the ignore list, whether they are too common or mostly unavailable
    remove = []
    for key in inverse_recipes.keys():
        if key in ignore_list:
            remove.append(key)
    for key in remove:
        del inverse_recipes[key]

    print("\nNumber of ingredients after ignore-purge: ", len(inverse_recipes))

    # try possible_cocktails
    print("\nIf we have grapefruit, ribiselsirup and ananas, what can we make?")
    print(possible_cocktails(inverse_recipes, {"grapefruit", "ribiselsirup", "ananas"}))

    # optimal ingredients
    print("\nTry to find the 5 optimal ingredients:")
    print(optimal_ingredients(inverse_recipes))


if __name__ == "__main__":
    main()