import os
import requests
import json
os.system("cls")

url = "https://pokeapi.co/api/v2/"
resp = requests.get(url)
info = json.loads(resp.text)



