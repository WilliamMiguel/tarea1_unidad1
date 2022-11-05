import os
import re
import requests
import json
os.system("cls")
# os.system("pip install tabulate")
from tabulate import tabulate

url = "https://pokeapi.co/api/v2/"
resp = requests.get(url)
info = resp.json()


def generator(urlPokemons: list, firstLimit: int, secondLimit: int):
    url = "https://pokeapi.co/api/v2/pokemon/"
    for pokemon in range(firstLimit, secondLimit):
        info = requests.get(urlPokemons[pokemon]).json()
        nameDefault = info["varieties"][0]["pokemon"]["name"]
        jsonData = requests.get(url + nameDefault).json()
        abilities = [data["ability"]["name"] for data in jsonData["abilities"]]
        urlImage = jsonData["sprites"]["back_default"]
        if urlImage == None:
                urlImage = "Sin imagen"
        
    return nameDefault, abilities, urlImage

def isNumber(text: str):
    while True:
        value = input(text)
        if value.isnumeric():
            value = int(value)
            break
    return value

def infoPokemons(pokemons: list, selection: str, firstLimit, secondLimit: int) -> list:
    print(pokemons)
    dataPokemons = []
    imagePokemons = []
    numberPokemon = firstLimit
    for pokemon in range(firstLimit, secondLimit):
        url = "https://pokeapi.co/api/v2/pokemon/"
        info = requests.get(pokemons[numberPokemon]).json()
        nameDefault = info["varieties"][0]["pokemon"]["name"]
        jsonData = requests.get(url + nameDefault).json()
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

    print(f"\nENCONTRAMOS {len(pokemons)} POKEMONES\n")

    while True:
        showPokemons = input("¿MOSTRAR TODOS? S/N: ").upper()
        if showPokemons == "S":
            print(f"\nCARGANDO SUS HABILIDADES...\n")
            dataPokemons = infoPokemons(urlPokemons,"abilities", 0, len(pokemons))
            tuplePokemons = zip(pokemons, dataPokemons[0], dataPokemons[1])
            fieldnames = ["Pokemon", "Habilidades", "URL Imagen"]
            print(tabulate(tuplePokemons, headers=fieldnames))
            break


        elif showPokemons == "N":
            print("\nINGRESA UN RANGO")
            print()
            while True:
                firstLimit = isNumber("LÍMITE INFERIOR: ")
                secondLimit = isNumber("LÍMITE SUPERIOR: ")
                if firstLimit > secondLimit or secondLimit > len(pokemons):
                    print("VUELVE A INGRESAR LOS LÍMITES")
                    continue
                break

            print(f"\nCARGANDO SUS HABILIDADES...\n")
            dataPokemons = infoPokemons(urlPokemons,"abilities", firstLimit, secondLimit)
            tuplePokemons = zip(pokemons[firstLimit:secondLimit], dataPokemons[0], dataPokemons[1])
            fieldnames = ["Pokemon", "Habilidades", "URL Imagen"]
            print(tabulate(tuplePokemons, headers=fieldnames))

            break

    # dataPokemons = infoPokemons(urlPokemons,"abilities")
    # tuplePokemons = zip(pokemons, dataPokemons[0], dataPokemons[1])
    # fieldnames = ["Pokemon", "Habilidades", "URL Imagen"]
    # print(tabulate(tuplePokemons, headers=fieldnames))

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
        selection = input("Ingresa T para ver los pokemones de todas las habilidades o U para elegir una habilidad: ").upper()
        if selection == "T":
            break
        elif selection == "U":
            print()
            while True:
                numberAbility = input("Ingresa el número de la habilidad: ")
                if numberAbility.isnumeric() and int(numberAbility) in availableAbility:
                    numberAbility = int(numberAbility)
                    break
            break

    print("\nBUSCANDO POKEMONES...\n")

    listPokemons = []
    if selection == "T":
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
    
    else:
        jsonPokemons = requests.get(urlAbility + selectedAbilities[numberAbility-1].lower()).json()
        pokemons = [pokemon["pokemon"]["name"].capitalize() for pokemon in jsonPokemons["pokemon"]]
        if pokemons == []:
                pokemons.append("No hay pokemones")
        print(f"Habilidad: {selectedAbilities[numberAbility-1].capitalize()}")
        print("Pokemones:")
        print(*pokemons, sep= ", ")
    
    print("\nCARGA COMPLETA")

# option03(info)

