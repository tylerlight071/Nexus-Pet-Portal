from common_functions import clear_screen, load_data

ANIMAL_DATA_FILE = "animals.json"

def view_animals():
    clear_screen()
    animals = load_data(ANIMAL_DATA_FILE)
    print("\nList of Animals:")
    for name, data in animals.items():
        print(f"Name: {name} | Species: {data['species']} | Breed: {data['breed']} | Age: {data['age']} | Adopted: {data['adopted']}")  
    while True:
        user_input = input("Enter 'exit' to return to the main menu: ")
        if user_input.lower() == 'exit':
            clear_screen()
            return
        else:
            print("Invalid input. Please choose one of the options.")

if __name__ == "__main__":
    view_animals()
