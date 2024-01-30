import json
import os
import datetime

def clear_screen():
    # Clears the terminal screen based on the OS type
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data(file_name):
    # Load data from a JSON file
    with open(file_name, 'r') as f:
        return json.load(f)

def save_data(data, file_name):
    # Save data to the JSON file with indentation for readability
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

def log_action(username, action_description):
    # Get the current timestamp
    current_time = datetime.datetime.now()

    # Format the log entry
    log_entry = f"[{current_time}] - {username}: {action_description}"
    
    # Define the filepath for the audit log file
    log_file_path = "audit_log.txt"
    
    
    # Check if the file exists, if not, create it
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w"):
            pass
    
    # Append the log entry to the file
    with open(log_file_path, "a") as log_file:
        log_file.write(log_entry + "\n")
