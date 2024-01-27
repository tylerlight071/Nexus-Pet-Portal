import time
from colorama import Fore, Style
from common_functions import clear_screen ,load_data, save_data

ANIMAL_DATA_FILE = "animals.json"

def add_animal():
    clear_screen()
    animals = load_data(ANIMAL_DATA_FILE)
    name = input("Enter the animal's name: ")
    species = input("Enter the animal's species: ")
    breed = input ("Enter the animal's breed: ")
    age = input ("Enter the animal's age: ")
    animals[name] = {'species': species, 'breed': breed, 'age': age, 'adopted': False}
    save_data(animals, ANIMAL_DATA_FILE)
    print(Fore.GREEN + "Animal added successfully!" + Style.RESET_ALL)
    time.sleep(2)
