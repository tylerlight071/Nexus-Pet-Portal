import os
import json
import time
import getpass
from colorama import Fore, Style
from view_animals import view_animals
from add_animal import add_animal
from change_adopted_status import change_adopted_status
from common_functions import clear_screen, save_data
from admin_dashboard import admin_dashboard

# File paths for user and animal data
USER_DATA_FILE = "users.json"
ANIMAL_DATA_FILE = "animals.json"

# Default user data if files do not exist
DEFAULT_USER_DATA = {"ADMIN": "ADMIN"}
DEFAULT_ANIMAL_DATA = {}

def change_admin_password():
    clear_screen()
    print(Fore.YELLOW + "\nYour password must be changed from the default 'ADMIN' for security reasons." + Style.RESET_ALL)
    new_password = getpass.getpass("\nEnter a new password for ADMIN: ")
    confirm_password = getpass.getpass("Confirm the new password: ")

    if new_password == confirm_password:
        with open(USER_DATA_FILE, 'r+') as user_file:
            data = json.load(user_file)
            data["ADMIN"] = new_password
            user_file.seek(0)
            json.dump(data, user_file, indent=4)
            user_file.truncate()
            print(Fore.GREEN + "\nPassword changed successfully!" + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
    else:
        print(Fore.RED + "\nPasswords do not match. Please try again." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        change_admin_password()

def login():
    while True:
        print("\n👤 User Login 👤")
        username = input("\nEnter your username: ")
        password = getpass.getpass("Enter your password: ")

        with open(USER_DATA_FILE, 'r') as user_file:
            users = json.load(user_file)

            if username in users:
                if users[username] == password:
                    if username == "ADMIN" and password == "ADMIN":
                        change_admin_password()
                        admin_dashboard()
                        return username  # Ensure to return after admin login
                    elif username == "ADMIN":
                        admin_dashboard()
                        return username
                    else:
                        return username  # Return username for non-admin users
                else:
                    print(Fore.RED + "\nIncorrect password. Please try again." + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
            else:
                print(Fore.RED + "\nUsername not found. Please try again." + Style.RESET_ALL)
                time.sleep(2)
                clear_screen()

def main():
    clear_screen()

    # Check if user.json exists, if not, create it with default data
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as user_file:
            json.dump(DEFAULT_USER_DATA, user_file, indent=4)

    # Check if animals.json exists, if not, create it with default data
    if not os.path.exists(ANIMAL_DATA_FILE):
        with open(ANIMAL_DATA_FILE, 'w') as animal_file:
            json.dump(DEFAULT_ANIMAL_DATA, animal_file, indent=4)

    while True:
        print(Fore.CYAN + "\n🐕 Welcome to FurEver Friends Management System! 🐈" + Style.RESET_ALL)
        print("\n1. " + Fore.GREEN + "Login" + Style.RESET_ALL)
        print("2. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
        choice = input("\nPlease select an option: ")

        if choice == '1':
            clear_screen()
            username = login()
            if username is not None:
                while True:
                    clear_screen()
                    print(Fore.CYAN + "\n📖 Main Menu 📖" + Style.RESET_ALL)
                    print("\n1. " + Fore.GREEN + "🐶 Add a new animal" + Style.RESET_ALL)
                    print("2. " + Fore.GREEN + "🔎 View all animals" + Style.RESET_ALL)
                    print("3. " + Fore.GREEN + "🏡 Change animal adoption status" + Style.RESET_ALL)
                    print("4. " + Fore.YELLOW + "🔐 Logout" + Style.RESET_ALL)
                    option = input("\nPlease select an option: ")

                    if option == '1':
                        add_animal()
                    elif option == '2':
                        view_animals()
                    elif option == '3':
                        change_adopted_status()
                    elif option == '4':
                        print("\nLogging out...")
                        clear_screen()
                        break
                    else:
                        print(Fore.RED + "\nInvalid option. Please try again." + Style.RESET_ALL)
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

if __name__ == "__main__":
    main()
