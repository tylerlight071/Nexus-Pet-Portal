import os
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import datetime
import configparser

def clear_screen():
    # Clears the terminal screen based on the OS type
    os.system('cls' if os.name == 'nt' else 'clear')

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

def hash_password(password: str):
    # Hash the password using Argon2
    ph = PasswordHasher(time_cost=10, memory_cost=409600, parallelism=16, hash_len=256, salt_len=256, encoding='utf-8')
    hashed_password = ph.hash(password)
    return hashed_password

def verify_password(stored_password, entered_password):
    # Create a PasswordHasher instance
    ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8, hash_len=16, salt_len=16, encoding='utf-8')

    try:
        # Verify the entered password against the stored password hash
        ph.verify(stored_password, entered_password)
        return True
    except VerifyMismatchError:
        return False
    
def get_mongodb_uri():
    # Read the configuration file
    config = configparser.ConfigParser()
    config_file = 'config.ini'
    if os.path.exists(config_file):
        config.read(config_file)
        return config['DEFAULT']['mongodb_uri']
    else:
        uri = input("Please enter your MongoDB URI: ")
        config['DEFAULT'] = {'mongodb_uri': uri}
        with open(config_file, 'w') as configfile:
            config.write(configfile)
        return uri

