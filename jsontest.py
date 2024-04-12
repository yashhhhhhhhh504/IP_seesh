import os
import json

def get_file_info(file_path):
    file_info = {
        "file_name": os.path.basename(file_path),
        "file_path": file_path,
        "file_size": os.path.getsize(file_path)
    }
    return file_info

def find_json_files(root_dir):
    json_files = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        files_in_dir = []
        for filename in filenames:
            if filename.endswith('.json'):
                file_path = os.path.join(dirpath, filename)
                files_in_dir.append(get_file_info(file_path))
        if files_in_dir:
            json_files[dirpath] = files_in_dir
    return json_files

def main():
    database_path = '/Users/nvgenomics/Desktop/IP_project/Database'
    json_mapping = find_json_files(database_path)
    
    json_file_path = 'database_json_mapping.json'
    try:
        with open(json_file_path, 'w') as json_file:
            json.dump(json_mapping, json_file, indent=4)
        print("JSON mapping file created successfully at:", json_file_path)
    except Exception as e:
        print("Error occurred while creating JSON file:", e)

if __name__ == "__main__":
    main()
