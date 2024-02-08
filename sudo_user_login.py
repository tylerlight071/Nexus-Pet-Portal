import time
import getpass
from common_functions import clear_screen, verify_password, log_action
from colorama import Fore, Style

user_verified = "\nUser Verified..."
enter_credentials = "\nPlease enter your credentials"

class SudoUser:
    MAX_ATTEMPTS = 2

    def __init__(self, db):
        self.db = db
        self.users_collection = db['users']

    def login(self):
        clear_screen()
        MAX_ATTEMPTS = 2 

        for attempts in range(MAX_ATTEMPTS):
            print(Fore.LIGHTMAGENTA_EX + "\n👤 Sudo Login 👤" + Style.RESET_ALL)
            print(enter_credentials)

            username, password = self.get_credentials()
            if username is None or password is None:
                continue

            user = self.attempt_login(username, password, attempts)
            if user:
                return user

        self.print_max_attempts_reached()

    def attempt_login(self, username, password, attempts):
        user = self.users_collection.find_one({'username': username})

        if user:
            stored_password = user['hashed_password']

            if verify_password(stored_password, password):
                user_level = user['level']
                    
                if username == "ADMIN":
                    print("\nNot a valid username")
                    clear_screen()
                    return None
                elif user_level >= 2:        
                    print(Fore.GREEN + user_verified + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    return username
                else:
                    self.print_insufficient_clearance(username)
                    exit()
            else:
                self.print_incorrect_password(username, attempts)
        else:
            self.print_username_not_found()

        return user

    def get_credentials(self):
        username = input("\nEnter your username: ")
        password = getpass.getpass("Enter your password: ")

        if not username or not password:
            print(Fore.RED + "\nUsername and password are required." + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
            return None, None

        return username, password
    
    def print_insufficient_clearance(self, username):
        print(Fore.RED + "\nYou do not have clearance to do this." + Style.RESET_ALL)
        time.sleep(1)
        print(Fore.RED + "\nADMIN user will be alerted." + Style.RESET_ALL)
        time.sleep(1)
        print(Fore.RED + "\nExiting..." + Style.RESET_ALL)
        time.sleep(1)
        log_action(username, "Tried to access without clearance")
    
    def print_incorrect_password(self, username, attempts):
        print(Fore.RED + "\nIncorrect password." + Style.RESET_ALL)
        time.sleep(2)
        print(Fore.RED + f"\nRemaining attempts: {self.MAX_ATTEMPTS - attempts}" + Style.RESET_ALL)
        log_action(username, "Failed attempted access via sudo")
        time.sleep(2)
        clear_screen()

    def print_username_not_found(self):
        print(Fore.RED + "\nUsername not found. Please try again." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()

    def print_max_attempts_reached(self):
        print(Fore.RED + "\nMaximum login attempts reached" + Style.RESET_ALL)
        time.sleep(1)
        print("\nExiting...")
        time.sleep(2)
        exit()


class SudoUserLevel1(SudoUser):
    def login(self):
        for attempts in range(self.MAX_ATTEMPTS):
            clear_screen()
            print(Fore.LIGHTMAGENTA_EX + "\n👤 Sudo Login 👤" + Style.RESET_ALL)
            print(enter_credentials)

            username, password = self.get_credentials()
            if username is None or password is None:
                continue

            user = self.attempt_login(username, password, attempts)
            if user:
                return user

        self.print_max_attempts_reached()

    def attempt_login(self, username, password, attempts):
        user = self.users_collection.find_one({'username': username})

        if user:
            stored_password = user['hashed_password']

            if verify_password(stored_password, password):
                user_level = user['level']
                    
                if username == "ADMIN":
                    print("\nNot a valid username")
                    clear_screen()
                    return username
                elif user_level >= 1:        
                    print(Fore.GREEN + user_verified + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    return user
                else:
                    self.print_insufficient_clearance(username)
                    exit()
            else:
                self.print_incorrect_password(username, attempts)
        else:
            self.print_username_not_found()

        return user

class SudoAdmin(SudoUser):
    def login(self):
        for attempts in range(self.MAX_ATTEMPTS):
            clear_screen()
            print(Fore.LIGHTMAGENTA_EX + "\n👤 ADMIN Sudo Login 👤" + Style.RESET_ALL)
            print(enter_credentials)

            username, password = self.get_credentials()
            if username is None or password is None:
                continue

            if self.attempt_login(username, password, attempts):
                return username,

        self.print_max_attempts_reached()

    def attempt_login(self, username, password, attempts):
        user = self.users_collection.find_one({'username': username})

        if user:
            stored_password = user['hashed_password']

            if verify_password(stored_password, password):             
                if username == "ADMIN":
                    print(Fore.GREEN + user_verified + Style.RESET_ALL)
                    time.sleep(2)
                    return True
                else:
                    self.print_insufficient_clearance(username)
                    exit()
            else:
                self.print_incorrect_password(username)
        else:
            self.print_username_not_found()

        return False