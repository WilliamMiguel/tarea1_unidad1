from tabulate import tabulate
import os
import requests
import json
os.system("cls")
# os.system("pip install tabulate")

url = "https://pokeapi.co/api/v2/"
resp = requests.get(url)
info = resp.json()

print(info["pokemon"])

pokemon = requests.get(info["pokemon"]).json()
print(pokemon)