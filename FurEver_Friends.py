import time
from sys import exit
from colorama import Fore, Style
from view_animals import view_animals
from add_animal import add_animal
from customer_adoption_form import view_available_animals
from common_functions import clear_screen, log_action, hash_password, get_mongodb_uri
from login import login
from edit_animal_entries import modify_animal
from pymongo import MongoClient

get_mongodb_uri()

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)
db = client['animal_rescue']
users_collection = db['users']

# Default password
default_password = "ADMIN"

# Generate salt and hash the default password
hashed_password = hash_password(default_password)


# Default user data if collection do not exist
DEFAULT_USER_DATA = {
    "username": "ADMIN",
    "hashed_password": hashed_password,
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