import json
import os
import time
from colorama import Fore, Style
from common_functions import clear_screen, load_data, save_data

ANIMAL_DATA_FILE = "animals.json"

def change_adopted_status():
    clear_screen()

    # Load animal data from file
    animals = load_data(ANIMAL_DATA_FILE)

    name = input("\nEnter the name of the animal to toggle adoption status: ")
    
    # Check if animal exists in the data
    if name in animals:
        
        # Toggle the adopted status
        animals[name]['adopted'] = not animals[name].get('adopted', False)
        save_data(animals, ANIMAL_DATA_FILE)

        # Notify the user about the updated adoptino status
        if animals[name]['adopted']:
            print(Fore.GREEN + f"\n{name} has been marked as " + Fore.CYAN + "adopted!" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"\n{name} has been marked as " + Fore.RED + "not adopted!" + Style.RESET_ALL)

    # Notify the user if the animal is not found
    else:
        print(Fore.RED + f"\nNo animal found with the name {name}" + Style.RESET_ALL)

    time.sleep(2)