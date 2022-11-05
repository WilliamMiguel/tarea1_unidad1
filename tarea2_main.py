import os
import requests
import json
os.system("cls")
os.system("pip install tabulate")
from tabulate import tabulate

url = "https://pokeapi.co/api/v2/"
resp = requests.get(url)
info = resp.json()


def abilitiesPokemons(pokemons: list) -> list:
    abilitiesofPokemons = []
    for pokemon in pokemons:
        url = "https://pokeapi.co/api/v2/pokemon/"
        info = requests.get(pokemon).json()
        nameDefault = info["varieties"][0]["pokemon"]["name"]
        jsonabilities = requests.get(url + nameDefault).json()
        abilities = [ability["ability"]["name"] for ability in jsonabilities["abilities"]]
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
    pokemons = [pokemon["name"].capitalize() for pokemon in jsonShape["pokemon_species"]]
    urlPokemons = [pokemon["url"] for pokemon in jsonShape["pokemon_species"]]

    print(f"\nENCONTRAMOS {len(pokemons)} POKEMONES")
    print(f"\nCARGANDO SUS HABILIDADES...\n")
    abilities = abilitiesPokemons(urlPokemons)
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

    while True:
        firstLetter = input("Ingresa la primera letra de la habilidad: ").lower()
        if firstLetter.isalpha() and len(firstLetter) == 1:
            break
        
    print("\nBUSCANDO POKEMONES...\n")
    listAbilities = []
    listPokemons = []
    for ability in jsonAbilities["results"]:
        if ability["name"][0] == firstLetter:
            listAbilities.append(ability["name"].capitalize())
            jsonPokemons = requests.get(urlAbility + ability["name"]).json()
            pokemons = [pokemon["pokemon"]["name"] for pokemon in jsonPokemons["pokemon"]]
            if pokemons == []:
                listPokemons.append("No hay información")
            else:
                listPokemons.append(pokemons)
    
    if listAbilities == []:
        print(f"No encontramos pokemones con habilidades que empiezan por {firstLetter.upper()}")
    else:
        fieldnames = ["Habilidad", "Pokemones"]
        tuplePokemons = zip(listAbilities,listPokemons)
        print(tabulate(tuplePokemons,fieldnames))


option03(info)
