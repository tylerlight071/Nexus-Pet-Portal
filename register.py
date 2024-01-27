import getpass
import time
from colorama import Fore, Style
from common_functions import clear_screen, load_data, save_data

USER_DATA_FILE = "users.json"

def register():
    clear_screen()
    users = load_data(USER_DATA_FILE)
    username = input("Enter a username: ")
    if username in users:
        print(Fore.RED + "Username already exists. Please choose another one." + Style.RESET_ALL)
        time.sleep(2)
        return register()
    password = getpass.getpass("Enter a password: ")
    users[username] = password
    save_data(users, USER_DATA_FILE)
    print(Fore.GREEN + "Registration successful!" + Style.RESET_ALL)
    time.sleep(2)
    clear_screen()