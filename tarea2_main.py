import os
import re
import requests
import json
os.system("cls")
#os.system("pip install tabulate")
from tabulate import tabulate

url = "https://pokeapi.co/api/v2/"
resp = requests.get(url)
info = resp.json()

def isNumber(text: str):
    while True:
        value = input(text)
        if value.isnumeric():
            value = int(value)
            break
    return value

def infoPokemons(pokemons: list, selection: str, firstLimit, secondLimit: int) -> list:
    dataPokemons = []
    imagePokemons = []
    numberPokemon = firstLimit

    for pokemon in range(firstLimit, secondLimit):
        url = "https://pokeapi.co/api/v2/pokemon/"
        info = requests.get(pokemons[numberPokemon]).json()

        if ("varieties" in info):
            nameDefault = info["varieties"][0]["pokemon"]["name"]
            jsonData = requests.get(url + nameDefault).json()
        else:
            jsonData = info

        if selection == "abilities":
            dataAbilities = [data["ability"]["name"] for data in jsonData["abilities"]]
            dataPokemons.append(dataAbilities)
        
        dataImages = jsonData["sprites"]["back_default"]
        
        if dataImages == None:
            imagePokemons.append("Sin imagen")
        else:
            imagePokemons.append(dataImages)

        numberPokemon += 1
        
    return dataPokemons, imagePokemons

# ------------------------Opción 02 -----------------------------------
def option02(info=info):
    shape = info["pokemon-shape"]
    respShape = requests.get(shape).json()
    countShapes = respShape["count"]
    optionsShapes = [str(option + 1) for option in range(countShapes)]

    print("Elige la forma de pokemones...\n")
    
    for index, shape in enumerate(respShape["results"], 1):
        print("    " + str(index) + ": " + shape["name"].capitalize())

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
    numbersPokemons = len(pokemons)

    firstLimit = 0
    secondLimit = numbersPokemons

    print(f"\nENCONTRAMOS {numbersPokemons} POKEMONES\n")

    showPokemons = input("¿MOSTRAR TODOS? S/N: ").upper()

    while True:
        if (showPokemons not in ["S", "N"]):
            showPokemons = input("SOLO SE ACEPTA 2 VALORES. ¿MOSTRAR TODOS? S/N: ").upper()
            continue

        if showPokemons == "N":
            print("\nINGRESA UN RANGO\n")

            while True:
                firstLimit = isNumber("LÍMITE INFERIOR: ")
                secondLimit = isNumber("LÍMITE SUPERIOR: ")
                if firstLimit > secondLimit or secondLimit > numbersPokemons:
                    print("VUELVE A INGRESAR LOS LÍMITES\n")
                    continue
                break
        break

    print(f"\nCARGANDO SUS HABILIDADES...\n")

    dataPokemons = infoPokemons(urlPokemons,"abilities", firstLimit, secondLimit)
    tuplePokemons = zip(pokemons[firstLimit:secondLimit], dataPokemons[0], dataPokemons[1])
    fieldnames = ["Pokemon", "Habilidades", "URL Imagen"]

    print(tabulate(tuplePokemons, headers=fieldnames))

    print("\nCARGA COMPLETA")

option02(info)

