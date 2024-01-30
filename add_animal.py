import time
from colorama import Fore, Style
from common_functions import clear_screen, load_data, save_data, log_action
from sudo_user import sudo_user

ANIMAL_DATA_FILE = "animals.json"

def add_animal():
    # Load animal data from file
    animals = load_data(ANIMAL_DATA_FILE)

    # Continuous loop for adding animals
    while True:
        clear_screen()

        # Display header 
        print(Fore.CYAN + "\n🐾 Add Animal 🐾\n" + Style.RESET_ALL)

        print("Enter animal details or type 'exit' to cancel:")

        #Input fields for animal data
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

        # Add animals to the data dictionary
        animals[name] = {
            'name': name,
            'species': species,
            'breed': breed,
            'gender': gender,
            'age': age,
            'adopted': False
        }

        # Make the user verify their identity
        current_user = sudo_user() 

        save_data(animals, ANIMAL_DATA_FILE)

        # Log the action of adding animal into the audit file
        log_action(current_user, f"Added animal: {name}")

        # Confirm successful addition of the animal 
        print(Fore.GREEN + "\n✨ Animal added successfully! ✨" + Style.RESET_ALL)
        time.sleep(2)

        # Exit the loop after successful addition
        break 
