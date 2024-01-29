import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from colorama import Fore, Style
from tkinter import messagebox
from common_functions import clear_screen, load_data, save_data


ANIMAL_DATA_FILE = "animals.json"

def print_animal_table_with_index(animals):
    """Prints the table of animals with index numbers."""
    print("\n🐾 " + Fore.CYAN + "List of Animals" + Style.RESET_ALL + " 🐾")
    print("--------------------------------------------------------------------------------------------------")
    print("| " + Fore.YELLOW + "Index".ljust(6) + Style.RESET_ALL + "| " + Fore.YELLOW + "Name".ljust(20) + Style.RESET_ALL + "| " + Fore.YELLOW + "Species".ljust(8) + Style.RESET_ALL + "| " + Fore.YELLOW + "Breed".ljust(25) + Style.RESET_ALL + "| "  + Fore.YELLOW + "Gender".ljust(15) + Style.RESET_ALL + Fore.YELLOW + "Age".ljust(1) + Style.RESET_ALL + " | " + Fore.YELLOW + "Adopted".ljust(7) + Style.RESET_ALL + " |")
    print("--------------------------------------------------------------------------------------------------")

    for i, (name, data) in enumerate(animals.items(), 1):
        index_column = f"| {str(i).ljust(6)}"
        name_column = f"| {name.ljust(20)}"
        species_column = f"| {data['species'].ljust(8)}"
        breed_column = f"| {data['breed'].ljust(25)}"
        gender_column = f"| {data['gender'].ljust(15)}"
        age_column = f"| {str(data['age']).ljust(3)}"
        adopted_column = f"| {str(data['adopted']).ljust(7)}|"
        print(index_column + name_column + species_column + breed_column + gender_column + age_column + adopted_column)

    print("--------------------------------------------------------------------------------------------------")

def select_animal_to_view(animals):
    """Allows the user to select an animal from the table to view its profile."""
    clear_screen()
    print_animal_table_with_index(animals)
    selected_index = input("\nEnter the index of the animal to view its profile: ")

    try:
        selected_index = int(selected_index)
        if 1 <= selected_index <= len(animals):
            selected_animal = list(animals.keys())[selected_index - 1]
            view_animal_profile(animals[selected_animal])
        else:
            print(Fore.RED + "Invalid index!" + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "Invalid input! Please enter a valid index." + Style.RESET_ALL)

def view_animal_profile():
    """Displays the profile of the selected animal in a Tkinter window."""
    clear_screen()
    animals = load_data(ANIMAL_DATA_FILE)
    
    print_animal_table_with_index(animals)
    selected_index = input("\nEnter the index of the animal to view its profile: ")

    try:
        selected_index = int(selected_index)
        if 1 <= selected_index <= len(animals):
            selected_animal = list(animals.keys())[selected_index - 1]
            animal = animals[selected_animal]

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
                    animal['image'] = file_path
                    save_data(animals, ANIMAL_DATA_FILE)

            upload_button = tk.Button(root, text="Upload Image", command=upload_image, width=15, height=2)
            upload_button.pack(pady=10)

            # Close button
            close_button = tk.Button(root, text="Close", command=root.destroy, width=10, height=2, bg="red", fg="white")
            close_button.pack(pady=20)

            root.mainloop()
        else:
            print(Fore.RED + "Invalid index!" + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "Invalid input! Please enter a valid index." + Style.RESET_ALL)

def view_animals():
    """Main function to view animals."""
    clear_screen()

    while True:
        print(Fore.CYAN + "\n⚙️ Options ⚙️" + Style.RESET_ALL)
        print("\n1. " + Fore.GREEN + "Select an animal to view profile" + Style.RESET_ALL)
        print("2. " + Fore.YELLOW + "Exit" + Style.RESET_ALL)
        
        user_input = input("\nPlease select an option: ")

        if user_input == '1':
            view_animal_profile()
        elif user_input == '2':
            clear_screen()
            return
        else:
            print("\nInvalid input. Please choose one of the options.")