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
        if ("varieties" in info):
            nameDefault = info["varieties"][0]["pokemon"]["name"] #Obtiene el nombre de la primera "variación" del pokemon
            jsonData = requests.get(url + nameDefault).json() #Obtiene los datos de la primera variación del pokemon
        else:
            jsonData = info
        if selection == "abilities":
            dataAbilities = [data["ability"]["name"] for data in jsonData["abilities"]]
            dataPokemons.append(dataAbilities)
        dataImages = jsonData["sprites"]["front_default"]
        if dataImages == None:
            imagePokemons.append("Sin imagen")
        else:
            imagePokemons.append(dataImages)

        numberPokemon += 1
        
    return dataPokemons, imagePokemons

def pokemones_generacion(generacion):
    url_generacion="https://pokeapi.co/api/v2/generation/"
    resp=requests.get(url_generacion+str(generacion))

    data =resp.json()
    lista_pokemones=[generacion['name'].capitalize() for generacion in data['pokemon_species']]
    return lista_pokemones

def pokemones_habitat(habitat):
    url_habitat="https://pokeapi.co/api/v2/pokemon-habitat/"
    resp=requests.get(url_habitat+habitat)

    data =resp.json()
    lista_pokemones=[habitat['name'].capitalize() for habitat in data['pokemon_species']]
    return lista_pokemones

# ------------------------Opción 01 -----------------------------------
def option01():
    while True:
        lista_generaciones=[1,2,3,4,5,6,7,8]
        print("\n¿Qué categoría desea elegir?\n")
        for generation in lista_generaciones:
            print(f"    Generación: {generation}")
        print()

        while True:  
            pregunta1 = input("Ingresa una generación: ")
            if pregunta1.isnumeric() and int(pregunta1) in lista_generaciones:
                    break
            
        pokemones=pokemones_generacion(pregunta1)

        print("\nBuscando pokemons...\n")
        listaPokemons = infoPokemons(pokemones, "abilities", 0, len(pokemones))

        tuplePokemons = zip(pokemones,listaPokemons[0],listaPokemons[1])
        fieldnames = ["Pokemon","Habilidades","URL Imagen"]
        print(tabulate(tuplePokemons, headers=fieldnames))
        print()

        while True:
            anotherGeneration = input("¿Elegir otra generación? S/N: ").upper()
            if anotherGeneration == "S" or anotherGeneration == "N":
                break
        
        if anotherGeneration == "N":
            break

# ------------------------Opción 02 -----------------------------------
def option02(info):
    print()
    shape = info["pokemon-shape"]
    respShape = requests.get(shape).json()
    countShapes = respShape["count"]
    optionsShapes = [str(option + 1) for option in range(countShapes)]


    while True:
        print("Elige una de las siguientes formas: \n")
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
            print()
            continue
        elif anotherShape == "N":
            break

# ------------------------Opción 3-----------------------------------
def option03(info):
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
                        dataImages = jsonData["sprites"]["front_default"]
                        if dataImages == None:
                            imagePokemons.append("Sin imagen")
                        else:
                            imagePokemons.append(dataImages)
                    if pokemons == None or pokemons == []:
                            pokemons.append("No hay pokemons")

                    print(f"Habilidad: {selectedAbilities[numberAbility-1].capitalize()}\n")
                    tuplePokemons = zip(pokemons, imagePokemons)
                    fieldnames = ["Pokemon", "URL Imagen"]
                    print(tabulate(tuplePokemons, headers= fieldnames))
                    
                    print("\nCarga completa\n")

                    anotherAbility = input("¿Seleccionar otra habilidad? S/N: ").upper()
                    if anotherAbility == "S":
                        print()
                        for index, ability in enumerate(selectedAbilities,1):
                            print(f"    {index}: {ability}")
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

# ------------------------Opción 04-----------------------------------
def option04():
    while True:
        lista_habitat=["cave","forest","grassland","mountain","rare","rough-terrain","sea","urban","waters-edge"]   
        number_habitat=[]
        print("\n¿Qué habitat desea elegir?\n")
        for index,habitat in enumerate(lista_habitat,1):
            print(f"        {index}: {habitat.capitalize()}")
            number_habitat.append(index)
        print()

        while True:  
                pregunta4 = input("Ingresa un habitat: ")
                if pregunta4.isnumeric() and int(pregunta4) in number_habitat:
                        break
        
        pokemones=pokemones_habitat(pregunta4)

        print("\nBuscando pokemons...\n")
        listaPokemons = infoPokemons(pokemones, "abilities", 0, len(pokemones))

        tuplePokemons = zip(pokemones,listaPokemons[0],listaPokemons[1])
        fieldnames = ["Pokemon","Habilidades","URL Imagen"]
        print(tabulate(tuplePokemons, headers=fieldnames))
        print()

        while True:
            anotherHabitat = input("¿Elegir otro habitat? S/N: ").upper()
            if anotherHabitat == "S" or anotherHabitat == "N":
                break
        
        if anotherHabitat == "N":
            break

# ------------------------Opción 05-----------------------------------
def option05(info: dict) -> None:
    print()
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

    print(f"\nEncontramos {numbersPokemons} pokemons\n")

    showPokemons = input("¿Mostrar todos? S/N: ").upper()

    while True:
        if (showPokemons not in ["S", "N"]):
            showPokemons = input("Solo se aceptan 2 valores. ¿Mostrar todos? S/N: ").upper()
            continue

        if showPokemons == "N":
            print("\nIngresa un rango\n")

            while True:
                firstLimit = isNumber("Límite inferior: ")
                secondLimit = isNumber("Límite superior: ")
                if firstLimit > secondLimit or secondLimit > numbersPokemons:
                    print("Vuelve a ingresar los límites\n")
                    continue
                break
        break

    print(f"\nIdentificando habilidades...\n")
        
    dataPokemons = infoPokemons(urlPokemons,"abilities", firstLimit, secondLimit)
    tuplePokemons = zip(pokemonsNames[firstLimit:secondLimit], dataPokemons[0], dataPokemons[1])
    fieldnames = ["Pokemon", "Habilidades", "URL Imagen"]
        
    print(tabulate(tuplePokemons, headers=fieldnames))

options = ["option01()", "option02(info)", "option03(info)", "option04()", "option05(info)"]

def showOptions():
    print("\t\t\tPOKEAPI\n")
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
