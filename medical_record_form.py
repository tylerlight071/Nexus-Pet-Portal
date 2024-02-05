# ! Change this on Monday to work with, when modifying, animal profile 

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # For date picker

class AnimalMedicalHistoryForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Animal Medical History Form")

        # Creating labels and entry fields for the form
        self.name_label = ttk.Label(root, text="Name:")
        self.name_entry = ttk.Entry(root, width=30)

        self.species_label = ttk.Label(root, text="Species:")
        self.species_entry = ttk.Entry(root, width=30)

        self.age_label = ttk.Label(root, text="Age:")
        self.age_entry = ttk.Entry(root, width=10)

        self.weight_label = ttk.Label(root, text="Weight:")
        self.weight_entry = ttk.Entry(root, width=10)

        self.vaccination_label = ttk.Label(root, text="Vaccination Status:")
        self.vaccination_entry = ttk.Entry(root, width=30)

        self.medical_condition_label = ttk.Label(root, text="Medical Condition:")
        self.medical_condition_entry = ttk.Entry(root, width=30)

        self.last_visit_label = ttk.Label(root, text="Last Visit Date:")
        self.last_visit_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)

        self.next_visit_label = ttk.Label(root, text="Next Visit Date:")
        self.next_visit_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)

        self.other_notes_label = ttk.Label(root, text="Other Notes:")
        self.other_notes_entry = tk.Text(root, width=40, height=5)

        # Creating a submit button
        self.submit_button = ttk.Button(root, text="Submit", command=self.submit_form)

        # Placing labels and entry fields using grid layout
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        self.species_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.species_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        self.age_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.age_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

        self.weight_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.weight_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)

        self.vaccination_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.vaccination_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=2)

        self.medical_condition_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.medical_condition_entry.grid(row=5, column=1, padx=5, pady=5, columnspan=2)

        self.last_visit_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.last_visit_entry.grid(row=6, column=1, padx=5, pady=5, columnspan=2)

        self.next_visit_label.grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.next_visit_entry.grid(row=7, column=1, padx=5, pady=5, columnspan=2)

        self.other_notes_label.grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        self.other_notes_entry.grid(row=8, column=1, padx=5, pady=5, columnspan=2)

        self.submit_button.grid(row=9, column=1, padx=5, pady=10, columnspan=2)

    def submit_form(self):
        # Function to handle form submission
        name = self.name_entry.get()
        species = self.species_entry.get()
        age = self.age_entry.get()
        weight = self.weight_entry.get()
        vaccination_status = self.vaccination_entry.get()
        medical_condition = self.medical_condition_entry.get()
        last_visit = self.last_visit_entry.get()
        next_visit = self.next_visit_entry.get()
        other_notes = self.other_notes_entry.get("1.0", tk.END)

        print("Name:", name)
        print("Species:", species)
        print("Age:", age)
        print("Weight:", weight)
        print("Vaccination Status:", vaccination_status)
        print("Medical Condition:", medical_condition)
        print("Last Visit Date:", last_visit)
        print("Next Visit Date:", next_visit)
        print("Other Notes:", other_notes)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalMedicalHistoryForm(root)
    root.mainloop()