import time
from colorama import Fore, Style
from common_functions import clear_screen, load_data

ANIMAL_DATA_FILE = "animals.json"

def print_animal_table(animals):
    """Prints the table of animals."""
    print("\n🐾 " + Fore.CYAN + "List of Animals" + Style.RESET_ALL + " 🐾")
    print("--------------------------------------------------------------------------------------------")
    print("| " + Fore.YELLOW + "Name".ljust(20) + Style.RESET_ALL + "| " + Fore.YELLOW + "Species".ljust(20) + Style.RESET_ALL + "| " + Fore.YELLOW + "Breed".ljust(25) + Style.RESET_ALL + "| " + Fore.YELLOW + "Age".ljust(6) + Style.RESET_ALL + " | " + Fore.YELLOW + "Adopted".ljust(8) + Style.RESET_ALL + " |")
    print("--------------------------------------------------------------------------------------------")

    for name, data in animals.items():
        name_column = f"| {name.ljust(20)}"
        species_column = f"| {data['species'].ljust(20)}"
        breed_column = f"| {data['breed'].ljust(25)}"
        age_column = f"| {str(data['age']).ljust(6)}"
        adopted_column = f"| {str(data['adopted']).ljust(10)}|"
        print(name_column + species_column + breed_column + age_column + adopted_column)

    print("--------------------------------------------------------------------------------------------")

def search_animals(animals):
    """Allows user to search for animals."""
    search_query = input("Enter (name/species/breed/age): ").lower()
    found_results = False

    for name, data in animals.items():
        if search_query in name.lower() or \
           search_query in data['species'].lower() or \
           search_query in data['breed'].lower() or \
           search_query == str(data['age']):
            found_results = True
            print_animal_table({name: data})
            print("")
            print("1. " + Fore.GREEN + "Search for animal" + Style.RESET_ALL)
            print("2. " + Fore.GREEN + "View animal profile" + Style.RESET_ALL)
            print("3. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
            exit_input = input("Please select an option: ")

            if exit_input == '1':
                clear_screen()
                search_animals(animals)
            elif exit_input == '2':
                print("This feature is coming soon!")
                time.sleep(2)
                clear_screen()
                print_animal_table(animals)
            elif exit_input == '3':
                clear_screen()
                return
            else:
                print("Invalid input. Please choose one of the options.")

    if not found_results:
        print("No animals found matching the search criteria")
        time.sleep(2)
        clear_screen()

def view_animals():
    """Main function to view animals."""
    clear_screen()
    animals = load_data(ANIMAL_DATA_FILE)
    print_animal_table(animals)

    while True:
        print("")
        print("1. " + Fore.GREEN + "Search for animal" + Style.RESET_ALL)
        print("2. " + Fore.GREEN + "View animal profile" + Style.RESET_ALL)
        print("3. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
        user_input = input("Please select an option: ")

        if user_input == '1':
            clear_screen()
            search_animals(animals)
        elif user_input == '2':
            print("This feature is coming soon!")
            time.sleep(2)
            clear_screen()
            print_animal_table(animals)
        elif user_input == '3':
            clear_screen()
            return
        else:
            print("Invalid input. Please choose one of the options.")

if __name__ == "__main__":
    view_animals()
