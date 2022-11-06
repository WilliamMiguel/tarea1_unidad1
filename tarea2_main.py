import os
import re
import requests
import json
os.system("pip install tabulate")
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

#---------------------------Opción 2-----------------------
def option02(info = info):
    print()
    shape = info["pokemon-shape"]
    respShape = requests.get(shape).json()
    countShapes = respShape["count"]
    optionsShapes = [str(option + 1) for option in range(countShapes)]
    print("Elige una de las siguientes formas: \n")
    for index, shape in enumerate(respShape["results"], 1):
        print("    " + str(index) + ": " + shape["name"].capitalize())

    while True:
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

        print(f"\nEncontramos {len(pokemons)} pokemons\n")

        while True:
            showPokemons = input("¿Mostrar todos o ingresar un rango? T/R: ").upper()
            if showPokemons == "T":
                print(f"\nIdentificando habilidades...\n")
                dataPokemons = infoPokemons(urlPokemons,"abilities", 0, len(pokemons))
                tuplePokemons = zip(pokemons, dataPokemons[0], dataPokemons[1])
                fieldnames = ["Pokemon", "Habilidades", "URL Imagen"]
                print(tabulate(tuplePokemons, headers=fieldnames))
                break

            elif showPokemons == "R":
                print("\nIngresa un rango:")
                print()
                while True:
                    firstLimit = isNumber("    Límite inferior: ")
                    secondLimit = isNumber("    Límite superior: ")
                    if firstLimit > secondLimit or secondLimit > len(pokemons) or firstLimit == 0:
                        print("    Ingresa límites válidos")
                        continue
                    break

                print(f"\nIdentificando habilidades...\n")
                dataPokemons = infoPokemons(urlPokemons,"abilities", firstLimit, secondLimit)
                tuplePokemons = zip(pokemons[firstLimit:secondLimit], dataPokemons[0], dataPokemons[1])
                fieldnames = ["Pokemon", "Habilidades", "URL Imagen"]
                print(tabulate(tuplePokemons, headers=fieldnames))
                break

        print("\nCarga completa")
        anotherShape = input("\n¿Elegir otra forma? S/N: ").upper()
        if anotherShape == "S":
            continue
        elif anotherShape == "N":
            break

# ------------------------Opción 3-----------------------------------
def option03(info = info):
    print()
    urlAbility = info["ability"]
    respAbility = requests.get(urlAbility).json()
    countAbilities = respAbility["count"] #Obtenemos el número de habilidades existentes
    urlAllAbilities = "https://pokeapi.co/api/v2/ability/?offset=0&limit=" + str(countAbilities) #Enlace para mostrar todas las habilidades
    jsonAbilities = requests.get(urlAllAbilities).json()
    listAbilities = [ability["name"] for ability in jsonAbilities["results"]] # Lista de los nombres de todas las habilidades
    
    while True:
        while True:
            letters = input("Ingresa el nombre de la habilidad (o las primeras letras): ").lower()
            if letters.isalpha():
                selectedAbilities = []
                patron = re.compile('^' + letters) #Patrón de búsqueda en la lista de habilidades, que coincida desde el inicio
                for ability in listAbilities:
                    if patron.match(ability):
                        selectedAbilities.append(ability.capitalize()) #Habilidades que coinciden con la búsqueda
                if selectedAbilities == []:
                    print("Vuelve a intentar con otras letras")
                    continue
                break

        print("\nEncontramos las siguientes habilidades:\n")
        availableAbility = []
        for index, ability in enumerate(selectedAbilities,1):
            print(f"    {index}: {ability}")
            availableAbility.append(index)

        print()
        while True:
            selection = input("¿Ver pokemons con todas las habilidades o elegir una? T/U: ").upper()
            if selection == "T" or selection == "U":
                break

        while True:
            if selection == "T":
                print("\nBuscando pokemons\n")
                listPokemons = []
                for ability in selectedAbilities:
                    jsonPokemons = requests.get(urlAbility + ability.lower()).json()
                    pokemons = [pokemon["pokemon"]["name"].capitalize() for pokemon in jsonPokemons["pokemon"]] #Busca los pokemons que poseen cada habilidad
                    if pokemons == []:
                        listPokemons.append("No hay pokemons")
                    else:
                        listPokemons.append(pokemons)
                fieldnames = ["Habilidad", "Pokemones"]
                tuplePokemons = zip(selectedAbilities,listPokemons)
                print(tabulate(tuplePokemons,fieldnames))
                print("\nCarga completa\n")
                break

            elif selection == "U":
                print()
                while True:
                    while True:
                        numberAbility = input("Ingresa el número de la habilidad: ")
                        if numberAbility.isnumeric() and int(numberAbility) in availableAbility:
                            numberAbility = int(numberAbility)
                            break

                    print("\nBuscando pokemons...\n")

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
                            pokemons.append("No hay pokemons")

                    print(f"Habilidad: {selectedAbilities[numberAbility-1].capitalize()}\n")
                    tuplePokemons = zip(pokemons, imagePokemons)
                    fieldnames = ["Pokemon", "URL Imagen"]
                    print(tabulate(tuplePokemons, headers= fieldnames))
                    
                    print("\nCarga completa\n")

                    anotherAbility = input("¿Seleccionar otra habilidad? S/N: ").upper()
                    if anotherAbility == "S":
                        print()
                        continue
                    elif anotherAbility == "N":
                        print()
                        break
            break
        repeat = input("¿Buscar otra habilidad? S/N: ").upper()
        if repeat == "S":
            print()
            continue
        elif repeat =="N":
            break

options = ["option01", "option02(info)", "option03(info)", "option04", "option05(info)"]

def showOptions():
    print("Elije una de las siguientes opciones:\n")
    print('''    Opción 1: Listar pokemons por generación.
    Opción 2: Listar pokemons por forma.
    Opción 3: Listar pokemons por habilidad.
    Opción 4: Listar pokemons por habitat.
    Opción 5: Listar pokemons por tipo.
    ''')

numbersOptions = [1, 2, 3, 4, 5]
print()
while True:
    os.system("cls")
    showOptions()
    while True:
        selectOption = input("Ingresa una opción: ")
        if selectOption.isnumeric() and int(selectOption) in numbersOptions:
            selectOption = int(selectOption)
            break

    eval(options[selectOption-1])
    print()
    anotherOption = input("¿Seleccionar otra lista? S/N: ").upper()
    if anotherOption == "S":
        continue
    elif anotherOption == "N":
        break


