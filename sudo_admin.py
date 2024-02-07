import getpass
import time
from colorama import Fore, Style
from common_functions import clear_screen, log_action, verify_password, get_mongodb_uri
from pymongo import MongoClient

MAX_ATTEMPTS = 2

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)
db = client['animal_rescue']
users_collection = db['users']

def sudo_admin():
    clear_screen()

    attempts = 0 
    while attempts < MAX_ATTEMPTS:
        print(Fore.LIGHTMAGENTA_EX + "\n👤 ADMIN Sudo Login 👤" + Style.RESET_ALL)
        print("\nPlease enter your credentials")

        username, password = get_credentials()
        if username is None or password is None:
            continue

        user = users_collection.find_one({'username': username})

        if user:
            stored_password = user['hashed_password']

            if verify_password(stored_password, password):             
                if username == "ADMIN":
                    print(Fore.GREEN +"\nUser Verified..." + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    return username
                else:
                    print_insufficient_clearance(username)
                    exit()
            else:
                print_incorrect_password(username, attempts)
                attempts += 1
        else:
            print_username_not_found()
        
    print_max_attempts_reached()

def get_credentials():
    username = input("\nEnter your username: ")
    password = getpass.getpass("Enter your password: ")

    if not username or not password:
        print(Fore.RED + "\nUsername and password are required." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        return None, None

    return username, password

def print_insufficient_clearance(username):
    print(Fore.RED + "\nYou do not have clearance to do this." + Style.RESET_ALL)
    time.sleep(1)
    print(Fore.RED + "\nADMIN user will be alerted." + Style.RESET_ALL)
    time.sleep(1)
    print(Fore.RED + "\nExiting..." + Style.RESET_ALL)
    time.sleep(1)
    log_action(username, "Tried to access without clearance")

def print_incorrect_password(username, attempts):
    print(Fore.RED + "\nIncorrect password." + Style.RESET_ALL)
    time.sleep(2)
    print(Fore.RED + f"\nRemaining attempts: {MAX_ATTEMPTS - attempts}" + Style.RESET_ALL)
    log_action(username, "Failed attempted access via sudo")
    time.sleep(2)
    clear_screen()

def print_username_not_found():
    print(Fore.RED + "\nUsername not found. Please try again." + Style.RESET_ALL)
    time.sleep(2)
    clear_screen()

def print_max_attempts_reached():
    print(Fore.RED + "\nMaximum login attempts reached" + Style.RESET_ALL)
    time.sleep(1)
    print("\nExiting...")
    time.sleep(2)
    exit()