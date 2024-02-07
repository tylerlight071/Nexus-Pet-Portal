import time
from colorama import Fore, Style
from common_functions import clear_screen, get_mongodb_uri, get_input
from pymongo import MongoClient

NON_VALID_INPUT = "Please enter a valid option."

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)

db = client['animal_rescue']
customers_collection = db['customers']

def section_clear():
    print(Fore.GREEN + "\nSection Completed." + Style.RESET_ALL)
    time.sleep(2)
    clear_screen()

def adopt_dog_form():
        # Input validation loop
        while True:
            clear_screen()
            print("\n👤 " + Fore.CYAN + "Setting Up Adoption" + Style.RESET_ALL + " 👤")
            print("\nInform the client that you will require this information from them:")
            print(Fore.GREEN + "\n - Title")
            print(" - Full Name")
            print(" - Email Address")
            print(" - Phone Number")
            print(" - Full Address")
            print(" - Housing Details (Own/Rent, Residents)")
            print("\n Please ask whether they consent to giving these details." + Style.RESET_ALL)

            client_consent = get_input("\nDo they consent? (yes/no): ").strip().lower()

            if client_consent == 'yes':
                clear_screen()
                print(Fore.LIGHTMAGENTA_EX + "\nClient Information" + Style.RESET_ALL)
                customer_title = get_input("\nTitle (Mr/Mrs/Ms/Dr): ").strip()
                # Check title
                if customer_title not in ['Mr', 'Mrs', 'Ms', 'Dr']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue
                customer_name = get_input("Your full name: ").strip()
                customer_email = get_input("Your email address: ").strip()
                # Check email format
                if '@' not in customer_email or '.' not in customer_email:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue
                customer_phone = get_input("Your phone number: ").strip()
                # Check phone number format
                if not customer_phone.isdigit() or len(customer_phone) < 10:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue
                customer_address = get_input("Your full address (House No., Street, Town, County, Postcode): ").strip()

                branch_location = get_input("\nWhich branch are you adopting from? ").strip()

                chosen_animal = get_input("\nDo you know which animal are you interested in adopting? ").strip()
                if chosen_animal not in ['yes', 'no']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue

                elif chosen_animal == 'yes':
                    print(Fore.CYAN +"\nEnsure the client is aware that they may not get the animal they are interested in but can be matched to another." + Style.RESET_ALL)
                    time.sleep(1)
                    chosen_animal = get_input(Fore.YELLOW + "Please specify the name, breed and age if known: " + Style.RESET_ALL).strip()

                elif chosen_animal == 'no':
                    chosen_animal = "N/A"

                section_clear()

                print(Fore.LIGHTMAGENTA_EX + "\nHousing Details" + Style.RESET_ALL)                
                own_rent = get_input("\nDo you own or rent your home? ").strip()
                
                if own_rent not in ['own', 'rent']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue

                elif own_rent == 'rent':
                    landlord_permission = get_input(Fore.YELLOW +"Do you have permission from your landlord to keep pets? (yes/no): " + Style.RESET_ALL).strip().lower()
                
                garden = get_input("\nDo you have a garden? (yes/no/communal): ").strip().lower()
                if garden not in ['yes', 'no', 'communal']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue

                elif garden == 'yes':
                    garden_size = get_input(Fore.YELLOW + "What is the size of your garden? " + Style.RESET_ALL).strip()
                    garden_fenced = get_input("Is your garden fully fenced? (yes/no): " + Style.RESET_ALL).strip().lower()
                    garden_access = get_input("How is the garden accessed? " + Style.RESET_ALL).strip()
                
                elif garden == "communal":
                    garden_size = "N/A"
                    garden_fenced = "N/A"
                    garden_access = "N/A"
                
                elif garden == "no":
                    garden_size = "N/A"
                    garden_fenced = "N/A"
                    garden_access = "N/A"

                section_clear()

                print(Fore.LIGHTMAGENTA_EX + "\nHousehold Details" + Style.RESET_ALL)

                residents_at_address = get_input("\nHow many people live at your address? ").strip()

                children_at_address = get_input("Do you have children living at your address? (yes/no): ").strip().lower()
                
                if children_at_address not in ['yes', 'no']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue
                
                elif children_at_address == 'yes':
                    residents_children_age = get_input(Fore.YELLOW + "What are the ages of the children living at your address? " + Style.RESET_ALL).strip()

                elif children_at_address == 'no':
                    residents_children_age = "N/A"

                visiting_children = get_input("Do children visit your home? (yes/no): ").strip().lower()
                
                if visiting_children not in ['yes', 'no']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue
                
                elif visiting_children == 'yes':
                    visiting_children_age = get_input(Fore.YELLOW + "What are the ages of the visiting children? " + Style.RESET_ALL).strip()
                
                elif visiting_children == 'no':
                    visiting_children_age = "N/A"

                section_clear()

                print(Fore.LIGHTMAGENTA_EX + "\nOther Pets" + Style.RESET_ALL)

                other_dogs = get_input("\nDo you have any other dogs? (yes/no): ").strip().lower()
                
                if other_dogs not in ['yes', 'no']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue
                
                elif other_dogs == 'yes':
                    other_dogs_number = get_input(Fore.YELLOW + "How many other dogs do you have? " + Style.RESET_ALL).strip()
                    other_dogs_age = get_input(Fore.YELLOW + "What are the ages of the other dogs? " + Style.RESET_ALL).strip()
                    other_dogs_gender = get_input(Fore.YELLOW + "What are the genders of the other dogs? " + Style.RESET_ALL).strip()
                    other_dogs_neutered = get_input(Fore.YELLOW + "Are the other dogs neutered? (yes/no): " + Style.RESET_ALL).strip().lower()
                    other_dogs_vaccinated = get_input(Fore.YELLOW + "Are the other dogs vaccinated? (yes/no): " + Style.RESET_ALL).strip().lower()

                elif other_dogs == 'no':
                    other_dogs_number = "N/A"
                    other_dogs_age = "N/A"
                    other_dogs_gender = "N/A"
                    other_dogs_neutered = "N/A"
                    other_dogs_vaccinated = "N/A"

                other_animals = get_input("Do you have any other animals? (yes/no): ").strip().lower()
                
                if other_animals not in ['yes', 'no']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue

                elif other_animals == 'no':
                    other_animals_type = "N/A"

                elif other_animals == 'yes':
                    other_animals_type = get_input(Fore.YELLOW + "What type of animals do you have? " + Style.RESET_ALL).strip()

                section_clear()

                print(Fore.LIGHTMAGENTA_EX + "\nExercise and Routine" + Style.RESET_ALL)
                weekday_exercise = get_input("\nHow often will the dog be exercised on weekdays? ").strip()
                weekend_exercise = get_input("How often will the dog be exercised on weekends? ").strip()

                how_often_alone = get_input("How often will the dog be left alone? ").strip()
                alone_time = get_input("How long will the dog be left alone each day? ").strip()
                
                section_clear()

                print(Fore.LIGHTMAGENTA_EX + "\nFuture Plans" + Style.RESET_ALL)
                moving_plans = get_input("\nDo you have any plans to move in the next 6 months? (yes/no): ").strip().lower()
                
                if moving_plans not in ['yes', 'no']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue

                elif moving_plans == 'yes':
                    moving_timeframe = get_input(Fore.YELLOW + "When do you plan to move? " + Style.RESET_ALL).strip()
                
                elif moving_plans == 'no':
                    moving_timeframe = "N/A"

                holiday_plans = get_input("Do you have any holiday plans in the near future? (yes/no): ").strip().lower()
                
                if holiday_plans not in ['yes', 'no']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue

                elif holiday_plans == 'yes':
                    holiday_timeframe = get_input(Fore.YELLOW + "When do you plan to go on holiday? " + Style.RESET_ALL).strip()

                elif holiday_plans == 'no':
                    holiday_timeframe = "N/A"

                section_clear()

                print(Fore.LIGHTMAGENTA_EX + "\nIdeal Dog" + Style.RESET_ALL)
                print(Fore.GREEN + "\nWhat type of dog are you looking for? " + Style.RESET_ALL)
                print(" - Size")
                print(" - Age")
                print(" - Breed")
                print(" - Temperament")
                print(" - Energy Level")
                print(" - Grooming Needs")
                print(" - Training Needs")
                print(" - Health Needs")
                
                print("Please fill in all entries. If you are unsure, please enter 'N/A'.")

                ideal_dog_size = get_input("\nSize: ").strip()
                ideal_dog_age = get_input("Age: ").strip()
                ideal_dog_breed = get_input("Breed: ").strip()
                ideal_dog_temperament = get_input("Temperament: ").strip()
                ideal_dog_energy = get_input("Energy Level: ").strip()
                ideal_dog_grooming = get_input("Grooming Needs: ").strip()
                ideal_dog_training = get_input("Training Needs: ").strip()
                ideal_dog_health = get_input("Health Needs: ").strip()

                section_clear()

                print(Fore.LIGHTMAGENTA_EX + "\nOther Requirements" + Style.RESET_ALL)

                print(Fore.GREEN + "\nPlease specify any other requirements: " + Style.RESET_ALL)
                print(" - Must be good with cats ")
                print(" - Must be good with other dogs ")
                print(" - Must be good with children ")
                print(" - Must be good with strangers ")
                print(" - Must be house trained ")
                print(" - Must be crate trained ")
                print(" - Must be good on the lead ")
                print(" - Must be good off the lead")
                print(" - Must be good with travelling")

                other_requirements = get_input(Fore.YELLOW + "\nDo you have any other requirements? (yes/no) " + Style.RESET_ALL).strip()
                if other_requirements not in ['yes', 'no']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue

                elif other_requirements.lower() == "no":
                    other_requirements = "N/A"

                elif other_requirements.lower() == "yes":
                    other_requirements = get_input(Fore.YELLOW + "Please specify: " + Style.RESET_ALL).strip()

                experience = get_input("\nDo you have any experience with dogs? (yes/no) ").strip()
                
                if experience not in ['yes', 'no']:
                    print(Fore.RED + f"\n{NON_VALID_INPUT}" + Style.RESET_ALL)
                    time.sleep(2)
                    clear_screen()
                    continue

                elif experience == 'yes':
                    experience = get_input(Fore.YELLOW + "Please provide details of your experience: " + Style.RESET_ALL).strip()
                
                elif experience == 'no':
                    experience = "N/A"

                section_clear()

                print(Fore.LIGHTMAGENTA_EX + "\nConsent to Terms" + Style.RESET_ALL)
                signature = get_input("\nPlease enter your full name as a signature: ").strip()
                date = get_input("Please enter today's date (dd/mm/yyy): ").strip()             

                # Check consent to terms
                consent = get_input("\nBy adopting an animal, you agree to take full responsibility for its welfare and care, including providing a suitable living environment, regular veterinary check-ups, and necessary vaccinations. Do you consent to these terms? (yes/no): ").strip().lower()

                if consent == 'yes':
                    try:                      
                        # Save customer's information to the "customers" collection
                        customer_data = {
                            "title": customer_title,
                            "name": customer_name,
                            "email": customer_email,
                            "phone": customer_phone,
                            "address": customer_address,
                            "branch_location": branch_location,
                            "chosen_animal": chosen_animal,
                            "own/rent": own_rent,
                            "permission": landlord_permission,
                            "garden": garden,
                            "garden_size": garden_size,
                            "garden_fenced": garden_fenced,
                            "garden_access": garden_access,
                            "residents_at_address": residents_at_address,
                            "children_at_address": children_at_address,
                            "resident_children_age": residents_children_age,
                            "visiting_children": visiting_children,
                            "visiting_children_age": visiting_children_age,
                            "other_dogs": other_dogs,
                            "other_dogs_number": other_dogs_number,
                            "other_dogs_age": other_dogs_age,
                            "other_dogs_gender": other_dogs_gender,
                            "other_dogs_neutered": other_dogs_neutered,
                            "other_dogs_vaccinated": other_dogs_vaccinated,
                            "other_animals": other_animals,
                            "other_animals_type": other_animals_type,
                            "weekday_exercise": weekday_exercise,
                            "weekend_exercise": weekend_exercise,
                            "how_often_alone": how_often_alone,
                            "alone_time": alone_time,
                            "moving_plans": moving_plans,
                            "moving_timeframe": moving_timeframe,
                            "holiday_plans": holiday_plans,
                            "holdiay_timeframe": holiday_timeframe,
                            "ideal_dog_size": ideal_dog_size,
                            "ideal_dog_age": ideal_dog_age,
                            "ideal_dog_breed": ideal_dog_breed,
                            "ideal_dog_temperament": ideal_dog_temperament,
                            "ideal_dog_energy": ideal_dog_energy,
                            "ideal_dog_grooming": ideal_dog_grooming,
                            "ideal_dog_training": ideal_dog_training,
                            "ideal_dog_health": ideal_dog_health,
                            "other_requirements": other_requirements,
                            "experience": experience,
                            "signature": signature,
                            "date": date
                        }
                        customers_collection.insert_one(customer_data)

                        print("\Application Form sent to SuperUsers.")
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