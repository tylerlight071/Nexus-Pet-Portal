import time
from colorama import Fore, Style
from common_functions import clear_screen, load_animal_data, log_action, get_mongodb_uri
from view_animal_profile import view_animals_full
from sudo_user_level_1 import sudo_user
from edit_animal_entries import modify_animal
from add_animal import add_animal
from pymongo import MongoClient

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)

db = client['animal_rescue']
animals_collection = db['animals']



# Function to print the table of animals
def print_animal_table(animals):
    # Print table header
    print("\n🐾 " + Fore.CYAN + "List of Animals" + Style.RESET_ALL + " 🐾")
    print("+-------------------------------------------------------------------------------------------+")
    print("| " + Fore.YELLOW + "Name".ljust(20) + Style.RESET_ALL + "| " + Fore.YELLOW + "Species".ljust(8) + Style.RESET_ALL + "| " + Fore.YELLOW + "Breed".ljust(25) + Style.RESET_ALL + "| " + Fore.YELLOW + "Gender".ljust(15) + Style.RESET_ALL + "| " + Fore.YELLOW + "Age".ljust(1) + Style.RESET_ALL + " | " + Fore.YELLOW + "Adopted".ljust(7) + Style.RESET_ALL + " |")
    print("+-------------------------------------------------------------------------------------------+")

    # Print each animal's data row by row
    for animal in animals:
        name_column = f"| {animal['name'].ljust(20)}"
        species_column = f"| {animal['species'].ljust(8)}"
        breed_column = f"| {animal['breed'].ljust(25)}"
        gender_column = f"| {animal['gender'].ljust(15)}"
        age_column = f"|  {str(animal['age']).ljust(3)}"
        adopted_column = f"| {str(animal['adopted']).ljust(7)} |"
        print(name_column + species_column + breed_column + gender_column + age_column + adopted_column)

    # Print table footer
    print("+-------------------------------------------------------------------------------------------+")

# Function to filter animals based on user input
def filter_animals(animals):
    
    # Initialize variables
    species_query = None
    breed_query = None
    gender_query = None
    adopted_query = None

    clear_filters = input(Fore.LIGHTYELLOW_EX + "\nClear filters? (Y/N): " + Style.RESET_ALL).lower()

    if clear_filters == 'y':
        # Clear filters
        clear_screen()
        print_animal_table(animals)
        return
    
    elif clear_filters == 'n':
        # Print filter options
        species_query = input(Fore.GREEN + "\nEnter species" + Style.RESET_ALL + " (leave blank to skip): ").lower()
        breed_query = input(Fore.GREEN + "\nEnter breed " + Style.RESET_ALL + "(leave blank to skip): ").lower()
        gender_query = input(Fore.GREEN + "\nEnter gender "+ Style.RESET_ALL + "(leave blank to skip): ").lower()
        adopted_query = input(Fore.GREEN + "\nEnter adoption status " + Style.RESET_ALL + "(True/False, leave blank to skip): ").lower()
        clear_screen()

    filtered_animals = []
    # Iterate through animals and apply filters
    for animal in animals:
        if (not species_query or any(species_query.lower() in animal['species'].lower() for species in species_query.split(','))) and \
           (not breed_query or any(breed_query.lower() in animal['breed'].lower() for breed in breed_query.split(','))) and \
           (not gender_query or any(gender_query.lower() in animal['gender'].lower() for gender in gender_query.split(','))) and \
           (not adopted_query or any(adopted_query.lower() in str(animal['adopted']).lower() for adopted in adopted_query.split(','))):
            filtered_animals.append(animal)

    if filtered_animals:
        clear_screen()
        print_animal_table(filtered_animals)
    else:
        print("No animals found matching the filter criteria")
        time.sleep(2)
        clear_screen()
        print_animal_table(animals)

