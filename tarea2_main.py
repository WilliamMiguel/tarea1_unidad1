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


def option02(info = info):
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


def generator(limitInf, limitSup):
    url = "https://pokeapi.co/api/v2/ability/"
    for i in range(limitInf, limitSup + 1):
        yield url+str(i)

def isNumber(text):
    while True:
        value = input(text)
        if value.isnumeric():
            break
    return int(value)

def option03(info = info):
    print("\nINGRESA EL RANGO DE ID DE HABILIDADES QUE DESEAS VISUALIZAR...\n")
    while True:
        limitInf = isNumber("Ingresa el ID inferior: ")
        limitSup = isNumber("Ingresa el ID superior: ")
        if limitSup > limitInf:
            break
        print("Ingresa un ID superior mayor al ID inferior")
    
    print("\nBUSCANDO POKEMONES...\n")

    ability = info["ability"]
    respAbility = requests.get(ability).json()
    # countAbility = respAbility["count"]
    abilityGenerator = generator(limitInf, limitSup)
    nameAbility =[]
    pokeAbility = []
    for ability in range(limitInf,limitSup + 1):
        urlAbility = next(abilityGenerator)
        if requests.get(urlAbility).status_code != requests.codes.ok:
            break
        jsonAbility = requests.get(urlAbility).json()
        name = jsonAbility["name"].capitalize()
        nameAbility.append(name)
        pokemons = [pokemon["pokemon"]["name"].capitalize() for pokemon in jsonAbility["pokemon"]]
        pokeAbility.append(pokemons)
    
    if len(nameAbility) == 0:
        print("No se encontró información entre los IDs especificados")
    else:
        tupleAbilities = zip(nameAbility,pokeAbility)
        print(tabulate(tupleAbilities, headers=["Habilidad", "Pokemones"]))

    print("\nCARGA COMPLETA")


option03(info)