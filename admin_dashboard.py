import time
from colorama import Fore, Style
from common_functions import clear_screen, log_action
from user_management import user_management

def admin_dashboard():
    # Continuous loop for admin dashboard
    while True:
        clear_screen()
        print(Fore.YELLOW + "\nADMIN Dashboard" + Style.RESET_ALL)
        print("\n1. User Management")
        print("2. Audit Logs")
        print("3. Manage settings")
        print("4. Logout")
        
        option = input("\nPlease select an option: ")

        # Check user input and perform corresponding action
        if option == '1':
            user_management()
        elif option == '2':
            print("\nThis feature is under development.")
        elif option == '3':
            # ! Implement settings management
            print("\nThis feature is under development.")
            time.sleep(2)
        elif option == '4':
            print("\nLogging out...")
            log_action("ADMIN", "Logged Out")
            time.sleep(2)
            exit()
        else:
            print(Fore.RED + "\nInvalid option. Please try again." + Style.RESET_ALL)
            time.sleep(2)