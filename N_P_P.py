import time
from sys import exit
from colorama import Fore, Style
from notifications import notifications
from staff_portal import staff_portal
from view_animals import view_animals
from common_functions import clear_screen, log_action, hash_password, get_mongodb_uri
from login import login
from client_database import client_database
from pymongo import MongoClient
from tabulate import tabulate

get_mongodb_uri()

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)
db = client['animal_rescue']
users_collection = db['users']
animals_collection = db['animals']

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

def logout():
    return True

# Main menu
def display_menu(options):
    table_data = [[i, option] for i, option in enumerate(options, 1)]
    print(tabulate(table_data, tablefmt='fancy_grid'))

def handle_option(option, functions):
    try:
        # Convert the option to an integer
        option = int(option)
        # Call the function that corresponds to the selected option
        function_choice = functions[option - 1]
        result = function_choice()
        return result
    except (IndexError, ValueError):
        print(Fore.RED + "\nInvalid option. Please try again." + Style.RESET_ALL)
        time.sleep(2)

def main_menu():
    options = [Fore.GREEN + "Login" + Style.RESET_ALL, Fore.YELLOW + "Exit" + Style.RESET_ALL]
    functions = [login, exit]
    while True:
        clear_screen()
        welcome_table = [[Fore.CYAN + "🐕 Welcome to Nexus Pet Portal! 🐈" + Style.RESET_ALL]]
        options_table = [[f"{i}. {option}"] for i, option in enumerate(options, 1)]
        options_table.append(["Please select an option:"])
        print(tabulate(welcome_table, tablefmt='fancy_grid'))
        print(tabulate(options_table, tablefmt='fancy_grid'))
        choice = input("\n> ")
        user_details = handle_option(choice, functions)
        if user_details is not None:
            user_menu(user_details[0], user_details[1])

def user_menu(current_user, user_level):
    clear_screen()
    options = [Fore.GREEN + "🐶 Animal Database" + Style.RESET_ALL]
    functions = [view_animals]
    # Add options and functions based on user level
    if user_level >= 2:
        options.append(Fore.GREEN + "🧑 Client Database" + Style.RESET_ALL)
        functions.append(client_database)
    if user_level >= 3:
        options.append(Fore.GREEN + "👤 Staff Portal" + Style.RESET_ALL)
        functions.append(staff_portal)
    # Add common options and functions
    options.append(Fore.GREEN + "🔔 Notifications" + Style.RESET_ALL)
    options.append(Fore.YELLOW + "🔐 Logout" + Style.RESET_ALL)
    functions.append(notifications)
    functions.append(logout)
    while True:
        clear_screen()
        menu_table = [[Fore.CYAN + "📖 Main Menu 📖" + Style.RESET_ALL]]
        options_table = [[f"{i}. {option}"] for i, option in enumerate(options, 1)]
        options_table.append(["Please select an option:"])
        print(tabulate(menu_table, tablefmt='fancy_grid'))
        print(tabulate(options_table, tablefmt='fancy_grid'))
        choice = input("\n> ")
        # Logout option
        if choice == str(len(options)):  
            log_action(current_user, "Logged out")
            print("\nLogging out...")
            time.sleep(2)
            clear_screen()
            break
        handle_option(choice, functions)

def main():
    clear_screen()
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        time.sleep(2)

if __name__ == "__main__":
    # Check if the users collection exists, if not, create it with default values
    collection_names = db.list_collection_names()
    if 'users' not in collection_names:
        users_collection.insert_one(DEFAULT_USER_DATA)
    main()