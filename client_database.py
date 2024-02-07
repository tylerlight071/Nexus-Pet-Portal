import time
from colorama import Fore, Style
from common_functions import clear_screen
from customer_adoption_form import view_available_animals

def modify_clint_database():
    clear_screen()

    print(Fore.CYAN + "\n📝 Modify Database 📝" + Style.RESET_ALL)
    print("\n1. " + Fore.GREEN + "Add Client" + Style.RESET_ALL)
    print("2. " + Fore.GREEN + "Modify Client" + Style.RESET_ALL)
    print("3. " + Fore.GREEN + "Remove Client" + Style.RESET_ALL)
    print("4. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)

    choice = input("\nPlease select an option: ")

    if choice == '1':
        print(Fore.GREEN + "\nOpening Customer Adoption Form..." + Style.RESET_ALL)
        time.sleep(1)
        clear_screen()
        view_available_animals()
    
    elif choice == '2':
        print("\nThis feature is coming soon.")
        time.sleep(2)
        clear_screen()
    
    elif choice == '3':
        print("\nThis feature is coming soon.")
        time.sleep(2)
        clear_screen()

    elif choice == '4':
        print("\nExiting Modify Database...")
        time.sleep(1)
        clear_screen()
        return
    
    else:
        print(Fore.RED + "Invalid input. Please try again." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        modify_clint_database()

def client_database():
    print(Fore.CYAN + "\n🧑 Client Database 🧑" + Style.RESET_ALL)
    print("\n1. " + Fore.GREEN + "🔍 Search" + Style.RESET_ALL)
    print("2. " + Fore.GREEN + "📝 Modify Database" + Style.RESET_ALL)
    print("3. " + Fore.GREEN + "📁 Export Database" + Style.RESET_ALL)
    print("4. " + Fore.YELLOW + "🔐 Exit" + Style.RESET_ALL)
    choice = input("\nPlease select an option: ")

    if choice == '1':
        print("This feature is coming soon.")
        time.sleep(2)
        clear_screen()
    
    elif choice == '2':
        time.sleep(1)
        clear_screen()
        modify_clint_database()
    
    elif choice == '3':
        print("This feature is coming soon.")
        time.sleep(2)
        clear_screen()
    
    elif choice == '4':
        print("Exiting Client Database...")
        time.sleep(1)
        clear_screen()
        return

    else:
        print(Fore.RED + "\nInvalid input. Please try again." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        client_database()
    