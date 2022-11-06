import os
os.system("cls")
import json
import requests
from tabulate import tabulate

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

def listar_pokemon(pokemons):
    url_habilidad="https://pokeapi.co/api/v2/pokemon/"
    lista_habilidades = []
    image_url = []
    for pokemon in pokemons:
        resp=requests.get(url_habilidad+pokemon.lower())
        if resp.status_code==200:
            data =resp.json()
            habilidades=[habilidad['ability']['name'] for habilidad in data['abilities']]
            lista_habilidades.append(habilidades)
            url = data['sprites']['front_default']
            if url == None:
                image_url.append("No se encontró información")
            else: 
                image_url.append(url)
            
        else:
            lista_habilidades.append("No se encontró información")
            image_url.append("No se encontró información")
        
    return lista_habilidades, image_url

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
        listaPokemons = listar_pokemon(pokemones)

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
        listaPokemons = listar_pokemon(pokemones)

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
option01()
