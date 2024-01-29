import time
from colorama import Fore, Style
from common_functions import clear_screen, load_data
from view_animal_profile import view_animal_profile

ANIMAL_DATA_FILE = "animals.json"

def print_animal_table(animals):
    """Prints the table of animals."""
    print("\n🐾 " + Fore.CYAN + "List of Animals" + Style.RESET_ALL + " 🐾")
    print("---------------------------------------------------------------------------------------------")
    print("| " + Fore.YELLOW + "Name".ljust(20) + Style.RESET_ALL + "| " + Fore.YELLOW + "Species".ljust(8) + Style.RESET_ALL + "| " + Fore.YELLOW + "Breed".ljust(25) + Style.RESET_ALL + "| " + Fore.YELLOW + "Gender".ljust(15) + Style.RESET_ALL + "| " + Fore.YELLOW + "Age".ljust(1) + Style.RESET_ALL + " | " + Fore.YELLOW + "Adopted".ljust(7) + Style.RESET_ALL + " |")
    print("---------------------------------------------------------------------------------------------")

    for name, data in animals.items():
        name_column = f"| {name.ljust(20)}"
        species_column = f"| {data['species'].ljust(8)}"
        breed_column = f"| {data['breed'].ljust(25)}"
        gender_column = f"| {data['gender'].ljust(15)}"
        age_column = f"|  {str(data['age']).ljust(3)}"
        adopted_column = f"| {str(data['adopted']).ljust(7)} |"
        print(name_column + species_column + breed_column + gender_column + age_column + adopted_column)

    print("---------------------------------------------------------------------------------------------")

def filter_animals(animals):
    """Filters animals based on species, breed and adoption status."""
    species_query = input(Fore.GREEN + "\nEnter species" + Style.RESET_ALL + " (leave blank to skip): ").lower()
    breed_query = input(Fore.GREEN + "Enter breed " + Style.RESET_ALL + "(leave blank to skip): ").lower()
    adopted_query = input(Fore.GREEN + "Enter adoption status " + Style.RESET_ALL + "(True/False, leave blank to skip): ").lower()
    clear_screen()

    filtered_animals = {}
    for name, data in animals.items():
        if (not species_query or species_query == data['species'].lower()) and \
           (not breed_query or breed_query == data['breed'].lower()) and \
           (not adopted_query or adopted_query == str(data['adopted']).lower()):
            filtered_animals[name] = data

    if filtered_animals:
        clear_screen()
        print_animal_table(filtered_animals)
    else:
        print("No animals found matching the filter criteria")
        time.sleep(2)
        clear_screen()
        print_animal_table(animals)

def search_animals(animals):
    """Allows user to search for animals."""
    while True:
        search_query = input("\nEnter (name/species/breed/age): ").lower()
        found_results = False

        if search_query.strip():  # Check if the query is not empty
            for name, data in animals.items():
                if search_query in name.lower() or \
                   search_query in data['species'].lower() or \
                   search_query in data['breed'].lower() or \
                   search_query == str(data['age']):
                    found_results = True
                    clear_screen()
                    print_animal_table({name: data})
                    print("\n1. " + Fore.GREEN + "Search for animal" + Style.RESET_ALL)
                    print("2. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
                    exit_input = input("\nPlease select an option: ")

                    if exit_input == '1':
                        clear_screen()
                        continue  # Go back to the search menu
                    elif exit_input == '2':
                        clear_screen()
                        print_animal_table(animals)
                        return
                    else:
                        print(Fore.RED + "Invalid input. Please choose one of the options." + Style.RESET_ALL)
                        time.sleep(2)
                        clear_screen()
                        print_animal_table(animals)
            if not found_results:
                print(Fore.RED + "No animals found matching the search criteria" + Style.RESET_ALL)
                time.sleep(2)
                clear_screen()
                print_animal_table(animals)
        else:
            print(Fore.RED + "Invalid input. Please choose one of the options." + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()


def sort_animals(animals, key='name', reverse=False):
    """Sorts the animals based on the specified key."""
    if key == 'name':
        sorted_animals = sorted(animals.items(), key=lambda x: x[0], reverse=reverse)
    elif key == 'age':
        sorted_animals = sorted(animals.items(), key=lambda x: int(x[1]['age']), reverse=reverse)
    else:
        print("Invalid key for sorting.")
        return

    return dict(sorted_animals)

def view_animals():
    """Main function to view animals."""
    clear_screen()
    animals = load_data(ANIMAL_DATA_FILE)
    print_animal_table(animals)

    while True:
        print(Fore.CYAN + "\n⚙️ Options ⚙️" + Style.RESET_ALL)
        print("\n1. " + Fore.GREEN + "Search for animal" + Style.RESET_ALL)
        print("2. " + Fore.GREEN + "Sort animals" + Style.RESET_ALL)
        print("3. " + Fore.GREEN + "Filter animals" + Style.RESET_ALL)
        print("4. " + Fore.GREEN + "View animal profile" + Style.RESET_ALL)
        print("5. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
        
        user_input = input("\nPlease select an option: ")

        if user_input == '1':
            clear_screen()
            search_animals(animals)
        elif user_input == '2':
            print("\nSort by:")
            print("1." + Fore.GREEN + " Name (A-Z)" + Style.RESET_ALL)
            print("2." + Fore.GREEN + " Name (Z-A)" + Style.RESET_ALL)
            print("3." + Fore.GREEN + " Age (Youngest to Oldest)" + Style.RESET_ALL)
            sort_option = input("\nPlease select an option: ")
            if sort_option in ['1', '2', '3']:
                sort_key = 'name' if sort_option in ['1', '2'] else 'age'
                reverse_sort = True if sort_option == '2' else False
                animals = sort_animals(animals, key=sort_key, reverse=reverse_sort)
                clear_screen()
                print_animal_table(animals)
            else:
                print("\nInvalid option.")
                clear_screen()
                print_animal_table(animals)
        elif user_input == '3':
            filter_animals(animals)
        elif user_input == '4':
            view_animal_profile()
        elif user_input == '5':
            clear_screen()
            return
        else:
            print("\nInvalid input. Please choose one of the options.")
            clear_screen()
            print_animal_table(animals)

if __name__ == "__main__":
    view_animals()