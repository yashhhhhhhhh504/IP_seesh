import json
import os

def organize_files(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    organized_data = {}

    for item in data:
        file_name = item["file_name"]
        file_path = item["file_path"]
        main_folder, subfolder = get_main_and_subfolders(file_path)

        if main_folder not in organized_data:
            organized_data[main_folder] = {}

        if subfolder not in organized_data[main_folder]:
            organized_data[main_folder][subfolder] = []

        organized_data[main_folder][subfolder].append({
            "file_name": file_name,
            "file_path": file_path,
            "file_size": item["file_size"]
        })

    return organized_data

def get_main_and_subfolders(file_path):
    # Extract main folder and subfolder from file path
    components = file_path.split(os.sep)
    main_folder = components[-3]
    subfolder = components[-2]
    return main_folder, subfolder

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    json_file = "/Users/nvgenomics/Desktop/IP_project/file_info.json"  # Replace with the path to your existing JSON file
    organized_data = organize_files(json_file)
    save_to_json(organized_data, "organized_data.json")
