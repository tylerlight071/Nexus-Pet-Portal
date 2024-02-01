import os
import time
from colorama import Fore, Style
from view_animals import view_animals
from add_animal import add_animal
from customer_adoption_form import view_available_animals
from common_functions import clear_screen, log_action, generate_salt, hash_password, load_animal_data
from login import login
from edit_animal_entries import modify_animal
from pymongo import MongoClient
from pymongo.errors import InvalidURI
from config import mongodb_uri

# Check if config.py exists, if not, prompt the user to enter MongoDB URI and create it
if os.path.isfile('config.py'):
    # Read the contents of the config file:
    with open('config.py', 'r') as f:
        config_content = f.read()
    # Check if the URI has been inputted in the file
    if 'URI Inputted' in config_content:
        uri_inputted = True
    else:
        uri_inputted = False
else:
    uri_inputted = False

if not uri_inputted:
    while True:
        clear_screen()
        mongodb_uri = input("\nPlease enter your MongoDB connection URI: ")
        try:
            client = MongoClient(mongodb_uri)
            db = client['animal_rescue']
            users_collection = db['users']
            print(Fore.GREEN + "\nConnected to MongoDB successfully." + Style.RESET_ALL)
            time.sleep(2)
            print(Fore.GREEN + "\nConfig file updated successfully." + Style.RESET_ALL)
            time.sleep(2)
            print(Fore.GREEN + "\nDefault user created successfully." + Style.RESET_ALL)
            time.sleep(2)
            print(Fore.YELLOW + "\nThe application will now close. Please restart to begin." + Style.RESET_ALL)
            input("\nPress any key to exit.")
            # Update config file to indicate that URI has been inputted
            with open('config.py', 'w') as f:
                f.write(f"mongodb_uri = '{mongodb_uri}'\n")
                f.write("# URI Inputted\n")
            exit()
        except InvalidURI:
            print(Fore.RED + "\nInvalid MongoDB URI. Please check and try again." + Style.RESET_ALL)
            print(Fore.YELLOW + "Note: Please ensure that your MongoDB URI is correctly formatted and does not contain any errors." + Style.RESET_ALL)
            time.sleep(2)
            print(Fore.YELLOW + "\nThe application will now close. Please restart to begin." + Style.RESET_ALL)
            time.sleep(2)
            input("\nPress any key to exit.")
            exit()
        except Exception as e:
            print(Fore.RED + f"\nAn error occurred: {e}" + Style.RESET_ALL)
            time.sleep(2)
            print(Fore.YELLOW + "\nThe application will now close. Please restart to begin." + Style.RESET_ALL)
            time.sleep(2)
            input("\nPress any key to exit.")
            exit()
else:
    pass

# Connect to MongoDB
uri = mongodb_uri
client = MongoClient(uri)
db = client['animal_rescue']
users_collection = db['users']

# Default password
default_password = "ADMIN"

# Generate salt and hash password
salt = generate_salt()
hashed_password = hash_password(default_password, salt)

salt_hex = salt.hex()

# Default user data if collection do not exist
DEFAULT_USER_DATA = {
    "username": "ADMIN",
    "hashed_password": hashed_password,
    "salt": salt_hex,
    "level": 3
}

def main():
    clear_screen()

    try:
        while True:
            # Display main menu options
            print(Fore.CYAN + "\n🐕 Welcome to FurEver Friends Management System! 🐈" + Style.RESET_ALL)
            print("\n1. " + Fore.GREEN + "Login" + Style.RESET_ALL)
            print("2. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
            choice = input("\nPlease select an option: ")

            if choice == '1':
                clear_screen()
                # Pull the username and user level from the login function
                current_user, user_level = login()
                if current_user is not None:
                    while True:
                        clear_screen()
                        # Display main menu after successful login
                        print(Fore.CYAN + "\n📖 Main Menu 📖" + Style.RESET_ALL)
                        print("\n1. " + Fore.GREEN + "🔎 View all animals" + Style.RESET_ALL)

                        # Initialize option counter
                        option_counter = 2

                        # Adjust options based on user level
                        if user_level >= 2:
                            print(f"{option_counter}. " + Fore.GREEN + "🐶 Add a new animal" + Style.RESET_ALL)
                            option_counter += 1
                        if user_level >= 3:
                            print(f"{option_counter}. " + Fore.GREEN + "🏡 Customer Adoption Form" + Style.RESET_ALL)
                            option_counter += 1
                        if user_level >= 3:
                            print(f"{option_counter}. " + Fore.GREEN + "🗒️ Edit animal entries" + Style.RESET_ALL)
                            option_counter += 1

                        # Display Logout option with the correct number
                        print (f"{option_counter}. " + Fore.YELLOW + "🔐 Logout" + Style.RESET_ALL)
                        option = input("\nPlease select an option: ")

                        if option == '1':
                            time.sleep(1)
                            log_action(current_user, "Entered, 'Animal Database" )
                            view_animals()
                        elif option == '2' and user_level >= 2:
                            time.sleep(1)
                            log_action(current_user, "Entered 'Add an animal'")
                            add_animal()
                        elif option == '3' and user_level >= 3:
                            time.sleep(1)
                            view_available_animals()
                        elif option == '4' and user_level >= 3:
                            time.sleep(1)
                            modify_animal()
                        elif option == str(option_counter) and user_level >= 1:
                            print("\nLogging out...")
                            time.sleep(2)
                            log_action(current_user, f"Logged Out")
                            clear_screen()
                            break
                        else:
                            print(Fore.RED + "\nInvalid option. Please try again.")
                            time.sleep(2)
                            clear_screen()

            elif choice == '2':
                print("\nExiting...")
                time.sleep(2)
                exit()
            else:
                print(Fore.RED + "\nInvalid option. Please try again." + Style.RESET_ALL)
                time.sleep(2)
                clear_screen()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        time.sleep(2)

if __name__ == "__main__":
    # Check if the users collection exists, if not, create it with default values
    collection_names = db.list_collection_names()
    if 'users' not in collection_names:
        users_collection.insert_one(DEFAULT_USER_DATA)
    main()