# Function to search animals based on user input
def search_animals(animals, current_user):
   
    while True:
        clear_screen()
        print(Fore.LIGHTCYAN_EX + "\n🔎 SEARCH ANIMALS 🔍" + Style.RESET_ALL)
        print("\nEnter any of the following criteria to search:")
        print(Fore.GREEN + "\n - Name")
        print(" - Species")
        print(" - Breed")
        print(" - Gender (Male/Female)")
        print(" - Age" + Style.RESET_ALL)
        print("\nOr type 'exit' to return to the main menu.")

        search_query = input(Fore.LIGHTCYAN_EX + "\nSearch: " + Style.RESET_ALL).lower()

        if search_query == 'exit':
            clear_screen()
            print_animal_table(animals)
            return

        log_action(current_user, f"Searched for {search_query}")

        found_results = []

        if search_query.strip():
            for animal in animals:
                if (search_query in animal['name'].lower() or
                    search_query in animal['species'].lower() or
                    search_query in animal['breed'].lower() or
                    (search_query == 'male' and animal['gender'].lower() == 'male') or
                    (search_query == 'female' and animal['gender'].lower() == 'female') or
                    search_query == str(animal['age'])):
                    found_results.append(animal)

            if found_results:
                clear_screen()
                print(Fore.LIGHTYELLOW_EX + "SEARCH RESULTS" + Style.RESET_ALL)
                print_animal_table(found_results)
                print("\n1. " + Fore.GREEN + "Search for another animal" + Style.RESET_ALL)
                print("2. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
                exit_input = input("\nPlease select an option: ")

                if exit_input == '1':
                    continue
                elif exit_input == '2':
                    clear_screen()
                    print_animal_table(animals)
                    return
                else:
                    print(Fore.RED + "Invalid input. Please choose one of the options." + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    print_animal_table(animals)
            else:
                print(Fore.RED + "No animals found matching the search criteria" + Style.RESET_ALL)
                time.sleep(2)
                clear_screen()
                print_animal_table(animals)
        else:
            print(Fore.RED + "Invalid input. Please enter a search query or type 'exit'." + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()

# Function to sort animals based on user input
def sort_animals(animals, key='name', reverse=False):

    if key == 'name':
        sorted_animals = sorted(animals, key=lambda x: x['name'], reverse=reverse)
    elif key == 'age':
        sorted_animals = sorted(animals, key=lambda x: x['age'], reverse=reverse)
    else:
        print("Invalid key for sorting.")
        return animals
    
    return sorted_animals

def delete_animal(animal_name):

    try:
        # Check if there are multiple animals with the same name
        animal_count = animals_collection.count_documents({"name": animal_name})
        
        if animal_count == 0:
            print(f"{animal_name} not found in the database.")
            time.sleep(2)
            clear_screen()
            print_animal_table(load_animal_data(animals_collection))
            return False
        
        elif animal_count == 1:
            result = animals_collection.delete_one({"name": animal_name})
            if result.deleted_count == 1:
                print(Fore.GREEN + f"\nSuccessfully deleted {animal_name} from the database." + Style.RESET_ALL)
                time.sleep(2)
                clear_screen()
                print_animal_table(load_animal_data(animals_collection))
                return True
            else:
                print(f"Failed to delete {animal_name} from the database.")
                time.sleep(2)
                clear_screen()
                print_animal_table(load_animal_data(animals_collection))
                return False
        
        else:  # Multiple animals with the same name
            print(Fore.YELLOW + f"Multiple animals found with the name '{animal_name}'. Please select the index of the animal you want to delete:" + Style.RESET_ALL)
            
            # Find all animals with the same name and print their indices
            cursor = animals_collection.find({"name": animal_name})
            index = 1
            for animal in cursor:
                print(f"{index}. Name: {animal['name']}, Species: {animal['species']}, Breed: {animal['breed']}")
                index += 1
            
            # Prompt the user to select the index of the animal to delete
            selected_index = input("\nEnter the index of the animal to delete: ")
            try:
                selected_index = int(selected_index)
                if 1 <= selected_index <= animal_count:
                    cursor.rewind()  # Reset cursor to the beginning
                    selected_animal = cursor[selected_index - 1]
                    result = animals_collection.delete_one({"_id": selected_animal["_id"]})
                    if result.deleted_count == 1:
                        print(Fore.GREEN + f"\nSuccessfully deleted {selected_animal['name']} from the database." + Style.RESET_ALL)
                        time.sleep(2)
                        clear_screen()
                        return True
                    else:
                        print(f"Failed to delete {selected_animal['name']} from the database.")
                        time.sleep(2)
                        clear_screen()
                        return False
                else:
                    print(Fore.RED + "Invalid index. Please enter a valid index." + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    return False
            except ValueError:
                print(Fore.RED + "Invalid index. Please enter a valid index." + Style.RESET_ALL)
                time.sleep(2)
                clear_screen()
                return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False  

def modify_animal_database():

    animals = load_animal_data(animals_collection)

    print(Fore.CYAN + "\n🐶 Modify Animal Database 🐶" + Style.RESET_ALL)
    print("\n1. " + Fore.GREEN + "Add Animal" + Style.RESET_ALL)
    print("2. " + Fore.GREEN + "Update Animal Entry" + Style.RESET_ALL)
    print("3. " + Fore.GREEN + "Delete Animal" + Style.RESET_ALL)
    print("4. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)

    choice = input("\nPlease select an option: ")

    # Add Animal
    if choice == '1':
        time.sleep(2)
        add_animal()
    
    # Update Animal Entry
    elif choice == '2':
        time.sleep(2)
        modify_animal()
    
    # Delete Animal
    elif choice == '3':
        current_user = sudo_user()
        
        clear_screen()
        print_animal_table(animals)
        animal_name = input("\nEnter the name of the animal to delete: ")
        if delete_animal(animal_name):
            log_action(current_user, f"Deleted {animal_name} from the database")
            return 
        
        else:
            log_action(current_user, f"Failed to delete {animal_name} from the database")
            return

    # Exit   
    elif choice == '4':
        print("\nExiting Modify Database...")
        time.sleep(1)
        clear_screen()
        return
    
    else:
        print(Fore.RED + "\nInvalid input. Please choose one of the options." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        print_animal_table(animals)

    

# Function to view animals and interact with options
def view_animals():
    
    animals = load_animal_data(animals_collection)

    current_user = sudo_user()

    # Load animal data
    print_animal_table(animals)

    while True:
        print(Fore.CYAN + "\n⚙️ Options ⚙️" + Style.RESET_ALL)
        print("\n1. " + Fore.GREEN + "Search for animal" + Style.RESET_ALL)
        print("2. " + Fore.GREEN + "Sort/Filter Animals" + Style.RESET_ALL)
        
        
        if current_user['level'] >= 2:
            print("3. " + Fore.GREEN + "View animal profile" + Style.RESET_ALL)
            print("4. " + Fore.GREEN + "Modify Database" + Style.RESET_ALL)
            print("5. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
        else:
            print("3. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)

        user_input = input("\nPlease select an option: ")

        # Search Database
        if user_input == '1':
            time.sleep(1)
            clear_screen()
            search_animals(animals, current_user)
        
        # Sort Database
        elif user_input == '2':
            sort_filter_option = input("\nSort or filter? (S/F): ").lower()
            if sort_filter_option == 's':
                clear_screen()
                print_animal_table(animals)
                print("\nSort by:")
                print("1." + Fore.GREEN + " Name (A-Z)" + Style.RESET_ALL)
                print("2." + Fore.GREEN + " Name (Z-A)" + Style.RESET_ALL)
                print("3." + Fore.GREEN + " Age (Youngest to Oldest)" + Style.RESET_ALL)
                print("4." + Fore.GREEN + " Age (Oldest to Youngest)" + Style.RESET_ALL)
                sort_option = input("\nPlease select an option: ")

                # Sort animals based on user input
                if sort_option in ['1', '2', '3', '4']:
                    sort_key = 'name' if sort_option in ['1', '2'] else 'age'
                    reverse_sort = True if sort_option in ['2', '4'] else False
                    animals = sort_animals(animals, key=sort_key, reverse=reverse_sort)
                    clear_screen()
                    print_animal_table(animals)

                 # Invalid option
                else:
                    print(Fore.RED + "\nInvalid input. Please choose one of the options." + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    print_animal_table(animals)

            # Filter Database
            elif sort_filter_option == 'f':
                filter_animals(animals)

            # Invalid option
            else:
                print(Fore.RED + "\nInvalid input. Please choose one of the options." + Style.RESET_ALL)
                time.sleep(2)
                clear_screen()
                print_animal_table(animals)

        # View Animal Profile
        elif user_input == '3':
            if current_user['level'] >= 2:
                view_animals_full()
            else:
                log_action(current_user, "Exited 'View Animal Database'")
                print("\nExiting...")
                time.sleep(2)
                clear_screen()
                return

        elif user_input == '4':
            if current_user['level'] >= 2:
                log_action(current_user, "Entered 'Modify Animal Database'")
                time.sleep(2)
                clear_screen()
                modify_animal_database()
            
        # Exit Database 
        elif user_input == '5' and current_user['level'] >= 2:
            log_action(current_user, "Exited 'View Animal Database'")
            print("\nExiting...")
            time.sleep(2)
            clear_screen()
            return
        else:
            print(Fore.RED + "\nInvalid input. Please choose one of the options." + Style.RESET_ALL)
            time.sleep(2)
            clear_screen()
            print_animal_table(animals)

if __name__ == "__main__":
    view_animals()