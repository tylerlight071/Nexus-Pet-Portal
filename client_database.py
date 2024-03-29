import time
from sudo_user_login import SudoUser
from colorama import Fore, Style
from common_functions import clear_screen, get_mongodb_uri
from customer_adoption_form_dog import adopt_dog_form
from pymongo import MongoClient

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)

db = client['animal_rescue']
animals_collection = db['animals']
users_collection = db['users']

new_feature_message = "\nThis feature is coming soon."

def modify_clint_database():
    clear_screen()

    print(Fore.CYAN + "\n📝 Modify Database 📝" + Style.RESET_ALL)
    print("\n1. " + Fore.GREEN + "Add Client" + Style.RESET_ALL)
    print("2. " + Fore.GREEN + "Modify Client" + Style.RESET_ALL)
    print("3. " + Fore.GREEN + "Remove Client" + Style.RESET_ALL)
    print("4. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)

    choice = input("\nPlease select an option: ")

    if choice == '1':
        adoption_form = input("\nOpen adoption form for dogs or cats? ")
        if adoption_form not in ['dogs', 'cats']:
            print(Fore.RED + "\nInvalid input. Please try again." + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
            modify_clint_database()

        if adoption_form == 'dogs':
            print("\n Opening dog adoption form...")
            time.sleep(2)
            clear_screen()
            adopt_dog_form()
        
        elif adoption_form == 'cats':
            print(new_feature_message)
            time.sleep(2)
            clear_screen()
    
    elif choice == '2':
        print("\nThis feature is coming soon.")
        time.sleep(2)
        clear_screen()
    
    elif choice == '3':
        print(new_feature_message)
        time.sleep(2)
        clear_screen()

    elif choice == '4':
        print("\nExiting Modify Database...")
        time.sleep(1)
        clear_screen()

    
    else:
        print(Fore.RED + "Invalid input. Please try again." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        modify_clint_database()

def client_database():
    
    clear_screen()

    SudoUser(users_collection.database).login()

    print(Fore.CYAN + "\n🧑 Client Database 🧑" + Style.RESET_ALL)
    print("\n1. " + Fore.GREEN + "🔍 Search" + Style.RESET_ALL)
    print("2. " + Fore.GREEN + "📝 Modify Database" + Style.RESET_ALL)
    print("3. " + Fore.GREEN + "📁 Export Database" + Style.RESET_ALL)
    print("4. " + Fore.YELLOW + "🔐 Exit" + Style.RESET_ALL)
    choice = input("\nPlease select an option: ")

    if choice == '1':
        print(new_feature_message)
        time.sleep(2)
        clear_screen()
    
    elif choice == '2':
        time.sleep(1)
        clear_screen()
        modify_clint_database()
    
    elif choice == '3':
        print(new_feature_message)
        time.sleep(1)
        clear_screen()
    
    elif choice == '4':
        print("Exiting Client Database...")
        time.sleep(1)
        clear_screen()

    else:
        print(Fore.RED + "\nInvalid input. Please try again." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        client_database()
    