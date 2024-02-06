import time
from colorama import Fore, Style
from common_functions import clear_screen, get_mongodb_uri
from pymongo import MongoClient
from sudo_user import sudo_user

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)

db = client['animal_rescue']
animals_collection = db['animals']
customers_collection = db['customers']

def display_available_animals():
    """
    Display a formatted table of available animals for adoption.
    """
    clear_screen()
    print("\n🐾 " + Fore.CYAN + "Available Animals for Adoption" + Style.RESET_ALL + " 🐾")
    print("+------------------------------------------------------------------------------+")
    print("| " + Fore.YELLOW + "Index " + Style.RESET_ALL + "| " + Fore.YELLOW + "Name                 " + Style.RESET_ALL +                  "| " + Fore.YELLOW + "Species " + Style.RESET_ALL +  "| " + Fore.YELLOW + "Breed                " + Style.RESET_ALL +                "| " + Fore.YELLOW + "Gender " + Style.RESET_ALL + "| " + Fore.YELLOW + "Age" + Style.RESET_ALL + " |")
    print("+------------------------------------------------------------------------------+")

    animals = animals_collection.find({"adopted": False})

    for i, animal in enumerate(animals, 1):
        print(f"| {i}     | {animal['name'].ljust(20)} | {animal['species'].ljust(7)} | {animal['breed'].ljust(20)} | {animal['gender'].ljust(6)} | {str(animal['age']).ljust(3)} |")

    print("+------------------------------------------------------------------------------+")

def search_animals_by_name(name):
    """
    Search for animals by name and display them with their original index numbers.
    """
    clear_screen()
    print("\n🐾 " + Fore.CYAN + "Available Animals for Adoption" + Style.RESET_ALL + " 🐾")
    print("+------------------------------------------------------------------------------+")
    print("| " + Fore.YELLOW + "Index " + Style.RESET_ALL + "| " + Fore.YELLOW + "Name                 " + Style.RESET_ALL +                  "| " + Fore.YELLOW + "Species " + Style.RESET_ALL +  "| " + Fore.YELLOW + "Breed                " + Style.RESET_ALL +                "| " + Fore.YELLOW + "Gender " + Style.RESET_ALL + "| " + Fore.YELLOW + "Age" + Style.RESET_ALL + " |")
    print("+------------------------------------------------------------------------------+")

    # Find animals with the provided name
    animals = list(animals_collection.find({"name": name, "adopted": False}))

    if animals:
        # Display the animals with their original index numbers
        for i, animal in enumerate(animals, 1):
            print(f"| {i}     | {animal['name'].ljust(20)} | {animal['species'].ljust(7)} | {animal['breed'].ljust(20)} | {animal['gender'].ljust(6)} | {str(animal['age']).ljust(3)} |")
        
        print("+------------------------------------------------------------------------------+")
    else:
        print("No animals found with that name.")
        time.sleep(2)
        clear_screen()

    # Return the list of animals
    return animals

