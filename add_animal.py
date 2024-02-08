import time
from colorama import Fore, Style
from common_functions import clear_screen, log_action, get_mongodb_uri, load_animal_data
from sudo_user_login import SudoUser
from tables import print_animal_table
from pymongo import MongoClient

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)

db = client['animal_rescue']
animals_collection = db['animals']
users_collection = db['users']

def add_animal():

    animals = load_animal_data(animals_collection)

    # Continuous loop for adding animals
    while True:
        clear_screen()

        SudoUser(users_collection.database).login()

        # Display header 
        print(Fore.CYAN + "\n🐾 Add Animal 🐾\n" + Style.RESET_ALL)

        print("Enter animal details or type 'exit' to cancel:")

        # Input fields for animal data
        name = input(Fore.GREEN + "\nName: " + Style.RESET_ALL).strip().capitalize()  # Capitalize the first letter

        # Check if user wants to exit
        if name.lower() == 'exit':
            print("\nExiting..." + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
            print_animal_table(animals)
            break

        species = input(Fore.GREEN + "Species: " + Style.RESET_ALL).strip().capitalize()  # Capitalize the first letter
        breed = input(Fore.GREEN + "Breed: " + Style.RESET_ALL).strip().capitalize()  # Capitalize the first letter
        gender = input(Fore.GREEN + "Gender: " + Style.RESET_ALL).strip().capitalize()  # Capitalize the first letter
        age = input(Fore.GREEN + "Age: " + Style.RESET_ALL).strip()

        # Validate input fields
        if not all([name, species, breed, gender, age]):
            print(Fore.RED + "\nInvalid input. All fields are required." + Style.RESET_ALL)
            time.sleep(2)
            continue

        # Validate gender fields
        if gender.lower() not in ["male", "female"]:
            print(Fore.RED + "\nInvalid input. Gender must be 'Male' or 'Female'." + Style.RESET_ALL)
            time.sleep(2)
            continue

        # Validate age as positive integer
        if not age.isdigit() or int(age) <= 0:
            print(Fore.RED + "\nInvalid age. Please enter a positive integer." + Style.RESET_ALL)
            time.sleep(2)
            continue

        age = int(age)

        clear_screen()
        # Make the user verify their identity
        current_user = SudoUser(users_collection.database).login() 

        # Add hashed animal data to the animals collection
        animals_collection.insert_one ({
            'name': name,
            'species': species,
            'breed': breed,
            'gender': gender,
            'age': age,
            'adopted': False,
        })

        # Log the action of adding the animal into the audit file
        log_action(current_user, f"Added animal: {name}, {species}, {breed}")

        # Confirm successful addition of the animal 
        print(Fore.GREEN + "\n✨ Animal added successfully! ✨" + Style.RESET_ALL)
        log_action(current_user, "Exited 'Add an animal'")
        time.sleep(2)

        # Ask if the user wants to add another animal
        add_another = input(Fore.LIGHTYELLOW_EX + "Do you want to add another animal? (yes/no): " + Style.RESET_ALL)
        if add_another.lower() == 'no':
            break