# ------------------------Opción 3-----------------------------------
def option03(info=info):
    urlAbility = info["ability"]

    respAbility = requests.get(urlAbility).json()
    countAbilities = respAbility["count"]
    urlAllAbilities = "https://pokeapi.co/api/v2/ability/?offset=0&limit=" + str(countAbilities)
    jsonAbilities = requests.get(urlAllAbilities).json()
    listAbilities = [ability["name"] for ability in jsonAbilities["results"]]
    
    while True:
        letters = input("Ingresa la habilidad (o las primeras letras): ").lower()
        if letters.isalpha():
            selectedAbilities = []
            patron = re.compile('^' + letters)
            for ability in listAbilities:
                if patron.match(ability):
                    selectedAbilities.append(ability.capitalize())
            if selectedAbilities == []:
                print("Vuelve a intentar con otras letras")
                continue
            break

    print("\nENCONTRAMOS LAS SIGUIENTES HABILIDADES\n")
    availableAbility = []
    for index, ability in enumerate(selectedAbilities,1):
        print(f"    {index}: {ability}")
        availableAbility.append(index)

    print()
    while True:
        selection = input("¿VER TODAS LAS HABILIDADES O ELEGIR UNA? T/U: ").upper()
        if selection == "T" or selection == "U":
            break

    while True:
        if selection == "T":
            print("\nBUSCANDO POKEMONES...\n")
            listPokemons = []
            for ability in selectedAbilities:
                jsonPokemons = requests.get(urlAbility + ability.lower()).json()
                pokemons = [pokemon["pokemon"]["name"].capitalize() for pokemon in jsonPokemons["pokemon"]]
                if pokemons == []:
                    listPokemons.append("No hay pokemones")
                else:
                    listPokemons.append(pokemons)
            fieldnames = ["Habilidad", "Pokemones"]
            tuplePokemons = zip(selectedAbilities,listPokemons)
            print(tabulate(tuplePokemons,fieldnames))
            break

        elif selection == "U":
            print()
            while True:
                while True:
                    numberAbility = input("INGRESA EL NÚMERO DE LA HABILIDAD: ")
                    if numberAbility.isnumeric() and int(numberAbility) in availableAbility:
                        numberAbility = int(numberAbility)
                        break

                print("\nBUSCANDO POKEMONES...\n")

                jsonPokemons = requests.get(urlAbility + selectedAbilities[numberAbility-1].lower()).json()
                pokemons = [pokemon["pokemon"]["name"].capitalize() for pokemon in jsonPokemons["pokemon"]]
                urlPokemons = [pokemon["pokemon"]["url"] for pokemon in jsonPokemons["pokemon"]]
                imagePokemons = []
                for pokemon in urlPokemons:
                    jsonData = requests.get(pokemon).json()
                    dataImages = jsonData["sprites"]["back_default"]
                    if dataImages == None:
                        imagePokemons.append("Sin imagen")
                    else:
                        imagePokemons.append(dataImages)
                if pokemons == None:
                        pokemons.append("No hay pokemones")

                print(f"Habilidad: {selectedAbilities[numberAbility-1].capitalize()}\n")
                tuplePokemons = zip(pokemons, imagePokemons)
                fieldnames = ["Pokemon", "URL Imagen"]
                print(tabulate(tuplePokemons, headers= fieldnames))
                
                print("\nCARGA COMPLETA\n")

                anotherAbility = input("¿SELECCIONAR OTRA HABILIDAD? S/N: ").upper()
                if anotherAbility == "S":
                    print()
                    continue
                elif anotherAbility == "N":
                    print()
                    break
        break

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
    numbersPokemons = len(pokemonsNames)
    dataPokemons = []

    firstLimit = 0
    secondLimit = numbersPokemons
   
    if (not urlPokemons):
        print(f"\nNo hay pokemones del tipo {nameType}")
        return

    print(f"\nENCONTRAMOS {numbersPokemons} POKEMONES\n")

    showPokemons = input("¿MOSTRAR TODOS? S/N: ").upper()

    while True:
        if (showPokemons not in ["S", "N"]):
            showPokemons = input("SOLO SE ACEPTA 2 VALORES. ¿MOSTRAR TODOS? S/N: ").upper()
            continue

        if showPokemons == "N":
            print("\nINGRESA UN RANGO\n")

            while True:
                firstLimit = isNumber("LÍMITE INFERIOR: ")
                secondLimit = isNumber("LÍMITE SUPERIOR: ")
                if firstLimit > secondLimit or secondLimit > numbersPokemons:
                    print("VUELVE A INGRESAR LOS LÍMITES\n")
                    continue
                break
        break

    print(f"\nCARGANDO SUS HABILIDADES...\n")
        
    dataPokemons = infoPokemons(urlPokemons,"abilities", firstLimit, secondLimit)
    tuplePokemons = zip(pokemonsNames[firstLimit:secondLimit], dataPokemons[0], dataPokemons[1])
    fieldnames = ["Pokemon", "Habilidades", "URL Imagen"]
        
    print(tabulate(tuplePokemons, headers=fieldnames))
#option05()
