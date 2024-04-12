import os
import pickle
import json
import time
path = "/Users/nvgenomics/Desktop/IP_project/Database"
def save_state(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    with open('file_list.pkl', 'wb') as f:
        pickle.dump(file_list, f)

def list_files(directory):
    saved_file_list = []
    if os.path.exists('file_list.pkl'):
        with open('file_list.pkl', 'rb') as f:
            saved_file_list = pickle.load(f)
    
    current_file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            current_file_list.append(os.path.join(root, file))
    
    new_files = set(current_file_list) - set(saved_file_list)
    removed_files = set(saved_file_list) - set(current_file_list)
    if new_files:
        print("Newly added files or directories:")
        for file in new_files:
            print(file)
            # Add new file info to JSON
            update_json(file, "added")
    if removed_files:
        print("Removed files or directories:")
        for file in removed_files:
            print(file)
            # Add removed file info to JSON
            update_json(file, "removed")
    save_state(directory)
def update_json(file_path, action):
    if os.path.exists('file_changes.json'):
        with open('file_changes.json', 'r') as f:
            file_changes = json.load(f)
    else:
        file_changes = {}
    file_changes[file_path] = action
    with open('file_changes.json', 'w') as f:
        json.dump(file_changes, f, indent=4)
while True:
    list_files(path)
    time.sleep(10)  # Check every 10 seconds
