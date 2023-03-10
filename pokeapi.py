import requests
from PIL import Image
import os
import time
from termcolor import colored
try:
    import ascii_magic
except ModuleNotFoundError:
    print("Error: ascii_magic library is required to run this program. Please install the package with the following command:")
    print("pip install ascii-magic")
    exit()

URL = "https://pokeapi.co/api/v2/pokemon/"
ALL_PK = "https://pokeapi.co/api/v2/pokemon?limit=1000"
WELCOME_MSG = "Enter the Name of the Pokémon (or 'all' to see all the available pokemons, or 'exit' to finish) => "
EXIT = "exit"
LIST = "all"
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
    time.sleep(0.5) #optional
    
def print_pokemon_data(pokemon_data):
    print(colored("Name:", COLOR_GREEN), pokemon_data["name"])
    print(colored("Weight:", COLOR_BLUE), f"{pokemon_data['weight']} kg")
    print(colored("Height:", COLOR_MAGENTA), f"{pokemon_data['height']} m")
    print(colored("HP:", COLOR_RED), pokemon_data["stats"][0]["base_stat"])
    print(colored("Att:", COLOR_YELLOW), pokemon_data["stats"][1]["base_stat"])
    print(colored("Def:", COLOR_CYAN), pokemon_data["stats"][2]["base_stat"])
    print(colored("Type:", COLOR_GREY), pokemon_data["types"][0]["type"]["name"])
    print(colored("Abilities:", "light_green"))
    for ability in pokemon_data["abilities"]:
        print(" ", ability["ability"]["name"])

def show_pokemon(pokemon_data):
    try:
        with Image.open(IMAGE_FILE) as img:
            ascii_art = ascii_magic.from_image(IMAGE_FILE)
            print()
            ascii_art.to_terminal(columns=120, width_ratio=3)
            print_pokemon_data(pokemon_data)
            print()

    except Exception as e:
        print(f"Error loading image: {e}")

def check_pokemon_found(response, pokemon_name):
    if response.status_code != 200:
        print(colored(f"No Pokémon with the name found {pokemon_name}, if you want you can check the list ", COLOR_RED))
        return False
    return True

def show_all_pk():
    response = requests.get(ALL_PK)
    pokemon_list = response.json()["results"]
    print("All Pokémon:")
    for pokemon in pokemon_list:
        print(pokemon["name"])
      
if __name__ == "__main__":
    while True:
        pokemon_name = input(colored(WELCOME_MSG, COLOR_BLUE)).lower().strip()
        if pokemon_name == EXIT:
            break
        elif pokemon_name == LIST:
            show_all_pk()
            print()
            continue
        
        response = requests.get(URL + pokemon_name)
        if check_pokemon_found(response, pokemon_name):
            print()
            pokemon_data = get_pokemon_data(pokemon_name)
            prepare_pokemon_image(pokemon_data)
            show_pokemon(pokemon_data)