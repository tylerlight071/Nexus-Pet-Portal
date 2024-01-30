import time
from colorama import Fore, Style
from sudo_user import sudo_user
from common_functions import clear_screen, load_animal_data, save_data, log_action
from pymongo import MongoClient
from config import mongodb_uri

# Connect to MongoDB
uri = mongodb_uri
client = MongoClient(uri)

db = client['animal_rescue']
animals_collection = db['animals']

def change_adopted_status():
    clear_screen()

    # Load animal data from file
    animals = load_animal_data(animals_collection)
    current_user = sudo_user()

    name = input("\nEnter the name of the animal to toggle adoption status (type 'exit' to leave): ")
    
    if name == "exit":
        log_action(current_user, "Exited 'Change Adoption Status'")
        print("\nExiting...")
        time.sleep(2)
        return

    else:
        # Check if animal exists in the data
        if name in animals:
            
            # Toggle the adopted status
            animals[name]['adopted'] = not animals[name].get('adopted', False)
            save_data(animals)

            # Notify the user about the updated adoptino status
            if animals[name]['adopted']:
                print(Fore.GREEN + f"\n{name} has been marked as " + Fore.CYAN + "adopted!" + Style.RESET_ALL)
                log_action(current_user, f"{name} marked as adopted")
            else:
                print(Fore.GREEN + f"\n{name} has been marked as " + Fore.RED + "not adopted!" + Style.RESET_ALL)
                log_action(current_user, f"{name} marked as not adopted")
        # Notify the user if the animal is not found
        else:
            print(Fore.RED + f"\nNo animal found with the name {name}" + Style.RESET_ALL)

        time.sleep(2)