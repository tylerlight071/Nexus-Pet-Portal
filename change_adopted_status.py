import json
import os
import time
from colorama import Fore, Style

ANIMAL_DATA_FILE = "animals.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)

def save_data(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

def change_adopted_status():
    clear_screen()
    animals = load_data(ANIMAL_DATA_FILE)
    name = input("Enter the name of the animal to mark as adopted: ")

    if name in animals:
        animals[name]['adopted'] = True
        save_data(animals, ANIMAL_DATA_FILE)
        print(Fore.GREEN + f"{name} has been marked as adopted!" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"No animal found with the name {name}" + Style.RESET_ALL)

    time.sleep(2)
