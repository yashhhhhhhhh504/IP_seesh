import psycopg2
from fuzzywuzzy import fuzz
import os

def connect_to_database():
    try:
        connection = psycopg2.connect(
            dbname="IP",
            user="yash",
            password="yash",
            host="localhost",
            port="5433"
        )
        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

def search_model(query):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = query.upper()

            # Search for the model based on the query
            search_query = """
            SELECT folder_id, folder_name, abbreviation FROM MAIN_FOLDER
            """
            cursor.execute(search_query)
            models = cursor.fetchall()

            if models:
                for model in models:
                    model_id, model_name, abbreviation = model
                    # Check similarity for both full name and abbreviation
                    if (fuzz.partial_ratio(query, model_name) >= 80 or fuzz.partial_ratio(query, abbreviation) >= 80) or (len(query) < 5 and (fuzz.partial_ratio(query, model_name) >= 80 or fuzz.partial_ratio(query, abbreviation) >= 80)):
                        print(f"Model Name: {model_name}, Model ID: {model_id}")

                        # Retrieve related file data
                        file_query = """
                        SELECT file_name, file_type, file_path FROM FILE WHERE folder_id = %s
                        """
                        cursor.execute(file_query, (model_id,))
                        files = cursor.fetchall()

                        if files:
                            print("Related Files:")
                            for file in files:
                                file_name, file_type, file_path = file
                                print(f"  - {file_name} ({file_type})")
                            open_file_option = input("Enter the name of the file you want to open (or type 'exit' to exit): ")
                            if open_file_option.lower() != 'exit':
                                for file in files:
                                    file_name, _, db_file_path = file
                                    if file_name == open_file_option:
                                        if os.path.exists(db_file_path):
                                            os.system(f"open '{db_file_path}'")  # Open file using default program
                                            break
                                        else:
                                            print("File not found.")
                            else:
                                return  # Exit function if user chooses to exit
                        else:
                            print("No files found for this model.")

            else:
                print("No models found.")

            cursor.close()
            connection.close()

        except psycopg2.Error as e:
            print("Error executing query:", e)
    else:
        print("Error: Unable to connect to the database.")

if __name__ == "__main__":
    while True:
        search_query = input("Enter model name or abbreviation: ")
        if search_query.lower() == 'exit':
            break
        search_model(search_query)
