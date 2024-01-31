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


def user_management():
    # Continuous loop for user management options
    while True:
        clear_screen()
        print(Fore.YELLOW + "\nUser Management\n" + Style.RESET_ALL)
        print("1. Change user password")
        print("2. Update user information")
        print("3. Delete user")
        print("4. Back to admin dashboard")
        option = input("\nPlease select an option: ")

        # Perform actions based on user input
        if option == '1':
            reset_user_password()
        elif option == '2':
            update_user_information()
        elif option == '3':
            delete_user()
        elif option == '4':
            print("\nReturning to admin dashboard...")
            time.sleep(2)
            return
        else:
            print(Fore.RED + "\nInvalid option. Please try again." + Style.RESET_ALL)
            time.sleep(2)

def reset_user_password():
    # Prompt for username and new password
    username = input("\nEnter the username to change the password: ")

    # Change password if the user exists and is not ADMIN
    user = users_collection.find_one({'username': username})
    if user and username != "ADMIN": 
        new_password = "password"

        # Generate salt and hash password
        salt = generate_salt()
        hashed_password = hash_password(new_password, salt)

        # Convert salt to hexadecimal string for serialization
        salt_hex = salt.hex()
        
        # Update user's password and salt
        users_collection.update_one({'username': username}, 
                                    {'$set': {'hashed_password': hashed_password, 'salt': salt_hex}})
        print(Fore.GREEN + f"\nPassword for user '{username}' reset successfully!" + Style.RESET_ALL)
    
    elif username == "ADMIN":  
        print(Fore.RED + "\nYou cannot change the password for the ADMIN user." + Style.RESET_ALL)
    
    else:
        print(Fore.RED + f"\nUser '{username}' not found." + Style.RESET_ALL)
    time.sleep(2)

def update_user_information():
    # Prompt for username to update information
    username = input("\nEnter the username to update information: ")

    user = users_collection.find_one({'username': username})
    if user and username != "ADMIN":  
        print("\nCurrent user information:")
        print(f"\nUsername: {username}")
        print(f"User Level: {user['level']}")
        
        # Prompt for the information to be updated
        print("\nSelect the information you want to update:")
        print("\n1. Username")
        print("2. User Level")
        print("3. Cancel")
        
        option = input("\nEnter your choice: ")
        
        # Process user's choice and perform updates accordingly
        if option == '1':
            new_username = input("Enter the new username: ")
            if not users_collection.find_one({'username': new_username}):  
                users_collection.update_one({'username': username}, {'$set': {'username': new_username}})
                print(Fore.GREEN + f"\nUsername updated successfully to '{new_username}'!" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"\nUsername '{new_username}' already exists. Please choose a different username." + Style.RESET_ALL)
        elif option == '2':
            new_level = int(input("Enter the new user level: "))
            users_collection.update_one({'username': username}, {'$set': {'level': new_level}})
            print(Fore.GREEN + f"\nUser level updated successfully for '{username}'!" + Style.RESET_ALL)
        elif option == '3':
            print("\nOperation canceled.")
        else:
            print(Fore.RED + "\nInvalid option. Please try again." + Style.RESET_ALL)
    elif username == "ADMIN": 
        print(Fore.RED + "\nYou cannot update information for the ADMIN user." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"\nUser '{username}' not found." + Style.RESET_ALL)

    time.sleep(2)

def delete_user():
    # Prompt for username to be deleted
    username = input("\nEnter the username to delete: ")
    confirm_delete = input("Are you sure you want to delete this user? (y/n) ")

    # Throw error if user tries to delete ADMIN user
    if username == "ADMIN":
        print("\nThe ADMIN user cannot be modified.")
        time.sleep(2)
        clear_screen()
        delete_user()
    
    # Process user's choice and perform deletion accordingly
    else:
        user = users_collection.find_one({'username': username})
        if user and confirm_delete.lower() == 'y':
            users_collection.delete_one({'username': username})
            print(Fore.GREEN + f"\nUser '{username}' deleted successfully!" + Style.RESET_ALL)
        elif user and confirm_delete.lower() == 'n':
            print(Fore.RED + "User has not been deleted!" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"\nUser '{username}' not found." + Style.RESET_ALL)

        time.sleep(2)

