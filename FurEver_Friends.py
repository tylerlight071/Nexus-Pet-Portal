import json
import os
from colorama import Fore, Style
import getpass

# File paths for user and animal data
USER_DATA_FILE = "users.json"
ANIMAL_DATA_FILE = "animals.json"

# Initialize empty data files if they don't exist
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump({}, f)

if not os.path.exists(ANIMAL_DATA_FILE):
    with open(ANIMAL_DATA_FILE, 'w') as f:
        json.dump({}, f)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)

def save_data(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

def register():
    users = load_data(USER_DATA_FILE)
    username = input("Enter a username: ")
    if username in users:
        print(Fore.RED + "Username already exists. Please choose another one." + Style.RESET_ALL)
        return register()
    password = getpass.getpass("Enter a password: ")
    users[username] = password
    save_data(users, USER_DATA_FILE)
    print(Fore.GREEN + "Registration successful!" + Style.RESET_ALL)

def login():
    users = load_data(USER_DATA_FILE)
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    if users.get(username) == password:
        print(Fore.GREEN + "Login successful!" + Style.RESET_ALL)
        return username
    else:
        print(Fore.RED + "Invalid username or password. Please try again." + Style.RESET_ALL)
        return login()

def add_animal():
    animals = load_data(ANIMAL_DATA_FILE)
    name = input("Enter the animal's name: ")
    species = input("Enter the animal's species: ")
    animals[name] = {'species': species, 'adopted': False}
    save_data(animals, ANIMAL_DATA_FILE)
    print(Fore.GREEN + "Animal added successfully!" + Style.RESET_ALL)

def view_animals():
    animals = load_data(ANIMAL_DATA_FILE)
    print("\nList of Animals:")
    for name, data in animals.items():
        print(f"Name: {name}, Species: {data['species']}, Adopted: {data['adopted']}")

def change_adopted_status():
    animals = load_data(ANIMAL_DATA_FILE)
    name = input("Enter the name of the animal to mark as adopted: ")
    if name in animals:
        animals[name]['adopted'] = True
        save_data(animals, ANIMAL_DATA_FILE)
        print(Fore.GREEN + f"{name} has been marked as adopted!" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"No animal found with the name {name}" + Style.RESET_ALL)

def main():
    clear_screen()
    while True:
        print(Fore.CYAN + "Welcome to the Animal Adoption System!" + Style.RESET_ALL)
        print("1. Register")
        print("2. Login")
        choice = input("Please select an option: ")

        if choice == '1':
            clear_screen()
            register()
        elif choice == '2':
            clear_screen()
            username = login()
            while True:
                print("\nMenu:")
                print("1. Add a new animal")
                print("2. View all animals")
                print("3. Change animal to adopted")
                print("4. Logout")
                option = input("Please select an option: ")

                if option == '1':
                    clear_screen()
                    add_animal()
                elif option == '2':
                    clear_screen()
                    view_animals()
                elif option == '3':
                    clear_screen()
                    change_adopted_status()
                elif option == '4':
                    print("Logging out...")
                    break
                else:
                    print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
