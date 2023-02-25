import requests
from PIL import Image
import ascii_magic
import os
import time
from termcolor import colored

# URL de la API de Pokémon
URL = "https://pokeapi.co/api/v2/pokemon/"
WELCOME_MSG = "Ingresa el Nombre del Pokémon (o 'salir' para finalizar) => "
EXIT = "salir"
NAME_FILE = ""
COLOR_GREEN = "green"
COLOR_BLUE = "blue"
COLOR_MAGENTA = "magenta"
COLOR_RED = "red"
COLOR_YELLOW = "yellow"
COLOR_CYAN = "cyan"
COLOR_GREY = "grey"
IMAGE_FILE = "pokemon.png"

def get_pokemon_data(name):
    response = requests.get(URL + name.lower())
    response.raise_for_status()
    return response.json()

def prepare_pokemon_image(pokemon_data):
    sprite_url = pokemon_data["sprites"]["front_default"]
    response = requests.get(sprite_url)
    with open(IMAGE_FILE, "wb") as f:
        f.write(response.content)

    os.chmod(IMAGE_FILE, 0o755)
    
def print_pokemon_data(pokemon_data):
    print(colored("Nombre:", COLOR_GREEN), pokemon_data["name"])
    print(colored("Peso:", COLOR_BLUE), f"{pokemon_data['weight']} kg")
    print(colored("Altura:", COLOR_MAGENTA), f"{pokemon_data['height']} m")
    print(colored("HP:", COLOR_RED), pokemon_data["stats"][0]["base_stat"])
    print(colored("Ataque:", COLOR_YELLOW), pokemon_data["stats"][1]["base_stat"])
    print(colored("Defensa:", COLOR_CYAN), pokemon_data["stats"][2]["base_stat"])
    print(colored("Tipo:", COLOR_GREY), pokemon_data["types"][0]["type"]["name"])

def show_pokemon(pokemon_data):
    try:
        with Image.open(IMAGE_FILE) as img:
            ascii_art = ascii_magic.from_image(IMAGE_FILE)
            print()
            ascii_art.to_terminal(columns=120, width_ratio=3)
            print_pokemon_data(pokemon_data)
            print()

    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

def check_pokemon_found(response, pokemon_name):
    if response.status_code != 200:
        print(colored(f"No se encontró ningún Pokémon con el nombre {pokemon_name}", "red"))
        return False
    return True

if __name__ == "__main__":
    while True:
        pokemon_name = input(colored(WELCOME_MSG, COLOR_BLUE)).lower()
        if pokemon_name == EXIT:
            break
        response = requests.get(URL + pokemon_name)
        if check_pokemon_found(response, pokemon_name):
            print()
            pokemon_data = get_pokemon_data(pokemon_name)
            prepare_pokemon_image(pokemon_data)
            show_pokemon(pokemon_data)

