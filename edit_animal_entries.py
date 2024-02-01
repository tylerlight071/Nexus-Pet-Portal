import time
from common_functions import clear_screen 
from colorama import Fore, Style
from pymongo import MongoClient
from config import mongodb_uri

# Connect to MongoDB
uri = mongodb_uri
client = MongoClient(uri)

db = client['animal_rescue']
animals_collection = db['animals']

def modify_animal():
    clear_screen()
    print(Fore.CYAN + "\n🐾 Modify Animal 🐾\n" + Style.RESET_ALL)

    # Input the name of the animal to modify
    animal_name = input(Fore.CYAN + "Enter the name of the animal to modify: " + Style.RESET_ALL).strip()

    # Search for the animal in the database
    animal = animals_collection.find_one({'name': animal_name})

    if animal:
        print(Fore.GREEN + "\nAnimal found. You can modify the following fields:")
        print("1. Name")
        print("2. Species")
        print("3. Breed")
        print("4. Gender")
        print("5. Age")
        print(Style.RESET_ALL)

        field_choice = input("Enter the number of the field to modify or 'exit' to cancel: ")

        if field_choice.lower() == 'exit':
            print(Fore.YELLOW + "\nExiting..." + Style.RESET_ALL)
            time.sleep(2)
            return
        
        if field_choice.isdigit():
            field_choice = int(field_choice)
            if field_choice == 1:
                new_value = input("Enter new name: ").strip()
                animals_collection.update_one({'name': animal_name}, {'$set': {'name': new_value}})
            elif field_choice == 2:
                new_value = input("Enter new species: ").strip()
                animals_collection.update_one({'name': animal_name}, {'$set': {'species': new_value}})
            elif field_choice == 3:
                new_value = input("Enter new breed: ").strip()
                animals_collection.update_one({'name': animal_name}, {'$set': {'breed': new_value}})
            elif field_choice == 4:
                new_value = input("Enter new gender: ").strip()
                if new_value in ['male', 'female']:
                    animals_collection.update_one({'name': animal_name}, {'$set': {'gender': new_value}})
                else:
                    print(Fore.RED + "\nInvalid input. Gender must be 'Male' or 'Female'." + Style.RESET_ALL)
            elif field_choice == 5:
                new_value = input("Enter new age: ").strip()
                if new_value.isdigit() and int(new_value) > 0:
                    animals_collection.update_one({'name': animal_name}, {'$set': {'age': int(new_value)}})
                else:
                    print(Fore.RED + "Invalid age. Please enter a positive integer.")
                    
            else:
                print(Fore.RED + "Invalid choice.")

    else:
        print(Fore.RED + "Animal not found.")

    input(Fore.GREEN + "Press Enter to continue..." + Style.RESET_ALL)