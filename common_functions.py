import json
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)

def save_data(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)
