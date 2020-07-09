'''
Christopher Höllriegl, Marvin Schmitt
Blatt 7 Aufgabe 1
'''

import json
import re

ignore = {'wasser', 'eiswürfel'}

#Aufgabe a)

# Read the recipes file and store the json object
# Finally... forgot to set utf-8 flag
with open('cocktails.json', encoding='utf-8') as data:
    recipes = json.load(data)


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

    # for every cocktail in the recipes
    for cocktail in recipes:
        # go through every ingredient
        for ingredient in recipes[cocktail]["ingredients"]:
            ingredients.append(normalizeString(ingredient))

    # use list as set because of duplicates
    return list(set(ingredients))

#Aufgabe b)

def cocktails_inverse(recipes):
    dictionary = {"":[]}

    # create a list of all ingredients
    ingredients = all_ingredients(recipes)

    # now add every ingredient to the dictionary
    for ingredient in ingredients:
        dictionary.update({ingredient: []})

        # add every cocktail to the ingredient if needed.
        for cocktail in recipes:
            name = cocktail
            if contains_word(" ".join(recipes[cocktail]["ingredients"]).lower(), ingredient):
                dictionary[ingredient].append(name)
    return dictionary

# from stackoverflow because there are no 478 cocktails containing "ei"
def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

def ingredient_count(inverse_recipes):
    counts = {"": 0}

    # count
    for ingredient in inverse_recipes:
        counts.update({ingredient: len(inverse_recipes[ingredient])})

    return counts

#Aufgabe c)
#Wäre die Aufgabe nicht sinnvoller, wenn man mit der normalen Rezeptliste arbeitet anstatt der invertierten?

def possible_cocktails(inverse_recipes, available_ingredients):
    possible_recipes = list()

    for ingredient in available_ingredients:
        ingredient = normalizeString(ingredient)
        if ingredient in inverse_recipes:
            for recipe in inverse_recipes[ingredient]:
                if recipe not in possible_recipes:
                    possible_recipes.append(recipe)
    for ingredient in inverse_recipes.keys():
        if len(possible_recipes) == 0: break
        if ingredient not in available_ingredients and ingredient not in ignore:
            for recipe in inverse_recipes[ingredient]:
                if recipe in possible_recipes:
                    possible_recipes.remove(recipe)

    return possible_recipes

if __name__ == "__main__":
    # Number of all ingredients
    print("Number of ingredients overall: ", len(all_ingredients(recipes)))

    # Print all ingredients
    print(all_ingredients(recipes))

    # instruction from the sheet
    inverse_recipes = cocktails_inverse(recipes)

    # dump the data as a json file
    json.dump(inverse_recipes, open('cocktails_inverse.json', 'w', encoding='utf-8'))

    # print the 15 most used ingredients
    ingredients = ingredient_count(inverse_recipes)
    print("\nIngredients in number of cocktails:")
    n = 0
    for item in sorted(ingredients, key=ingredients.get, reverse=True):
        print(item, ingredients[item])
        #if n < 15:
            #print(item, ingredients[item])
        #n += 1

    possible_cocktails(inverse_recipes, {"Grapefruit", "Ribiselsirup", "Ananas"})


