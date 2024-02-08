import time
from colorama import Fore, Style
from common_functions import clear_screen, load_animal_data, log_action, get_mongodb_uri, sanitize_input
from view_animal_profile import view_animals_full
from sudo_user_login import SudoUserLevel1, SudoUser
from edit_animal_entries import modify_animal
from add_animal import add_animal
from tables import print_animal_table
from pymongo import MongoClient

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)

db = client['animal_rescue']
animals_collection = db['animals']
users_collection = db['users']

select_option = "\nPlease select an option: "
invalid_input = "\nInvalid input! Please enter a valid index."

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
        if (not species_query or any(species_query.lower() in animal['species'].lower() for species_query in species_query.split(','))) and \
           (not breed_query or any(breed_query.lower() in animal['breed'].lower() for breed_query in breed_query.split(','))) and \
           (not gender_query or gender_query.lower() == animal['gender'].lower()) and \
           (not adopted_query or any(adopted_query.lower() in str(animal['adopted']).lower() for adopted_query in adopted_query.split(','))):
            filtered_animals.append(animal)

    if filtered_animals:
        clear_screen()
        print_animal_table(filtered_animals)
    else:
        print("No animals found matching the filter criteria")
        time.sleep(2)
        clear_screen()
        print_animal_table(animals)

def search_animals(animals, current_user):
    while True:
        print_search_prompt()
        search_query = get_search_query()

        if search_query == 'exit':
            clear_screen_and_print_animals(animals)
            return

        log_action(current_user, f"Searched for {search_query}")

        found_results = search_animals_by_query(animals, search_query)

        if found_results:
            handle_found_results(animals, found_results)
        else:
            handle_no_results(animals)

def print_search_prompt():
    clear_screen()
    print(Fore.LIGHTCYAN_EX + "\n🔎 SEARCH ANIMALS 🔍" + Style.RESET_ALL)
    print("\nEnter any of the following criteria to search:")
    print(Fore.GREEN + "\n - Name")
    print(" - Species")
    print(" - Breed")
    print(" - Gender (Male/Female)")
    print(" - Age" + Style.RESET_ALL)
    print("\nOr type 'exit' to return to the main menu.")

def get_search_query():
    return input(Fore.LIGHTCYAN_EX + "\nSearch: " + Style.RESET_ALL).lower()

def search_animals_by_query(animals, search_query):
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
    return found_results

