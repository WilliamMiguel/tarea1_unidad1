from tabulate import tabulate
import os
import requests
import json
os.system("cls")
# os.system("pip install tabulate")

url = "https://pokeapi.co/api/v2/"
resp = requests.get(url)
info = resp.json()


def abilitiesPokemons(pokemons: list) -> list:
    abilitiesofPokemons = []
    for pokemon in pokemons:
        url = "https://pokeapi.co/api/v2/pokemon/"
        try:
            info = requests.get(url + pokemon.lower()).json()
        except:
            abilitiesofPokemons.append(["No hay información"])
            continue
        else:
            abilities = [ability["ability"]["name"]
                         for ability in info["abilities"]]

            abilitiesofPokemons.append(abilities)

    return abilitiesofPokemons


def option02(info=info):
    shape = info["pokemon-shape"]
    respShape = requests.get(shape).json()
    countShapes = respShape["count"]
    optionsShapes = [str(option + 1) for option in range(countShapes)]
    print("Elige la forma de pokemones...\n")
    for index, shape in enumerate(respShape["results"], 1):
        print("    Opción " + str(index) + ": " + shape["name"].capitalize())

    print()
    while True:
        selectionShape = input("Ingresa una opción: ")
        if selectionShape in optionsShapes:
            selectionShape = int(selectionShape)
            break

    urlShape = respShape["results"][int(selectionShape)-1]["url"]
    jsonShape = requests.get(urlShape).json()
    pokemons = [pokemon["name"].capitalize()
                for pokemon in jsonShape["pokemon_species"]]
    print(f"\nENCONTRAMOS {len(pokemons)} POKEMONES")
    print(f"\nCARGANDO SUS HABILIDADES...\n")
    abilities = abilitiesPokemons(pokemons)
    tuplePokemons = zip(pokemons, abilities)
    fieldnames = ["Pokemon", "Habilidades"]
    print(tabulate(tuplePokemons, headers=fieldnames))

# option02(info)


# ------------------------Opción 3-----------------------------------


def option03(info=info):
    urlAbility = info["ability"]

    respAbility = requests.get(urlAbility).json()
    countAbilities = respAbility["count"]
    urlAllAbilities = "https://pokeapi.co/api/v2/ability/?offset=0&limit=" + \
        str(countAbilities)
    jsonAbilities = requests.get(urlAllAbilities).json()

    firstLetter = input("Ingresa la primera letra de la habilidad: ")
    print("\nBUSCANDO POKEMONES...\n")
    listabilities = []
    listPokemons = []
    for ability in jsonAbilities["results"]:
        if ability["name"][0] == firstLetter:
            listabilities.append(ability["name"])
            jsonPokemons = requests.get(urlAbility + ability["name"]).json()
            pokemons = [pokemon["pokemon"]["name"] for pokemon in jsonPokemons["pokemon"]]
            if pokemons == []:
                listPokemons.append("No hay información")
            else:
                listPokemons.append(pokemons)

    print(listabilities)
    print("-----------------------------------")
    print(listPokemons)


option03(info)
