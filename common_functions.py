import json
import os
import hashlib
import datetime

def clear_screen():
    # Clears the terminal screen based on the OS type
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data(file_name):
    # Load data from a JSON file
    with open(file_name, 'r') as f:
        return json.load(f)

def load_animal_data(animals_collection):
    animals = []
    try:
        # Load all animals from the database
        cursor = animals_collection.find({})
        for animal in cursor:
            animals.append(animal)
    except Exception as e:
        print(f"Error loading animal data: {e}")
    return animals

def save_data(data, file_name):
    # Save data to the JSON file with indentation for readability
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

def log_action(username, action_description):
    # Get the current timestamp
    current_time = datetime.datetime.now().replace(microsecond=0)

    # Format the log entry
    log_entry = f"[{current_time}] - {username}: {action_description}"
    
    # Define the filepath for the audit log file
    log_file_path = "audit_log.txt"
    
    # Add separator between log entries
    separator = '-' * 50 + '\n'
    
    # Check if the file exists, if not, create it
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as log_file:
            log_file.write("=== Audit Log ===\n\n")

    try:
        # Append the log entry to the file
        with open(log_file_path, "a") as log_file:
            log_file.write(log_entry + "\n")
            log_file.write(separator)  # Add separator after each entry
    except Exception as e:
        print(f"Error occurred while writing to log file: {e}")

def generate_salt():
    # Generate a 16-byte (128-bit) random salt
    return os.urandom(16)  

def hash_password(password, salt):
    # Combine the password and salt together and hash them
    combined_value = password.encode('utf-8') + salt
    hashed_password = hashlib.sha256(combined_value).hexdigest()
    return hashed_password

def hash_animal_data(animals, salt):
    # Serialize the animal data and hash it
    animal_data_string = json.dumps(animals, sort_keys=True)
    combined_value = animal_data_string.encode('utf-8') + salt
    hashed_animal_data = hashlib.sha256(combined_value).hexdigest()
    return hashed_animal_data
