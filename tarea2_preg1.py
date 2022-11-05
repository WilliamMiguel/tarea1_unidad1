import os
os.system("cls")
import json
import requests

#Opción 1: Listar pokemons por generación. Se ingresa alguna generación (1, 2, 3, ..) y se listan todos los pokemon respectivos.
url_generacion="https://pokeapi.co/api/v2/generation/"
lista_generaciones=[1,2,3,4,5,6,7,8]

def pokemones_generacion(generacion):
    resp=requests.get(url_generacion+str(generacion))

    data =resp.json()
    lista_pokemones=[generacion['name'] for generacion in data['pokemon_species']]
    return lista_pokemones
  
while True:   
    pregunta1=input(f"¿Qué categoría desea elegir? {lista_generaciones}: ") 
    if pregunta1.isnumeric() :
        if int(pregunta1) in lista_generaciones:
            break
      
pokemones=pokemones_generacion(pregunta1)

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



