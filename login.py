import getpass
import time
from colorama import Fore, Style
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
        else:
            break

    confirm_password = getpass.getpass("Confirm the new password: ")

    # Check if passwords match
    if new_password == confirm_password:
        # Generate salt and hash password

        hashed_password = hash_password(new_password)

        # Convert salt to hexadecimal string for serialization   

        # Update the password in the MongoDB collection for ADMIN
        users_collection.update_one(
            {'username': 'ADMIN'},
            {'$set': {'hashed_password': hashed_password}}
        )

        log_action(username, f"Admin Password has been changed")
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
    print(Fore.YELLOW + f"\nYour password must be changed for security reasons." + Style.RESET_ALL)

    # Prompt user for a new password and confirmation
    while True:
        new_password = getpass.getpass("\nEnter a new password: ")
        if not new_password.strip():
            clear_screen()
            print(Fore.RED + "\nPassword cannot be empty. Please try again." + Style.RESET_ALL)
            continue
        else:
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
    attempts = 0
    # Continuous loop for login
    while attempts < MAX_ATTEMPTS:
        # Display login prompt
        print("\n👤 User Login 👤")
        username = input("\nEnter your username: ")
        password = getpass.getpass("Enter your password: ")  # No need for getpass as input is hidden in most consoles

        # Query user credentials from MongoDB
        user = users_collection.find_one({'username': username})

        if user:
            stored_password = user['hashed_password']

            # Verify the entered password with the stored password hash
            if verify_password(stored_password, password):
                user_level = user['level'] 

                if username == "ADMIN" and password == "ADMIN":
                    print("\nLogging In...")
                    time.sleep(2)
                    change_admin_password(username)
                    admin_dashboard()
                    return username, user_level
                
                elif username == "ADMIN":
                    log_action(username, f"ADMIN Logged In")
                    print("\nLogging In...")
                    time.sleep(2)
                    admin_dashboard()
                    return username, user_level
                
                elif password == "password":
                    print("\nLogging In...")
                    # Pass username to the reset_password function
                    reset_password(username) 

                else:
                    print("\nLogging in...")
                    time.sleep(2)
                    log_action(username, f"Logged In")
                    return username, user_level 
                
            else:
                print(Fore.RED + "\nIncorrect password." + Style.RESET_ALL)
                attempts += 1
                time.sleep(2)
                print(Fore.RED + f"\nRemaining attempts: {MAX_ATTEMPTS - attempts}" + Style.RESET_ALL)
                log_action(username, "Failed login attempt")
                time.sleep(2)
                clear_screen()

        else:
            print(Fore.RED + "\nUsername not found. Please try again." + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()

    print(Fore.RED + "\nMaximum login attempts reached" + Style.RESET_ALL)
    time.sleep(1)
    print("\nExiting...")
    time.sleep(2)
    exit()