import os
import requests
import json
import pandas as pd
os.system("cls")
# os.system("pip install tabulate")
from tabulate import tabulate

url = "https://pokeapi.co/api/v2/"
resp = requests.get(url)
info = resp.json()

shape = info["pokemon-shape"]
respShape = requests.get(shape).json()
countShapes = respShape["count"]
optionsShapes = [str(option + 1) for option in range(countShapes)]
print("Elige la forma de pokemones...\n")
for index, shape in enumerate(respShape["results"], 1):
    print("    Opción " + str(index) + ": " + shape["name"].capitalize())

while True:
    selectionShape = input("\nIngresa una opción: ")
    if selectionShape  in optionsShapes:
        selectionShape = int(selectionShape)
        break
    # selectionShape = 0

urlShape = respShape["results"][int(selectionShape)]["url"]
jsonShape = requests.get(urlShape).json()
pokemons = [pokemon["name"].capitalize() for pokemon in jsonShape["pokemon_species"]]

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
            abilities = [ability["ability"]["name"] for ability in info["abilities"]]

            abilitiesofPokemons.append(abilities)

    return abilitiesofPokemons

print(f"\nENCONTRAMOS {len(pokemons)} POKEMONES")
print(f"\nCARGANDO SUS HABILIDADES...\n")
abilities = abilitiesPokemons(pokemons)
tuplePokemons = zip(pokemons,abilities)
fieldnames = ["Pokemon","Habilidades"]
print(tabulate(tuplePokemons,headers = fieldnames))
