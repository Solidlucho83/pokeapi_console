import requests
from PIL import Image
import ascii_magic
import os
import time
from termcolor import colored

# URL de la API de Pokémon
URL = "https://pokeapi.co/api/v2/pokemon/"

def get_pokemon(name):
    # Hacer una solicitud GET a la API de Pokémon para obtener la información del Pokémon
    response = requests.get(URL + name.lower())
    response.raise_for_status()
    pokemon_data = response.json()
     
   
    # Obtener la URL de la imagen del Pokémon en formato PNG
    sprite_url = response.json()["sprites"]["front_default"]

    # Descargar la imagen del Pokémon en formato PNG
    response = requests.get(sprite_url)
    with open(f"pokemon.png", "wb") as f:
        f.write(response.content)

    # Agregar permisos al archivo
    os.chmod(f"pokemon.png", 0o755)

    time.sleep(0.5)
    # Cargar la imagen del archivo
    try:
        with Image.open(f"pokemon.png") as img:
            # Convertir la imagen a ASCII utilizando ascii_magic
            ascii_art = ascii_magic.from_image("pokemon.png")
            # Mostrar la imagen en la consola
            print()
            ascii_art.to_terminal(columns=120, width_ratio=3)
            print(colored("Nombre:", "green"), pokemon_data["name"])
            print(colored("Peso:", "blue"), f"{pokemon_data['weight']} kg")
            print(colored("Altura:", "magenta"), f"{pokemon_data['height']} m")
            print(colored("HP:", "red"), pokemon_data["stats"][0]["base_stat"])
            print(colored("Ataque:", "yellow"), pokemon_data["stats"][1]["base_stat"])
            print(colored("Defensa:", "cyan"), pokemon_data["stats"][2]["base_stat"])
            print(colored("Tipo:", "grey"), pokemon_data["types"][0]["type"]["name"])
            print()

    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

if __name__ == "__main__":
      while True:
        pokemon_name = input(colored("Ingresa el Nombre del Pokémon (o 'salir' para finalizar) => ", "blue")).lower()
        if pokemon_name == "salir":
            break
        response = requests.get(URL + pokemon_name)
        if response.status_code != 200:
            print(colored(f"No se encontró ningún Pokémon con el nombre {pokemon_name}", "red"))
        else: 
            print()
            get_pokemon(pokemon_name)
            