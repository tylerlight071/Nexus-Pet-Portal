from colorama import Fore, Style
from common_functions import clear_screen
from tabulate import tabulate

animal_table_with_index = ("+---------------------------------------------------------------------------------+")

# Function to print the table of animals
def print_animal_table(animals):
    
    # Print table header
    print("\n🐾 " + Fore.CYAN + "List of Animals" + Style.RESET_ALL + " 🐾\n")

    # Prepare table data
    table_data = []
    for animal in animals:
        row = [animal['name'], animal['species'], animal['breed'], animal['gender'], animal['age'], animal['adopted']]
        table_data.append(row)

    # Print table with tabulate
    headers = [Fore.YELLOW + "Name", "Species", "Breed", "Gender", "Age", "Adopted" + Style.RESET_ALL]
    print(tabulate(table_data, headers=headers, tablefmt='fancy_grid'))

# presto
# pretty
# psql

# Function to print the table of animals with index numbers
def print_animal_table_with_index(animals):
    # Displays the table of animals with index numbers
    clear_screen()
    print("\n🐾 " + Fore.CYAN + "List of Animals" + Style.RESET_ALL + " 🐾")
    print(animal_table_with_index)
    print("| " + Fore.YELLOW + "Index    " + Style.RESET_ALL + "| " + Fore.YELLOW + "Name                 " + Style.RESET_ALL +                  "| " + Fore.YELLOW + "Species " + Style.RESET_ALL +  "| " + Fore.YELLOW + "Breed                " + Style.RESET_ALL +                "| " + Fore.YELLOW + "Gender " + Style.RESET_ALL + "| " + Fore.YELLOW + "Age" + Style.RESET_ALL + " |")
    print(animal_table_with_index)

    for i, animal in enumerate(animals, 1):
        print(f"| {i}        | {animal['name'].ljust(20)} | {animal['species'].ljust(7)} | {animal['breed'].ljust(20)} | {animal['gender'].ljust(6)} | {str(animal['age']).ljust(3)} |")

    print(animal_table_with_index)