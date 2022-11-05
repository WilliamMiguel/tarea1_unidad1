import os
import requests
import json
os.system("cls")
#os.system("pip install tabulate")
from tabulate import tabulate

url = "https://pokeapi.co/api/v2/"
resp = requests.get(url)
info = resp.json()

#-------------------------------------------- Cargando Las Habilidades de los Pokemones  --------------------------------------------
def abilitiesPokemons(pokemons: list) -> list:
    abilitiesofPokemons = []

    for pokemon in pokemons:
        url = "https://pokeapi.co/api/v2/pokemon/"
        info: dict = requests.get(pokemon).json()
        abilities = []

        if ("varieties" in info) :
            nameDefault = info["varieties"][0]["pokemon"]["name"]
            jsonabilities = requests.get(url + nameDefault).json()
            abilities = [ability["ability"]["name"] for ability in jsonabilities["abilities"]]
        else :
            abilities = [ability["ability"]["name"] for ability in info["abilities"]]
        
        abilitiesofPokemons.append(abilities)

    return abilitiesofPokemons

#-------------------------------------------- Opción 02 --------------------------------------------
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
    pokemons = [pokemon["name"].capitalize() for pokemon in jsonShape["pokemon_species"]]
    urlPokemons = [pokemon["url"] for pokemon in jsonShape["pokemon_species"]]

    print(f"\nENCONTRAMOS {len(pokemons)} POKEMONES")
    print(f"\nCARGANDO SUS HABILIDADES...\n")
    abilities = abilitiesPokemons(urlPokemons)
    tuplePokemons = zip(pokemons, abilities)
    fieldnames = ["Pokemon", "Habilidades"]
    print(tabulate(tuplePokemons, headers=fieldnames))

option02(info)

#-------------------------------------------- Opción 03 --------------------------------------------
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


#option03(info)

# ------------------------Opción 05-----------------------------------
def option05(info: dict = info) -> None: 
    urlType = info["type"]

    resultType: dict = requests.get(urlType).json()
    types: dict = resultType["results"]
    numberType: str = 0
    listTypesNumbers: range =  range(1, resultType['count'] + 1)

    print(f"Selecciona el tipo de pokemon a listar, se cuenta con {resultType['count']} tipos:\n")

    for index, typeP in enumerate(types, start = 1):
        print("    Opción " + str(index) + ": " + typeP["name"].capitalize())
    
    numberType =  input("\nIngrese el número de tipo a listar: ")

    while True:
        if (not(numberType.isnumeric()) or int(numberType) not in listTypesNumbers):
            numberType = input(f"Opción inválida el {numberType} no se encuentra en la lista de los tipos de pokemones. Ingrese nuevamente el número de tipo a listar: ")
            continue

        numberType: int = int(numberType) - 1
        break

    nameType = types[numberType]["name"]
    urlPokemonType = types[numberType]["url"]
        
    # ---- Obteniendo las habilidades de los pokemones
    resultPokemons: dict = requests.get(urlPokemonType).json()

    pokemonsNames = [pokemon["pokemon"]["name"].capitalize() for pokemon in resultPokemons["pokemon"]]
    urlPokemons = [pokemon["pokemon"]["url"] for pokemon in resultPokemons["pokemon"]]
    pokemonsAbilities = []

    if (not urlPokemons):
        print(f"\nNo hay pokemones del tipo {nameType}")
        return

    print(f"\nENCONTRAMOS {len(pokemonsNames)} POKEMONES")
    print(f"\nCARGANDO SUS HABILIDADES ...\n")

   #for url in urlPokemons:
   #    infoPokemon = requests.get(url).json()
   #    pokemonsAbilities.append([pokemonAbility["ability"]["name"] for pokemonAbility in infoPokemon["abilities"]])

    pokemonsAbilities = abilitiesPokemons(urlPokemons)
    tuplePokemons = zip(pokemonsNames, pokemonsAbilities)
    fieldnames = ["Pokemon", "Habilidades"]

    print(tabulate(tuplePokemons, headers=fieldnames) + "\n")
#option05()
