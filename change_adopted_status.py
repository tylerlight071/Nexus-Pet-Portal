import json
import os
import time
from colorama import Fore, Style
from common_functions import clear_screen, load_data, save_data

ANIMAL_DATA_FILE = "animals.json"

def change_adopted_status():
    clear_screen()
    animals = load_data(ANIMAL_DATA_FILE)
    name = input("\nEnter the name of the animal to mark as adopted: ")

    if name in animals:
        animals[name]['adopted'] = True
        save_data(animals, ANIMAL_DATA_FILE)
        print(Fore.GREEN + f"\n{name} has been marked as adopted!" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"\nNo animal found with the name {name}" + Style.RESET_ALL)

    time.sleep(2)
