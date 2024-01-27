from common_functions import clear_screen, load_data
from colorama import Fore, Style

ANIMAL_DATA_FILE = "animals.json"

def view_animals():
    clear_screen()
    animals = load_data(ANIMAL_DATA_FILE)

    print("\n🐾 " + Fore.CYAN + "List of Animals" + Style.RESET_ALL + " 🐾")
    print("-----------------------------------------------------------------------------")
    print("| " + Fore.YELLOW + "Name".ljust(12) + Style.RESET_ALL + "| " + Fore.YELLOW + "Species".ljust(13) + Style.RESET_ALL + "| " + Fore.YELLOW + "Breed".ljust(20) + Style.RESET_ALL + "| " + Fore.YELLOW + "Age" + Style.RESET_ALL + " | " + Fore.YELLOW + "Adopted" + Style.RESET_ALL + " |")
    print("-----------------------------------------------------------------------------")

    for name, data in animals.items():
        name_column = f"| {name.ljust(12)}"
        species_column = f"| {data['species'].ljust(14)}"
        breed_column = f"| {data['breed'].ljust(19)}"
        age_column = f"| {str(data['age']).ljust(4)}"
        adopted_column = f"| {str(data['adopted']).ljust(8)}|"
        print(name_column + species_column + breed_column + age_column + adopted_column)

    print("-----------------------------------------------------------------------------")

    while True:
        user_input = input("Enter 'exit' to return to the main menu: ")
        if user_input.lower() == 'exit':
            clear_screen()
            return
        else:
            print("Invalid input. Please choose one of the options.")

if __name__ == "__main__":
    view_animals()