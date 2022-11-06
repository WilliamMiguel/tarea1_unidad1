import os
# os.system("cls")
import json
import requests
from tabulate import tabulate

#Opción 1: Listar pokemons por generación. Se ingresa alguna generación (1, 2, 3, ..) y se listan todos los pokemon respectivos.

lista_generaciones=[1,2,3,4,5,6,7,8]

def pokemones_generacion(generacion):
    url_generacion="https://pokeapi.co/api/v2/generation/"
    resp=requests.get(url_generacion+str(generacion))

    data =resp.json()
    lista_pokemones=[generacion['name'].capitalize() for generacion in data['pokemon_species']]
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
                # lista_habilidades.append("No se encontró información")
                image_url.append("No se encontró información")
            else: 
                image_url.append(url)
            
            # print(f"Nombre Pokemon: {pokemon}") 
            # print(f"Lista de habilidades: {lista_habilidades}")
            # print(f"URL de la imagen: {image_url}")
            # print("-----------------------------------"*2)
        else:
            lista_habilidades.append("No se encontró información")
            image_url.append("No se encontró información")
            # print(f"Nombre Pokemon: {pokemon}")
            # print("No se encontró información")
            # print("-----------------------------------"*2)
    return lista_habilidades, image_url

while True:
    print(f"\n¿Qué categoría desea elegir?\n")
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
    # for i in pokemones:
    #     listar_pokemon(i)
    print()

    while True:
        anotherGeneration = input("¿Elegir otra generación? S/N: ").upper()
        if anotherGeneration == "S" or anotherGeneration == "N":
            break
    
    if anotherGeneration == "N":
        break

