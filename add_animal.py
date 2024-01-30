import time
from colorama import Fore, Style
from common_functions import clear_screen, log_action, hash_animal_data, generate_salt
from sudo_user import sudo_user
from pymongo import MongoClient
from config import mongodb_uri

# Connect to MongoDB
uri = mongodb_uri 
client = MongoClient(uri)

db = client['animal_rescue']
animals_collection = db['animals']

def add_animal():
    # Continuous loop for adding animals
    while True:
        clear_screen()

        # Display header 
        print(Fore.CYAN + "\n🐾 Add Animal 🐾\n" + Style.RESET_ALL)

        print("Enter animal details or type 'exit' to cancel:")

        # Input fields for animal data
        name = input(Fore.CYAN + "Name: " + Style.RESET_ALL).strip()

        # Check if user wants to exit
        if name.lower() == 'exit':
            print(Fore.YELLOW + "\nExiting..." + Style.RESET_ALL)
            time.sleep(2)
            break

        species = input(Fore.GREEN + "Species: " + Style.RESET_ALL).strip()
        breed = input(Fore.GREEN + "Breed: " + Style.RESET_ALL).strip()
        gender = input(Fore.GREEN + "Gender: " + Style.RESET_ALL).strip()
        age = input(Fore.GREEN + "Age: " + Style.RESET_ALL).strip()

        # Validate input fields
        if not all([name, species, breed, gender, age]):
            print(Fore.RED + "\nInvalid input. All fields are required." + Style.RESET_ALL)
            input(Fore.GREEN + "Press Enter to continue..." + Style.RESET_ALL)
            continue

        # Validate age as positive integer
        if not age.isdigit() or int(age) <= 0:
            print(Fore.RED + "\nInvalid age. Please enter a positive integer." + Style.RESET_ALL)
            input(Fore.GREEN + "Press Enter to continue..." + Style.RESET_ALL)
            continue

        age = int(age)

        # Make the user verify their identity
        current_user = sudo_user() 

        # Generate salt
        salt = generate_salt()

        # Hash the new animal data with the salt
        hashed_animal_data = hash_animal_data({
            'name': name,
            'species': species,
            'breed': breed,
            'gender': gender,
            'age': age,
            'adopted': False
        }, salt)

        # Store the salt in hexadecimal format
        salt_hex = salt.hex()

        # Add hashed animal data to the animals dictionary
        animals_collection.insert_one ({
            'name': name,
            'species': species,
            'breed': breed,
            'gender': gender,
            'age': age,
            'adopted': False,
            'salt': salt_hex,
            'hashed_animal_data': hashed_animal_data,
        })

        # Log the action of adding the animal into the audit file
        log_action(current_user, f"Added animal: {name}, {species}, {breed}")

        # Confirm successful addition of the animal 
        print(Fore.GREEN + "\n✨ Animal added successfully! ✨" + Style.RESET_ALL)
        log_action(current_user, f"Exited 'Add an animal'")
        time.sleep(2)

        # Exit the loop after successful addition
        break 