import time
from colorama import Fore, Style
from common_functions import clear_screen, hash_password, get_mongodb_uri
from register import register
from pymongo import MongoClient
from sudo_user_login import SudoAdmin

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)
db = client['animal_rescue']
users_collection = db['users']


def user_management():
    # Continuous loop for user management options
    while True:
        clear_screen()
        print(Fore.YELLOW + "\nUser Management" + Style.RESET_ALL)
        print("\n1. Update user information")
        print("2. Register new user")
        print("3. Delete user")
        print("4. Back to ADMIN dashboard")
        option = input("\nPlease select an option: ")

        # Perform actions based on user input
        if option == '1':
            update_user_information()
        elif option == '2':
            register()
        elif option == '3':
            delete_user()
        elif option == '4':
            print("\nReturning to ADMIN dashboard...")
            time.sleep(2)
            return
        else:
            print(Fore.RED + "\nInvalid option. Please try again." + Style.RESET_ALL)
            time.sleep(2)

def reset_user_password(username):
    # Check if the user is ADMIN
    SudoAdmin(users_collection.database).login()

    # Change password if the user exists and is not ADMIN
    user = users_collection.find_one({'username': username})
    if user and username != "ADMIN": 
        new_password = "password"

        # Generate salt and hash password
        hashed_password = hash_password(new_password)
        
        # Update user's password and salt
        users_collection.update_one({'username': username}, 
                                    {'$set': {'hashed_password': hashed_password}})
        print(Fore.GREEN + f"\nPassword for user '{username}' reset successfully!" + Style.RESET_ALL)
    
    elif username == "ADMIN":  
        print(Fore.RED + "\nYou cannot change the password for the ADMIN user." + Style.RESET_ALL)
    
    else:
        print(Fore.RED + f"\nUser '{username}' not found." + Style.RESET_ALL)
    time.sleep(2)

def get_username():
    return input("\nEnter the username to update information: ")

def get_user(username):
    return users_collection.find_one({'username': username})

def print_user_info(username, user):
    clear_screen()  
    print(Fore.CYAN + "\nCurrent user information:" + Style.RESET_ALL)
    print(Fore.GREEN + f"\nUsername: {username}" + Style.RESET_ALL)
    print(Fore.GREEN + f"User Level: {user['level']}" + Style.RESET_ALL)

def get_option():
    print("\nSelect the information you want to update:")
    print("\n1. Username")
    print("2. User Level")
    print("3. Reset Password")
    print("4. Cancel")
    return input("\nEnter your choice: ")

def update_username(username):
    new_username = input("Enter the new username: ")
    if not users_collection.find_one({'username': new_username}):  
        users_collection.update_one({'username': username}, {'$set': {'username': new_username}})
        print(Fore.GREEN + f"\nUsername updated successfully to '{new_username}'!" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"\nUsername '{new_username}' already exists. Please choose a different username." + Style.RESET_ALL)

def update_user_level(username):
    new_level = input("Enter the new user level: ")
    if new_level.isdigit():  # Check if the input is a valid integer
        new_level = int(new_level)
        users_collection.update_one({'username': username}, {'$set': {'level': new_level}})
        print(Fore.GREEN + f"\nUser level updated successfully for '{username}'!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nInvalid user level. Please enter a valid level." + Style.RESET_ALL)

def update_user_information():
    username = get_username()
    user = get_user(username)

    if user and username != "ADMIN":
        print_user_info(username, user)
        option = get_option()
        
        if option == '1':
            update_username(username)
        elif option == '2':
            update_user_level(username)
        elif option == '3':
            time.sleep(2)
            reset_user_password(username)
        elif option == '4':
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