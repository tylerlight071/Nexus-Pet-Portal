import getpass
import time
from colorama import Fore, Style
from common_functions import clear_screen, load_data, save_data

USER_DATA_FILE = "users.json"

def register():
    clear_screen()
    users = load_data(USER_DATA_FILE)
    username = input("\nEnter a username: ")
    if username in users:
        print(Fore.RED + "\nUsername already exists. Please choose another one." + Style.RESET_ALL)
        time.sleep(2)
        return

    while True:
        password = getpass.getpass("Enter a password: ")
        confirm_password = getpass.getpass("Confirm your password: ")
        if password == confirm_password:
            users[username] = password
            save_data(users, USER_DATA_FILE)
            print(Fore.GREEN + "\nRegistration successful!" + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
            break  # Exit the loop when registration is successful
        else:
            print(Fore.RED + "\nPasswords do not match. Please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    register()
