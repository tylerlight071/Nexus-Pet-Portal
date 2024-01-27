import time
from colorama import Fore, Style
from common_functions import clear_screen, load_data, save_data
from register import register

USER_DATA_FILE = "users.json"

def admin_dashboard():
    while True:
        clear_screen()
        print(Fore.YELLOW + "\nADMIN Dashboard" + Style.RESET_ALL)
        print("1. Register a new user")
        print("2. Manage settings")
        print("3. Logout")
        option = input("Please select an option: ")

        if option == '1':
            register()
        elif option == '2':
            # Implement settings management
            print("This feature is under development.")
            time.sleep(2)
        elif option == '3':
            print("Logging out...")
            exit()
        else:
            print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)
            time.sleep(2)
