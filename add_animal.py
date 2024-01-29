import time
from colorama import Fore, Style
from common_functions import clear_screen ,load_data, save_data

ANIMAL_DATA_FILE = "animals.json"

def add_animal():
    animals = load_data(ANIMAL_DATA_FILE)

    while True:
        clear_screen()  # Clear the screen before prompting for input

        name = input("\nEnter the animal's name: ")
        if not name.strip():  # Check if the name is empty
            print(Fore.RED + "Invalid input. Please enter the animal's name." + Style.RESET_ALL)
            input(Fore.GREEN + "Press Enter to continue..."+ Style.RESET_ALL)
            continue

        species = input("Enter the animal's species: ")
        if not species.strip():  # Check if the species is empty
            print(Fore.RED + "Invalid input. Please enter the animal's name." + Style.RESET_ALL)
            input(Fore.GREEN + "Press Enter to continue..."+ Style.RESET_ALL)
            continue

        breed = input("Enter the animal's breed: ")
        if not breed.strip():  # Check if the breed is empty
            print(Fore.RED + "Invalid input. Please enter the animal's name." + Style.RESET_ALL)
            input(Fore.GREEN + "Press Enter to continue..."+ Style.RESET_ALL)
            continue

        gender = input("Enter the animal's gender: ")
        if not gender.strip():  # Check if the breed is empty
            print(Fore.RED + "Invalid input. Please enter the animal's name." + Style.RESET_ALL)
            input(Fore.GREEN + "Press Enter to continue..."+ Style.RESET_ALL)
            continue

        age = input("Enter the animal's age: ")
        if not age.strip():  # Check if the age is empty
            print(Fore.RED + "Invalid input. Please enter the animal's name." + Style.RESET_ALL)
            input(Fore.GREEN + "Press Enter to continue..."+ Style.RESET_ALL)
            continue
        elif not age.isdigit():  # Check if the age is a valid number
            print(Fore.RED + "Invalid input. Please enter the animal's name." + Style.RESET_ALL)
            input(Fore.GREEN + "Press Enter to continue..."+ Style.RESET_ALL)
            continue

        age = int(age)  # Convert age to an integer

        # Assuming age should be a positive number
        if age <= 0:
            print(Fore.RED + "Invalid input. Please enter the animal's name." + Style.RESET_ALL)
            input(Fore.GREEN + "Press Enter to continue..."+ Style.RESET_ALL)
            continue

        animals[name] = {'name': name, 'species': species, 'breed': breed, 'gender': gender,  'age': age, 'adopted': False}
        save_data(animals, ANIMAL_DATA_FILE)
        print(Fore.GREEN + "\nAnimal added successfully!" + Style.RESET_ALL)
        time.sleep(2)
        break  # Break the loop after successfully adding the animal
