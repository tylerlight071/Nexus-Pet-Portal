import time
from common_functions import clear_screen, get_mongodb_uri, load_animal_data
from tables import print_animal_table
from colorama import Fore, Style
from pymongo import MongoClient
from sudo_user_login import SudoUser

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)

db = client['animal_rescue']
animals_collection = db['animals']
users_collection = db['users']

FIELDS = {
    1: "name",
    2: "species",
    3: "breed",
    4: "gender",
    5: "age"
}

def get_animal_name():
    return input(Fore.CYAN + "Enter the name of the animal to modify (enter 'exit' to leave): " + Style.RESET_ALL).strip().capitalize()
    

def get_field_choice():
    return input("Enter the number of the field to modify or 'exit' to cancel: ")

def get_new_value(field):
    return input(f"Enter new {field}: ").strip().capitalize()

def update_animal_field(animal, field, new_value):
    if new_value != animal[field]:
        animals_collection.update_one({'name': animal['name']}, {'$set': {field: new_value}})
        print(Fore.GREEN + f"\n{field.capitalize()} updated successfully." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        print_animal_table(load_animal_data(animals_collection))
    else:
        print(Fore.YELLOW + f"\nNew {field} is the same as the current one. No update performed." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        print_animal_table(load_animal_data(animals_collection))

def modify_animal():
    animals = load_animal_data(animals_collection)

    clear_screen()
    SudoUser(users_collection.database).login()
    print(Fore.CYAN + "\n🐾 Modify Animal 🐾\n" + Style.RESET_ALL)

    animal_name = get_animal_name()

    if animal_name.lower() == 'exit':
        print(Fore.YELLOW + "\nExiting..." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        print_animal_table(animals)
        return
    
    animal = animals_collection.find_one({'name': animal_name})

    if animal:
        print(Fore.LIGHTMAGENTA_EX + "\nAnimal found. You can modify the following fields:" + Style.RESET_ALL)
        print("\n1. Name")
        print("2. Species")
        print("3. Breed")
        print("4. Gender")
        print("5. Age")
        print(Style.RESET_ALL)

        field_choice = get_field_choice()

        if field_choice.lower() == 'exit':
            print(Fore.YELLOW + "\nExiting..." + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
            print_animal_table(animals)
            return
        
        if field_choice.isdigit():
            field_choice = int(field_choice)
            if field_choice in FIELDS:
                field = FIELDS[field_choice]
                new_value = get_new_value(field)
                update_animal_field(animal, field, new_value)
            else:
                print(Fore.RED + "Invalid input! Please enter a valid number." + Style.RESET_ALL)
                time.sleep(2)
                modify_animal()