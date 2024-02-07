from colorama import Fore, Style
from common_functions import clear_screen

basic_animal_table = print("+-------------------------------------------------------------------------------------------+")
animal_table_with_index = ("+---------------------------------------------------------------------------------+")

# Function to print the table of animals
def print_animal_table(animals):
    
    # Print table header
    print("\n🐾 " + Fore.CYAN + "List of Animals" + Style.RESET_ALL + " 🐾")
    print(basic_animal_table)
    print("| " + Fore.YELLOW + "Name".ljust(20) + Style.RESET_ALL + "| " + Fore.YELLOW + "Species".ljust(8) + Style.RESET_ALL + "| " + Fore.YELLOW + "Breed".ljust(25) + Style.RESET_ALL + "| " + Fore.YELLOW + "Gender".ljust(15) + Style.RESET_ALL + "| " + Fore.YELLOW + "Age".ljust(1) + Style.RESET_ALL + " | " + Fore.YELLOW + "Adopted".ljust(7) + Style.RESET_ALL + " |")
    print(basic_animal_table)

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
    print(basic_animal_table)

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