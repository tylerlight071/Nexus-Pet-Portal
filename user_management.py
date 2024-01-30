import time
from colorama import Fore, Style
from common_functions import clear_screen, load_data, save_data

USER_DATA_FILE = "users.json"

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
            change_user_password()
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

def change_user_password():
    # Load user data and prompt for username and new password
    users = load_data(USER_DATA_FILE)
    username = input("\nEnter the username to change the password: ")

    # Change password if the user exist and is not ADMIN
    if username in users and username != "ADMIN": 
        new_password = input("Enter the new password (use password to set their own): ")
        users[username]['password'] = new_password
        save_data(users, USER_DATA_FILE)
        print(Fore.GREEN + f"\nPassword for user '{username}' changed successfully!" + Style.RESET_ALL)
    elif username == "ADMIN":  
        print(Fore.RED + "\nYou cannot change the password for the ADMIN user." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"\nUser '{username}' not found." + Style.RESET_ALL)

    time.sleep(2)

def update_user_information():
    # Load user data and prompt for username and updates
    users = load_data(USER_DATA_FILE)
    clear_screen()
    username = input("\nEnter the username to update information: ")

    if username in users and username != "ADMIN":  
        clear_screen()
        print("\nCurrent user information:")
        print(f"\nUsername: {username}")
        print(f"User Level: {users[username]['level']}")
        
        # Prompt for the information to be updated
        print("\nSelect the information you want to update:")
        print("\n1. Username")
        print("2. User Level")
        print("3. Cancel")
        
        option = input("\nEnter your choice: ")
        
        # Process user's choice and perform updates accordingly
        if option == '1':
            new_username = input("Enter the new username: ")
            if new_username not in users:  
                users[new_username] = users.pop(username)
                print(Fore.GREEN + f"\nUsername updated successfully to '{new_username}'!" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"\nUsername '{new_username}' already exists. Please choose a different username." + Style.RESET_ALL)
        elif option == '2':
            new_level = int(input("Enter the new user level: "))
            users[username]['level'] = new_level
            print(Fore.GREEN + f"\nUser level updated successfully for '{username}'!" + Style.RESET_ALL)
        elif option == '3':
            print("\nOperation canceled.")
        else:
            print(Fore.RED + "\nInvalid option. Please try again." + Style.RESET_ALL)
    elif username == "ADMIN": 
        print(Fore.RED + "\nYou cannot update information for the ADMIN user." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"\nUser '{username}' not found." + Style.RESET_ALL)

    save_data(users, USER_DATA_FILE)
    time.sleep(2)

def delete_user():
    # Load user data and prompt for username to be deleted
    users = load_data(USER_DATA_FILE)
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
        if username in users and confirm_delete.lower() == 'y':
            del users[username]
            save_data(users, USER_DATA_FILE)
            print(Fore.GREEN + f"\nUser '{username}' deleted successfully!" + Style.RESET_ALL)
        elif username in users and confirm_delete.lower() == 'n':
            print(Fore.RED + "User has not been deleted!" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"\nUser '{username}' not found." + Style.RESET_ALL)

        time.sleep(2)

