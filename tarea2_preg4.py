import os
os.system("cls")
import json
import requests

#Opción 4: Listar pokemons por habitat. Se deben sugerir opciones a ingresar para interactuar.
url_habitat="https://pokeapi.co/api/v2/pokemon-habitat/"
lista_habitat=["cave","forest","grassland","mountain","rare","rough-terrain","sea","urban","waters-edge"]

def pokemones_habitat(habitat):
    resp=requests.get(url_habitat+habitat)

    data =resp.json()
    lista_pokemones=[habitat['name'] for habitat in data['pokemon_species']]
    return lista_pokemones
  
while True:   
    pregunta4=input(f"¿Qué habitat desea elegir? {lista_habitat}: ") 
    if pregunta4 in lista_habitat:
        break
      
pokemones=pokemones_habitat(pregunta4)

url_habilidad="https://pokeapi.co/api/v2/pokemon/"

def listar_pokemon(pokemon):
    resp=requests.get(url_habilidad+pokemon)
    
    if resp.status_code==200:
        data =resp.json()
        lista_habilidades=[habilidad['ability']['name'] for habilidad in data['abilities']]
        image_url = data['sprites']['front_default']
        
        print(f"Nombre Pokemon: {pokemon}") 
        print(f"Lista de habilidades: {lista_habilidades}")
        print(f"URL de la imagen: {image_url}")
        print("-----------------------------------"*2)
    else:   
        print(f"Nombre Pokemon: {pokemon}")
        print("No se encontró información")
        print("-----------------------------------"*2)


for i in pokemones:
    listar_pokemon(i)



