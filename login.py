import getpass
import time
from colorama import Fore, Style
from tabulate import tabulate
from common_functions import clear_screen, log_action, hash_password, verify_password, get_mongodb_uri
from admin_dashboard import admin_dashboard
from pymongo import MongoClient


MAX_ATTEMPTS = 3

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)
db = client['animal_rescue']
users_collection = db['users']

def change_admin_password(username):
    clear_screen()

    # Notify the user about changing the ADMIN password
    print(Fore.YELLOW + "\nYour password must be changed from the default 'ADMIN' for security reasons." + Style.RESET_ALL)

    # Prompt user for a new password and confirmation
    while True:
        new_password = getpass.getpass("\nEnter a new password for ADMIN: ")
        if not new_password.strip():
            clear_screen()
            print(Fore.RED + "\nPassword cannot be empty. Please try again." + Style.RESET_ALL)
            continue
        break

    confirm_password = getpass.getpass("Confirm the new password: ")

    # Check if passwords match
    if new_password == confirm_password:
        # Generate salt and hash password
        hashed_password = hash_password(new_password)

        # Update the password in the MongoDB collection for ADMIN
        users_collection.update_one(
            {'username': 'ADMIN'},
            {'$set': {'hashed_password': hashed_password}}
        )

        log_action("ADMIN", "ADMIN Password has been changed")
        print(Fore.GREEN + "\nPassword changed successfully!" + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
    else:
        # Notify the user about mismatching passwords and prompt again
        print(Fore.RED + "\nPasswords do not match. Please try again." + Style.RESET_ALL)
        log_action(username, "Failed attempt to access ADMIN")
        time.sleep(2)
        clear_screen()
        change_admin_password(username)

def reset_password(username):
    clear_screen()

    # Notify the user about changing the password
    print(Fore.YELLOW + "\nYour password must be changed for security reasons." + Style.RESET_ALL)

    # Prompt user for a new password and confirmation
    while True:
        new_password = getpass.getpass("\nEnter a new password: ")
        if not new_password.strip():
            clear_screen()
            print(Fore.RED + "\nPassword cannot be empty. Please try again." + Style.RESET_ALL)
            continue
        break

    confirm_password = getpass.getpass("Confirm the new password: ")

    # Check if passwords match
    if new_password == confirm_password:
        hashed_password = hash_password(new_password)

        # Update the password in the MongoDB collection
        users_collection.update_one(
            {'username': username},
            {'$set': {'hashed_password': hashed_password}}
        )

        log_action(username, f"Password has been reset for user {username}")
        print(Fore.GREEN + "\nPassword changed successfully!" + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
    else:
        # Notify the user about mismatching passwords and prompt again
        print(Fore.RED + "\nPasswords do not match. Please try again." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        reset_password(username)

def login():
    clear_screen()
    attempts = 0
    # Continuous loop for login
    while attempts < MAX_ATTEMPTS:
        # Display login prompt
        print(tabulate([["\n👤 User Login 👤"]], tablefmt='fancy_grid'))
        username = input("\nEnter your username: ")
        password = getpass.getpass("Enter your password: ")

        # Query user credentials from MongoDB
        user = users_collection.find_one({'username': username})

        if user and verify_password(user['hashed_password'], password):
            return handle_successful_login(user, username, password)
        else:
            handle_failed_login(username, password, attempts)
            attempts += 1
        
    # If user exceeds maximum login attempts
    print(Fore.RED + "\nYou have exceeded the maximum number of login attempts." + Style.RESET_ALL)
    time.sleep(1)
    log_action(username, "Failed to login")
    print("Exiting...")
    time.sleep(2)
    exit()

def handle_successful_login(user, username, password):
    user_level = user['level']
    print("\nLogging in...")
    time.sleep(2)

    if username == "ADMIN":
        if password == "ADMIN":
            change_admin_password(username)
            admin_dashboard()
        else:
            admin_dashboard()
    elif password == "password":
        reset_password(username)
    else:
        log_action(username, "Logged in")

    return username, user_level

def handle_failed_login(user, username, attempts):
    if user:
        print(Fore.RED + "\nInvalid password. Please try again." + Style.RESET_ALL)
        log_action(username, "Failed to login")
    else:
        print(Fore.RED + "\nUser not found. Please try again." + Style.RESET_ALL)
        log_action(username, "Failed to be found")
    
    time.sleep(2)
    print(Fore.RED + f"\nYou have {MAX_ATTEMPTS - attempts} attempts remaining." + Style.RESET_ALL)
    clear_screen()