def handle_found_results(animals, found_results):
    clear_screen()
    print(Fore.LIGHTYELLOW_EX + "SEARCH RESULTS" + Style.RESET_ALL)
    print_animal_table(found_results)
    print("\n1. " + Fore.GREEN + "Search for another animal" + Style.RESET_ALL)
    print("2. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
    exit_input = input(select_option)

    if exit_input == '1':
        return
    elif exit_input == '2':
        clear_screen_and_print_animals(animals)
    else:
        print_invalid_input(animals)

def handle_no_results(animals):
    print(Fore.RED + "No animals found matching the search criteria" + Style.RESET_ALL)
    time.sleep(2)
    clear_screen_and_print_animals(animals)

def print_invalid_input(animals):
    print(Fore.RED + invalid_input + Style.RESET_ALL)
    time.sleep(2)
    clear_screen_and_print_animals(animals)

def clear_screen_and_print_animals(animals):
    clear_screen()
    print_animal_table(animals)

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

    animal_name = sanitize_input(animal_name)

    try:
        animal_count = animals_collection.count_documents({"name": animal_name})

        if animal_count == 0:
            handle_no_animal_found(animal_name)
        elif animal_count == 1:
            delete_single_animal(animal_name)
        else:
            delete_multiple_animals(animal_name, animal_count)

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def handle_no_animal_found(animal_name):
    print(f"{animal_name} not found in the database.")
    time.sleep(2)
    clear_screen_and_print_animals()
    return False

def delete_single_animal(animal_name):
    result = animals_collection.delete_one({"name": animal_name})
    if result.deleted_count == 1:
        print(Fore.GREEN + f"\nSuccessfully deleted {animal_name} from the database." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen_and_print_animals()
        return True
    else:
        print(f"Failed to delete {animal_name} from the database.")
        time.sleep(2)
        clear_screen_and_print_animals()
        return False

def delete_multiple_animals(animal_name, animal_count):
    print(Fore.YELLOW + f"Multiple animals found with the name '{animal_name}'. Please select the index of the animal you want to delete:" + Style.RESET_ALL)
    cursor = animals_collection.find({"name": animal_name})
    print_animals_with_indices(cursor)
    selected_index = get_selected_index()

    if 1 <= selected_index <= animal_count:
        delete_selected_animal(cursor, selected_index)
    else:
        print_invalid_index()

def print_animals_with_indices(cursor):
    index = 1
    for animal in cursor:
        print(f"{index}. Name: {animal['name']}, Species: {animal['species']}, Breed: {animal['breed']}")
        index += 1

def get_selected_index():
    selected_index = input("\nEnter the index of the animal to delete: ")
    try:
        return int(selected_index)
    except ValueError:
        print_invalid_index()

def delete_selected_animal(cursor, selected_index):
    cursor.rewind()  # Reset cursor to the beginning
    selected_animal = cursor[selected_index - 1]
    result = animals_collection.delete_one({"_id": selected_animal["_id"]})
    if result.deleted_count == 1:
        print(Fore.GREEN + f"\nSuccessfully deleted {selected_animal['name']} from the database." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        return True
    else:
        print("Failed to delete from the database.")
        time.sleep(2)
        clear_screen()
        return False

def print_invalid_index():
    print(Fore.RED + "Invalid index. Please enter a valid index." + Style.RESET_ALL)
    time.sleep(2)
    clear_screen()
    return False

def clear_screen_and_print_animals():
    clear_screen()
    print_animal_table(load_animal_data(animals_collection))

def modify_animal_database():

    animals = load_animal_data(animals_collection)

    print(Fore.CYAN + "\n🐶 Modify Animal Database 🐶" + Style.RESET_ALL)
    print("\n1. " + Fore.GREEN + "Add Animal" + Style.RESET_ALL)
    print("2. " + Fore.GREEN + "Update Animal Entry" + Style.RESET_ALL)
    print("3. " + Fore.GREEN + "Delete Animal" + Style.RESET_ALL)
    print("4. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)

    choice = input(select_option)

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
        current_user = SudoUser(users_collection.database).login()
        
        clear_screen()
        print_animal_table(animals)
        animal_name = input("\nEnter the name of the animal to delete: ")
        if delete_animal(animal_name):
            log_action(current_user, f"Deleted {animal_name} from the database")
 
        
        else:
            log_action(current_user, f"Failed to delete {animal_name} from the database")

    # Exit   
    elif choice == '4':
        print("\nExiting Modify Database...")
        time.sleep(1)
        clear_screen()
    
    else:
        print(Fore.RED + invalid_input + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()
        print_animal_table(animals)   

# Function to view animals and interact with options
def view_animals():
    animals = load_animal_data(animals_collection)
    current_user = SudoUserLevel1(users_collection.database).login()

    # Load animal data
    print_animal_table(animals)

    while True:
        print_options(current_user)
        user_input = input(select_option)

        if user_input == '1':
            search_database(animals, current_user)
        elif user_input == '2':
            sort_or_filter_database(animals)
        elif user_input == '3':
            view_animal_profile_or_exit(current_user)
        elif user_input == '4' and current_user['level'] >= 2:
            modify_database(current_user)
        elif user_input == '5' and current_user['level'] >= 2:
            if exit_database(current_user):
                break
        else:
            handle_invalid_input(animals)

# Print options for the user
def print_options(current_user):
    print(Fore.CYAN + "\n⚙️ Options ⚙️" + Style.RESET_ALL)
    print("\n1. " + Fore.GREEN + "Search for animal" + Style.RESET_ALL)
    print("2. " + Fore.GREEN + "Sort/Filter Animals" + Style.RESET_ALL)

    if current_user['level'] >= 2:
        print("3. " + Fore.GREEN + "View animal profile" + Style.RESET_ALL)
        print("4. " + Fore.GREEN + "Modify Database" + Style.RESET_ALL)
        print("5. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
    else:
        print("3. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)

# Search the database
def search_database(animals, current_user):
    time.sleep(1)
    clear_screen()
    search_animals(animals, current_user)

# Sort or filter the database
def sort_or_filter_database(animals):
    sort_filter_option = input("\nSort or filter? (S/F): ").lower()
    if sort_filter_option == 's':
        sort_database(animals)
    elif sort_filter_option == 'f':
        filter_animals(animals)
    else:
        handle_invalid_input(animals)

# Sort the database
def sort_database(animals):
    clear_screen()
    print_animal_table(animals)
    print("\nSort by:")
    print("1." + Fore.GREEN + " Name (A-Z)" + Style.RESET_ALL)
    print("2." + Fore.GREEN + " Name (Z-A)" + Style.RESET_ALL)
    print("3." + Fore.GREEN + " Age (Youngest to Oldest)" + Style.RESET_ALL)
    print("4." + Fore.GREEN + " Age (Oldest to Youngest)" + Style.RESET_ALL)
    sort_option = input(select_option)

    # Sort animals based on user input
    if sort_option in ['1', '2', '3', '4']:
        sort_key = 'name' if sort_option in ['1', '2'] else 'age'
        reverse_sort = True if sort_option in ['2', '4'] else False
        animals = sort_animals(animals, key=sort_key, reverse=reverse_sort)
        clear_screen()
        print_animal_table(animals)
    else:
        handle_invalid_input(animals)

# View animal profile or exit
def view_animal_profile_or_exit(current_user):
    if current_user['level'] >= 2:
        view_animals_full()
    else:
        exit_database(current_user)

# Modify the database
def modify_database(current_user):
    log_action(current_user, "Entered 'Modify Animal Database'")
    time.sleep(2)
    clear_screen()
    modify_animal_database()

# Exit the database
def exit_database(current_user):
    log_action(current_user, "Exited 'View Animal Database'")
    print("\nExiting...")
    time.sleep(2)
    clear_screen()
    return True
      
# Handle invalid input
def handle_invalid_input(animals):
    print(Fore.RED + invalid_input + Style.RESET_ALL)
    time.sleep(2)
    clear_screen()
    print_animal_table(animals)

if __name__ == "__main__":
    view_animals()