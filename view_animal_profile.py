import tkinter as tk
import time
from PIL import Image, ImageTk
from tkinter import filedialog
from colorama import Fore, Style
from common_functions import clear_screen, load_animal_data, log_action, get_mongodb_uri, print_animal_table
from sudo_user import sudo_user
from pymongo import MongoClient

# Connect to MongoDB
uri = get_mongodb_uri()
client = MongoClient(uri)

db = client['animal_rescue']
animals_collection = db['animals']
    
def print_animal_table_with_index(animals):
    # Displays the table of animals with index numbers
    clear_screen()
    print("\n🐾 " + Fore.CYAN + "List of Animals" + Style.RESET_ALL + " 🐾")
    print("+------------------------------------------------------------------------------+")
    print("| " + Fore.YELLOW + "Index " + Style.RESET_ALL + "| " + Fore.YELLOW + "Name                 " + Style.RESET_ALL +                  "| " + Fore.YELLOW + "Species " + Style.RESET_ALL +  "| " + Fore.YELLOW + "Breed                " + Style.RESET_ALL +                "| " + Fore.YELLOW + "Gender " + Style.RESET_ALL + "| " + Fore.YELLOW + "Age" + Style.RESET_ALL + " |")
    print("+------------------------------------------------------------------------------+")

    for i, animal in enumerate(animals, 1):
        print(f"| {i}     | {animal['name'].ljust(20)} | {animal['species'].ljust(7)} | {animal['breed'].ljust(20)} | {animal['gender'].ljust(6)} | {str(animal['age']).ljust(3)} |")

    print("+------------------------------------------------------------------------------+")

def search_animal_by_name():
    # Asks the user for the name of the animal to search for
    search_name = input("\nEnter the name of the animal to search for: ")

    # Searches the MongoDB collection for animals with the specified name
    animals = list(animals_collection.find({"name": search_name, "adopted": False}))

    print_animal_table_with_index(animals)

    if not animals:
        print(Fore.RED + "No animals found with that name." + Style.RESET_ALL)
        time.sleep(2)
        view_animals_full()
    else:
        selected_index = input("\nEnter the index of the animal to view its profile: ")

        if selected_index == "exit":
            print("\nExiting search...")
            time.sleep(2)
            clear_screen()
            view_animal_profile()

        try:
            selected_index = int(selected_index)
            if 1 <= selected_index <= len(animals):
                selected_animal = animals[selected_index - 1]
                view_animal_profile(selected_index, selected_animal)
            else:
                print(Fore.RED + "Invalid input! Please enter a valid index." + Style.RESET_ALL)
                time.sleep(2)
                view_animal_profile()
        except ValueError:
            print(Fore.RED + "Invalid input! Please enter a valid index." + Style.RESET_ALL)
            time.sleep(2)
            view_animal_profile()

def view_animal_profile(selected_index, selected_animal):
    clear_screen()

    if not selected_animal:
        print(Fore.RED + "No animal found with that name." + Style.RESET_ALL)
        time.sleep(2)
        view_animals_full()
        return

    try:
        selected_index = int(selected_index)
        if 1 <= selected_index <= len(selected_animal):
            animal = selected_animal

            # Create a new Tkinter window
            root = tk.Tk()
            root.title(f"Animal Profile - {animal['name']}")
            root.geometry("800x700")

            def on_closing():
                root.destroy()
            
            root.protocol("WM_DELETE_WINDOW", on_closing)

            if 'image' in animal:
                image = Image.open(animal['image'])
                image = image.resize((350, 350))
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(root, image=photo)
                image_label.image = photo
                image_label.pack(pady=10)

            # Create a frame to hold the labels and upload button
            frame = tk.Frame(root)
            frame.pack(pady=10)

            # Display the animal details
            tk.Label(frame, text="Name:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w")
            tk.Label(frame, text=animal['name'], font=("Helvetica", 12)).grid(row=0, column=1, sticky="w")

            tk.Label(frame, text="Species:", font=("Helvetica", 12, "bold")).grid(row=1, column=0, sticky="w")
            tk.Label(frame, text=animal['species'], font=("Helvetica", 12)).grid(row=1, column=1, sticky="w")

            tk.Label(frame, text="Breed:", font=("Helvetica", 12, "bold")).grid(row=2, column=0, sticky="w")
            tk.Label(frame, text=animal['breed'], font=("Helvetica", 12)).grid(row=2, column=1, sticky="w")

            tk.Label(frame, text="Gender:", font=("Helvetica", 12, "bold")).grid(row=3, column=0, sticky="w")
            tk.Label(frame, text=animal['gender'], font=("Helvetica", 12)).grid(row=3, column=1, sticky="w")

            tk.Label(frame, text="Age:", font=("Helvetica", 12, "bold")).grid(row=4, column=0, sticky="w")
            tk.Label(frame, text=str(animal['age']), font=("Helvetica", 12)).grid(row=4, column=1, sticky="w")

            tk.Label(frame, text="Adopted:", font=("Helvetica", 12, "bold")).grid(row=5, column=0, sticky="w")
            tk.Label(frame, text=str(animal['adopted']), font=("Helvetica", 12)).grid(row=5, column=1, sticky="w")

            # Upload button
            def upload_image():
                file_path = filedialog.askopenfilename()
                if file_path:
                    # Save the image to the database
                    animals_collection.update_one({'name': animal['name']}, {'$set': {'image': file_path}})


            upload_button = tk.Button(root, text="Upload Image", command=upload_image, width=15, height=2)
            upload_button.pack(pady=10)

            # Close button
            close_button = tk.Button(root, text="Close", command=root.destroy, width=10, height=2, bg="red", fg="white")
            close_button.pack(pady=20)

            root.mainloop()
        else:
            print(Fore.RED + "Invalid input! Please enter a valid index." + Style.RESET_ALL)
            time.sleep(2)
            view_animal_profile()
    except ValueError:
        print(Fore.RED + "Invalid input! Please enter a valid index." + Style.RESET_ALL)
        time.sleep(2)
        view_animal_profile()

def view_animals_full():
    clear_screen()
    current_user = sudo_user()
    while True:
        # Continuous loop for viewing the animal options
        print(Fore.CYAN + "\n⚙️ Options ⚙️" + Style.RESET_ALL)
        print("\n1. " + Fore.GREEN + "Search for animal" + Style.RESET_ALL)
        print("2. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
        
        user_input = input("\nPlease select an option: ")
        
        if user_input == '1':
            search_animal_by_name()

        elif user_input == '2':
            print("\nExiting...")
            log_action(current_user, "Exited 'View Profile'")
            time.sleep(2)
            clear_screen()
            return
        
        else:
            print("\nInvalid input. Please choose one of the options.")
            time.sleep(2)
            clear_screen()