def adopt_animal(selected_animal):
    """
    Allow staff to assist customers in adopting an available animal.
    """
    if selected_animal:
        print("\nPlease provide the following information for adoption:")
        # Input validation loop
        while True:
            clear_screen()
            print("\n👤 " + Fore.CYAN + "Setting Up Adoption" + Style.RESET_ALL + " 👤")
            print("\nInform the client that you will require this information from them:")
            print(Fore.GREEN + "\n - Full Name")
            print(" - Email Address")
            print(" - Phone Number")
            print(" - Full Address" + Style.RESET_ALL)
            print("\n Please ask whether they consent to giving these details.")

            client_consent = input("\nDo they consent? (yes/no): ").strip().lower()

            if client_consent == 'yes':
                # Prompt user for input
                customer_name = input("\nYour full name: ").strip()
                customer_email = input("Your email address: ").strip()
                customer_phone = input("Your phone number: ").strip()
                customer_address = input("Your full address (House No., Street, Town, County, Postcode): ").strip()

                # Check if any input is empty
                if not all([customer_name, customer_email, customer_phone, customer_address]):
                    print(Fore.RED + "\nPlease fill in all fields." + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue  # Continue to the next iteration of the loop if any field is empty

                # Check email format
                if '@' not in customer_email or '.' not in customer_email:
                    print(Fore.RED + "\nPlease enter a valid email address." + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue

                # Check phone number format
                if not customer_phone.isdigit() or len(customer_phone) < 10:
                    print(Fore.RED + "\nPlease enter a valid phone number." + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue

                # Check consent to terms
                consent = input("\nBy adopting an animal, you agree to take full responsibility for its welfare and care, including providing a suitable living environment, regular veterinary check-ups, and necessary vaccinations. Do you consent to these terms? (yes/no): ").strip().lower()

                if consent == 'yes':
                    try:
                        # Mark the animal as adopted
                        animals_collection.update_one({"_id": selected_animal["_id"]}, {"$set": {"adopted": True}})

                        # Save customer's information to the "customers" collection
                        customer_data = {
                            "name": customer_name,
                            "email": customer_email,
                            "phone": customer_phone,
                            "address": customer_address,
                            "adopted_animal": selected_animal["_id"]
                        }
                        customers_collection.insert_one(customer_data)

                        print(Fore.GREEN + "\nCongratulations! You have successfully adopted {}.".format(selected_animal["name"]) + Style.RESET_ALL)
                        print("\nThank you for your adoption! You will now return to the main menu.")
                        time.sleep(2)
                        clear_screen()
                        return  # Exit the function after successful adoption
                    except Exception as e:
                        print(Fore.RED + f"An error occurred during adoption: {str(e)}" + Style.RESET_ALL)
                        time.sleep(2)
                        clear_screen()
                else:
                    print(Fore.RED + "\nAdoption cannot proceed without consent to the terms." + Style.RESET_ALL)
                    input(Fore.GREEN + "Press Enter to continue..." + Style.RESET_ALL)
                    clear_screen()
                    return
            else:
                print(Fore.RED + "\nAdoption cannot proceed without consent to the terms." + Style.RESET_ALL)
                input(Fore.GREEN + "Press Enter to continue..." + Style.RESET_ALL)
                clear_screen()
                return
    else:
        print(Fore.RED + "Invalid index! Please select a valid animal." + Style.RESET_ALL)
        time.sleep(2)
        clear_screen()

def view_available_animals():
    """
    Display available animals and provide options to assist customers in adoption.
    """
    clear_screen()
    sudo_user()

    while True:
        print(Fore.CYAN + "\n⚙️ Options ⚙️" + Style.RESET_ALL)
        print("\n1. " + Fore.GREEN + "Assist in adopting an animal" + Style.RESET_ALL)
        print("2. " + Fore.GREEN + "Search animals by name" + Style.RESET_ALL)
        print("3. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
        
        user_input = input("\nPlease select an option: ")

        if user_input == '1':
            display_available_animals()
            try:
                selected_index = int(input("\nEnter the index of the animal you want to adopt: "))
                # Check if the index is valid
                animals_count = animals_collection.count_documents({"adopted": False})
                if 1 <= selected_index <= animals_count:
                    # Get the list of all available animals
                    animals = list(animals_collection.find({"adopted": False}))
                    selected_animal = animals[selected_index - 1]
                    # Allow staff to assist in adopting the selected animal
                    adopt_animal(selected_animal)
                else:
                    print("\nInvalid index. Please select a valid animal.")
                    time.sleep(2)
                    clear_screen()
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")
                time.sleep(2)
                clear_screen()
        elif user_input == '2':
            # Search for animals by name
            search_name = input("\nEnter the name of the animal: ")
            animals = search_animals_by_name(search_name)
            if animals:
                try:
                    selected_index = int(input("\nEnter the index of the animal you want to adopt: "))
                    # Check if the index is valid
                    if 1 <= selected_index <= len(animals):
                        selected_animal = animals[selected_index - 1]
                        # Allow staff to assist in adopting the selected animal
                        adopt_animal(selected_animal)
                    else:
                        print("\nInvalid index. Please select a valid animal.")
                        time.sleep(2)
                        clear_screen()
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.")
                    time.sleep(2)
                    clear_screen()
        elif user_input == '3':
            print("\nExiting...")
            time.sleep(2)
            clear_screen()
            return
        else:
            print("\nInvalid input. Please choose one of the options.")
            time.sleep(2)
            clear_screen()

