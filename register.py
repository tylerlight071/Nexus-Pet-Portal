import getpass
import time
from colorama import Fore, Style
from common_functions import clear_screen, generate_salt, hash_password
from pymongo import MongoClient
from config import mongodb_uri

# Connect to MongoDB
uri = mongodb_uri
client = MongoClient(uri)
db = client['animal_rescue']
users_collection = db['users']

def register():
    clear_screen()

    while True:
        # Prompt user to enter a username
        username = input("\nEnter a username: ").strip()
        
        # Check if username already exists in the database
        if users_collection.find_one({'username': username}):
            print(Fore.RED + "\nUsername already exists. Please choose another one." + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
            continue

        # Continuous loop for user registration
        while True:
            # Prompt user to enter and confirm a password
            password = getpass.getpass("Enter a password: ")
            confirm_password = getpass.getpass("Confirm your password: ")

            # Check if passwords match
            if password == confirm_password:
                # Prompt user to enter their user level
                user_level = input("Enter your user level (1-3): ")
                
                # Validate user level input
                if user_level.isdigit() and 1 <= int(user_level) <= 3:
                    # Generate salt and hash password
                    salt = generate_salt()
                    hashed_password = hash_password(password, salt)

                    # Convert salt to hexadecimal string for serialization
                    salt_hex = salt.hex()

                    # Insert user data into the MongoDB collection
                    users_collection.insert_one({
                        'username': username,
                        'hashed_password': hashed_password,
                        'salt': salt_hex,
                        'level': int(user_level)
                    })

                    print(Fore.GREEN + "\nRegistration successful!" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    return
                else:
                    print(Fore.RED + "\nInvalid user level. Please enter a number between 1 and 3." + Style.RESET_ALL)
            else:
                print(Fore.RED + "\nPasswords do not match. Please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    register()
