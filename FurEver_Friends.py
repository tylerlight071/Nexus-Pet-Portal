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
    print("Your password must be changed from the default 'ADMIN' for security reasons.")
    new_password = getpass.getpass("Enter a new password for ADMIN: ")
    confirm_password = getpass.getpass("Confirm the new password: ")

    if new_password == confirm_password:
        with open(USER_DATA_FILE, 'r+') as user_file:
            data = json.load(user_file)
            data["ADMIN"] = new_password
            user_file.seek(0)
            json.dump(data, user_file, indent=4)
            user_file.truncate()
            print("Password changed successfully!")
            time.sleep(2)
            clear_screen()
    else:
        print("Passwords do not match. Please try again.")
        time.sleep(2)
        clear_screen()
        change_admin_password()

def login():
    while True:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        with open(USER_DATA_FILE, 'r') as user_file:
            users = json.load(user_file)

            if username in users:
                if users[username] == password:
                    if username == "ADMIN":
                        if username == "ADMIN" and password == "ADMIN":
                            change_admin_password()
                            admin_dashboard()
                        else:
                            admin_dashboard()                           
                    return username
                else:
                    print("Incorrect password. Please try again.")
                    time.sleep(2)
                    clear_screen()
            else:
                print("Username not found. Please try again.")
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
        print(Fore.CYAN + "\nWelcome to the Animal Adoption System!" + Style.RESET_ALL)
        print("1. Login")
        print("2. Exit")
        choice = input("Please select an option: ")

        if choice == '1':
            clear_screen()
            username = login()
            if username is not None:
                while True:
                    clear_screen()
                    print("\nMenu:")
                    print("1. Add a new animal")
                    print("2. View all animals")
                    print("3. Change animal to adopted")
                    print("4. Logout")
                    option = input("Please select an option: ")

                    if option == '1':
                        add_animal()
                    elif option == '2':
                        view_animals()
                    elif option == '3':
                        change_adopted_status()
                    elif option == '4':
                        print("Logging out...")
                        clear_screen()
                        break
                    else:
                        print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)
                        time.sleep(2)
                        clear_screen()
        elif choice == '2':
            print("Exiting...")
            time.sleep(2)
            exit()
        else:
            print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()

if __name__ == "__main__":
    main()
