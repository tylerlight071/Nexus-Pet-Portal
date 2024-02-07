import getpass
import time
from colorama import Fore, Style
from common_functions import clear_screen, hash_password, get_mongodb_uri
from pymongo import MongoClient

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)
db = client['animal_rescue']
users_collection = db['users']

def register():
    clear_screen()

    while True:
        username = get_username()
        if username is None:
            continue

        password = get_password("Enter a password: ")
        if password is None:
            continue

        confirm_password = get_password("Confirm your password: ")
        if confirm_password is None:
            continue

        if password != confirm_password:
            print_error_message("\nPasswords do not match. Please try again.")
            continue

        user_level = get_user_level()
        if user_level is None:
            continue

        hashed_password = hash_password(password)
        users_collection.insert_one({
            'username': username,
            'hashed_password': hashed_password,
            'level': int(user_level)
        })

        print(Fore.GREEN + "\nRegistration successful!" + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        return

def get_username():
    username = input("\nEnter a username: ").strip()
    if username == "":
        print_error_message("\nUsername cannot be empty. Please try again.")
        return None
    if users_collection.find_one({'username': username}):
        print_error_message("\nUsername already exists. Please choose another one.")
        time.sleep(2)
        clear_screen()
        return None
    return username

def get_password(prompt):
    password = getpass.getpass(prompt)
    if not password.strip():
        print_error_message("\nPassword cannot be empty. Please try again.")
        return None
    return password

def get_user_level():
    user_level = input("Enter your user level (1-3): ")
    if not user_level.isdigit() or not 1 <= int(user_level) <= 3:
        print_error_message("\nInvalid user level. Please enter a number between 1 and 3.")
        return None
    return user_level

def print_error_message(message):
    clear_screen()
    print(Fore.RED + message + Style.RESET_ALL)