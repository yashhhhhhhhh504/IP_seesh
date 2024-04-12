# import json
# import psycopg2

# def generate_abbreviation(folder_name):
#     words = folder_name.split()
#     abbreviation = ''
#     for word in words:
#         abbreviation += word[0].upper()
#         if len(abbreviation) >= 4:
#             break
#     if len(abbreviation) < 4:
#         abbreviation += folder_name[:4 - len(abbreviation)].upper()
#     return abbreviation

# conn = psycopg2.connect(
#     dbname="IP",
#     user="yash",
#     password="yash",
#     host="localhost",
#     port="5433"
# )
# cur = conn.cursor()

# # Create MAIN_FOLDER table
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS MAIN_FOLDER (
#         folder_id SERIAL PRIMARY KEY,
#         folder_name VARCHAR(255) NOT NULL,
#         abbreviation VARCHAR(10)  -- Added abbreviation column
#     )
# """)

# # Create FILE table
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS FILE (
#         file_id SERIAL PRIMARY KEY,
#         file_name VARCHAR(255) NOT NULL,
#         file_path TEXT NOT NULL,
#         file_size INTEGER,
#         file_type VARCHAR(100),
#         folder_id INTEGER REFERENCES MAIN_FOLDER(folder_id) ON DELETE CASCADE
#     )
# """)

# conn.commit()

# # Insert data into MAIN_FOLDER and FILE tables
# with open("organized_data.json", "r") as f:
#     data = json.load(f)

# for main_folder, subfolders_data in data.items():
#     abbreviation = generate_abbreviation(main_folder)
#     cur.execute("INSERT INTO MAIN_FOLDER (folder_name, abbreviation) VALUES (%s, %s) RETURNING folder_id", (main_folder, abbreviation))
#     main_folder_id = cur.fetchone()[0]
#     print(f"Inserted main folder: {main_folder} (ID: {main_folder_id})")
    
#     for subfolder, files in subfolders_data.items():
#         for file_data in files:
#             file_name = file_data["file_name"]
#             file_path = file_data["file_path"]
#             file_size = file_data["file_size"]
#             file_type = file_path.split(".")[-1][:50]
#             cur.execute("INSERT INTO FILE (file_name, file_path, file_size, file_type, folder_id) VALUES (%s, %s, %s, %s, %s)",
#                         (file_name, file_path, file_size, file_type, main_folder_id))
#             print(f"Inserted file: {file_name} in main folder: {main_folder}")

# conn.commit()
# cur.close()
# conn.close()


# import json
# import psycopg2
# import re
# import os

# def generate_abbreviation(folder_name):
#     words = folder_name.split()
#     abbreviation = ''
#     for word in words:
#         abbreviation += word[0].upper()
#         if len(abbreviation) >= 4:
#             break
#     if len(abbreviation) < 4:
#         abbreviation += folder_name[:4 - len(abbreviation)].upper()
#     return abbreviation

# def parse_txt_file(file_path):
#     """
#     Parses a .txt file for summary, nouns, and verbs.
#     Returns summary for COMPASS.txt, nouns for _m.txt, and verbs for _n.txt files.
#     """
#     try:
#         with open(file_path, 'r') as file:
#             content = file.read()

#         summary = noun = verb = None
#         if file_path.endswith('COMPASS.txt'):
#             summary = re.search(r'^SUMMARY\s*\$\s*(.*?)\s*\$', content, re.DOTALL)
#             summary = summary.group(1).replace('\n', ' ').strip() if summary else 'No description available.'
#         if file_path.endswith('_m.txt'):
#             noun = re.search(r'^PARTS\s*\$\s*(.*?)\s*\$', content, re.DOTALL)
#             noun = noun.group(1).replace('\n', ' ').strip() if noun else 'N/A'
#         if file_path.endswith('_n.txt'):
#             verb = re.search(r'^ACTION\s*\$\s*(.*?)\s*\$', content, re.DOTALL)
#             verb = verb.group(1).replace('\n', ' ').strip() if verb else 'N/A'

#         return summary, noun, verb
#     except FileNotFoundError:
#         return 'No description available.', 'N/A', 'N/A'

# conn = psycopg2.connect(
#     dbname="IP",
#     user="yash",
#     password="yash",
#     host="localhost",
#     port="5433"
# )
# cur = conn.cursor()

# # Assuming MAIN_FOLDER and FILE table schemas are already created as per previous instructions...

# conn.commit()

# # Insert data into MAIN_FOLDER and FILE tables
# # Assuming the rest of your script is unchanged, we focus on the corrected loop
# with open("organized_data.json", "r") as f:
#     data = json.load(f)

# for folder_name, files in data.items():
#     abbreviation = generate_abbreviation(folder_name)
#     summary = noun = verb = None
    
#     # Initialize variables to store content from .txt, _m.txt, and _n.txt files
#     descriptions = nouns = verbs = ""
    
#     # Loop through each file dictionary within the list for the current main folder
#     for file_data in files:
#         file_name = file_data.get("file_name")
#         file_path = file_data.get("file_path")
#         if file_name.endswith('.txt'):
#             _summary, _noun, _verb = parse_txt_file(file_path)
#             if _summary:
#                 descriptions += _summary + " "
#             if _noun:
#                 nouns += _noun + " "
#             if _verb:
#                 verbs += _verb + " "
    
#     # Adjusted INSERT/UPDATE logic to concatenate summaries, nouns, and verbs from all .txt files within a folder
#     cur.execute("""
#         INSERT INTO MAIN_FOLDER (folder_name, abbreviation, description, noun, verb)
#         VALUES (%s, %s, %s, %s, %s) ON CONFLICT (folder_name) DO UPDATE
#         SET description = EXCLUDED.description, noun = EXCLUDED.noun, verb = EXCLUDED.verb
#         RETURNING folder_id
#     """, (folder_name, abbreviation, descriptions.strip(), nouns.strip(), verbs.strip()))
     
#     folder_id = cur.fetchone()[0]
#     print(f"Processed folder: {folder_name} with ID: {folder_id}")

# conn.commit()
# cur.close()
# conn.close()



import json
import os
import psycopg2

def generate_abbreviation(folder_name):
    words = folder_name.split()
    abbreviation = ''
    for word in words:
        abbreviation += word[0].upper()
    if len(abbreviation) >= 4:
        return abbreviation
    if len(abbreviation) < 4:
        abbreviation += folder_name[:4 - len(abbreviation)].upper()
    return abbreviation

def parse_text_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    description = ""
    noun = ""
    verb = ""
    state = ""

    lines = content.split("\n")
    for line in lines:
        if line.startswith("FUNCTION"):
            description = line.split("$")[1].strip()
        elif line.startswith("PARTS"):
            noun = line.split("$")[1].strip()
        elif line.startswith("ACTION"):
            verb = line.split("$")[1].strip()
        elif line.startswith("STATE"):
            state = line.split("$")[1].strip()

    return description, noun, verb, state

def find_text_files(root_dir):
    text_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".txt"):
                text_files.append(os.path.join(dirpath, filename))
    return text_files

conn = psycopg2.connect(
    dbname="IP",
    user="yash",
    password="yash",
    host="localhost",
    port="5433"
)

cur = conn.cursor()

# Create MAIN_FOLDER table
cur.execute("""
CREATE TABLE IF NOT EXISTS MAIN_FOLDER (
    folder_id SERIAL PRIMARY KEY,
    folder_name VARCHAR(255) NOT NULL,
    abbreviation VARCHAR(10),
    description TEXT,
    noun TEXT,
    verb TEXT
)
""")

# Create FILE table
cur.execute("""
CREATE TABLE IF NOT EXISTS FILE (
    file_id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER,
    file_type VARCHAR(100),
    folder_id INTEGER REFERENCES MAIN_FOLDER(folder_id) ON DELETE CASCADE,
    description TEXT,
    noun TEXT,
    verb TEXT,
    state TEXT
)
""")

conn.commit()

# Insert data into MAIN_FOLDER and FILE tables
with open("organized_data.json", "r") as f:
    data = json.load(f)

for main_folder, subfolders_data in data.items():
    abbreviation = generate_abbreviation(main_folder)
    text_files = find_text_files(f"ADB/ACTUATOR/{main_folder}")
    if text_files:
        description, noun, verb, state = parse_text_file(text_files[0])
    else:
        description, noun, verb, state = "", "", "", ""
    cur.execute("INSERT INTO MAIN_FOLDER (folder_name, abbreviation, description, noun, verb) VALUES (%s, %s, %s, %s, %s) RETURNING folder_id", (main_folder, abbreviation, description, noun, verb))
    main_folder_id = cur.fetchone()[0]
    print(f"Inserted main folder: {main_folder} (ID: {main_folder_id})")

    for subfolder, files in subfolders_data.items():
        for file_data in files:
            file_name = file_data["file_name"]
            file_path = file_data["file_path"]
            file_size = file_data["file_size"]
            file_type = file_path.split(".")[-1][:50]

            text_files = find_text_files(file_path)
            if text_files:
                description, noun, verb, state = parse_text_file(text_files[0])
            else:
                description, noun, verb, state = "", "", "", ""

            cur.execute("INSERT INTO FILE (file_name, file_path, file_size, file_type, folder_id, description, noun, verb, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (file_name, file_path, file_size, file_type, main_folder_id, description, noun, verb, state))
            print(f"Inserted file: {file_name} in main folder: {main_folder}")

conn.commit()
cur.close()
conn.close()