import time
from common_functions import clear_screen, get_mongodb_uri
from colorama import Fore, Style
from pymongo import MongoClient
from sudo_user import sudo_user

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)

db = client['animal_rescue']
animals_collection = db['animals']

def modify_animal():
    clear_screen()
    sudo_user()
    print(Fore.CYAN + "\n🐾 Modify Animal 🐾\n" + Style.RESET_ALL)

    # Input the name of the animal to modify
    animal_name = input(Fore.CYAN + "Enter the name of the animal to modify: " + Style.RESET_ALL).strip().capitalize()

    # Search for the animal in the database
    animal = animals_collection.find_one({'name': animal_name})

    if animal:
        print(Fore.LIGHTMAGENTA_EX + "\nAnimal found. You can modify the following fields:" + Style.RESET_ALL)
        print("\n1. Name")
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
                if new_value != animal['name']:
                    animals_collection.update_one({'name': animal_name}, {'$set': {'name': new_value}})
                    print(Fore.GREEN + "\nName updated successfully." + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "\nNew name is the same as the current one. No update performed." + Style.RESET_ALL)
            elif field_choice == 2:
                new_value = input("Enter new species: ").strip()
                if new_value != animal['species']:
                    animals_collection.update_one({'name': animal_name}, {'$set': {'species': new_value}})
                    print(Fore.GREEN + "\nSpecies updated successfully." + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "\nNew species is the same as the current one. No update performed." + Style.RESET_ALL)
            elif field_choice == 3:
                new_value = input("Enter new breed: ").strip()
                if new_value != animal['breed']:
                    animals_collection.update_one({'name': animal_name}, {'$set': {'breed': new_value}})
                    print(Fore.GREEN + "\nBreed updated successfully." + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "\nNew breed is the same as the current one. No update performed." + Style.RESET_ALL)
            elif field_choice == 4:
                new_value = input("Enter new gender: ").strip().lower()
                if new_value in ['male', 'female'] and new_value != animal['gender']:
                    animals_collection.update_one({'name': animal_name}, {'$set': {'gender': new_value}})
                    print(Fore.GREEN + "\nGender updated successfully." + Style.RESET_ALL)
                elif new_value not in ['male', 'female']:
                    print(Fore.RED + "\nInvalid input. Gender must be 'Male' or 'Female'." + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "\nNew gender is the same as the current one. No update performed." + Style.RESET_ALL)
            elif field_choice == 5:
                new_value = input("Enter new age: ").strip()
                if new_value.isdigit() and int(new_value) > 0 and int(new_value) != animal['age']:
                    animals_collection.update_one({'name': animal_name}, {'$set': {'age': int(new_value)}})
                    print(Fore.GREEN + "\nAge updated successfully." + Style.RESET_ALL)
                elif not new_value.isdigit() or int(new_value) <= 0:
                    print(Fore.RED + "Invalid age. Please enter a positive integer." + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "\nNew age is the same as the current one. No update performed." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid choice." + Style.RESET_ALL)

    else:
        print(Fore.RED + "Animal not found." + Style.RESET_ALL)
        time.sleep(2)

    input("Press Enter to continue...")