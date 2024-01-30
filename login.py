import json
import getpass
import time
from colorama import Fore, Style
from common_functions import clear_screen
from admin_dashboard import admin_dashboard

USER_DATA_FILE = "users.json"

def change_admin_password():
    clear_screen()

    # Notify the user about changing the ADMIN password
    print(Fore.YELLOW + "\nYour password must be changed from the default 'ADMIN' for security reasons." + Style.RESET_ALL)

    # Prompt user for a new password and confirmation
    new_password = getpass.getpass("\nEnter a new password for ADMIN: ")
    confirm_password = getpass.getpass("Confirm the new password: ")

    # Check if passowrds match
    if new_password == confirm_password:
        #Update the password in the user data file
        with open(USER_DATA_FILE, 'r+') as user_file:
            data = json.load(user_file)
            data["ADMIN"] = {
                "password": new_password,
                "level": 5
            }
            user_file.seek(0)
            json.dump(data, user_file, indent=4)
            user_file.truncate()
            print(Fore.GREEN + "\nPassword changed successfully!" + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
    # Notify the user about mismatching passwords and prompt again
    else:
        print(Fore.RED + "\nPasswords do not match. Please try again." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        change_admin_password()

def login():
    # Continuous loop for login
    while True:
        # Display login prompt
        print("\n👤 User Login 👤")
        username = input("\nEnter your username: ")
        password = getpass.getpass("Enter your password: ")

        # Check user credentials from the user data file
        with open(USER_DATA_FILE, 'r') as user_file:
            users = json.load(user_file)

            if username in users:
                if users[username]['password'] == password:
                    user_level = users[username]['level'] 
                    # Change admin password if not already done so
                    if username == "ADMIN" and password == "ADMIN":
                        change_admin_password()
                        admin_dashboard()
                        return username, user_level
                    
                    # Go straight to admin dashboard 
                    elif username == "ADMIN":
                        admin_dashboard()
                        return username, user_level
                    
                    # Log in as regular user 
                    else:
                        print("\nLogging in...")
                        time.sleep(2)
                        return username, user_level 
                    
                # Notify about incorrect password                    
                else:
                    print(Fore.RED + "\nIncorrect password. Please try again." + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()

            # Notify about non-existing username                    
            else:
                print(Fore.RED + "\nUsername not found. Please try again." + Style.RESET_ALL)
                time.sleep(2)
                clear_screen()
