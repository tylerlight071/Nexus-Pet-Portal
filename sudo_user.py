import getpass
import json
import time
from colorama import Fore, Style
from common_functions import clear_screen, log_action

USER_DATA_FILE = "users.json"

def sudo_user():
    # Continuous loop for sudo user authentication 
    while True:
        print("\nPlease enter your credentials")
        username = input("\nEnter your username: ")
        password = getpass.getpass("Enter your password: ")

        # Check user credentials from the user data file
        with open(USER_DATA_FILE, 'r') as user_file:
            users = json.load(user_file)

            if username in users:
                if users[username]['password'] == password:
                    user_level = users[username]['level']
                    # Throw error if user is logging in with ADMIN account
                    if username == "ADMIN":
                        print("\nNot a valid username")
                        clear_screen()
                        sudo_user()
                        return username
                    
                    # Notify about user verification for high level users
                    elif user_level >= 2:        
                            print(Fore.GREEN +"\nUser Verified..." + Style.RESET_ALL)
                            time.sleep(2)
                            return username,user_level

                    # Notify insufficent clearance
                    else:
                        print(Fore.RED + "\nYou do not have clearance to do this." + Style.RESET_ALL)
                        time.sleep(1)
                        print(Fore.RED + "\nADMIN user will be alerted." + Style.RESET_ALL)
                        time.sleep(1)
                        print(Fore.RED + "\nExiting..." + Style.RESET_ALL)
                        time.sleep(1)

                        # Log user's username and add it to audit log
                        current_user = username
                        log_action(current_user, f"Tried to access without clearance")
                        exit()
                
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
