from flask import Flask, request, render_template, jsonify
import psycopg2
from fuzzywuzzy import fuzz
app = Flask(__name__)
def connect_to_database():
    # Connection details should be configured according to your setup
    try:
        return psycopg2.connect(dbname="IP", user="yash", password="yash", host="localhost", port="5433")
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def search_folders_and_files(query):
    results = []
    connection = connect_to_database()
    if not connection:
        print("Failed to connect to the database.")
        return results  # Return an empty list if the database connection fails

    with connection, connection.cursor() as cursor:
        query = query.upper()
        cursor.execute("SELECT folder_id, folder_name, abbreviation FROM MAIN_FOLDER")
        models = cursor.fetchall()

        for model in models:
            model_id, model_name, abbreviation = model
            if fuzz.partial_ratio(query, model_name) >= 80 or fuzz.partial_ratio(query, abbreviation) >= 80:
                cursor.execute("SELECT file_name, file_type, file_path FROM FILE WHERE folder_id = %s", (model_id,))
                files = cursor.fetchall()
                results.append({
                    "folder_id": model_id,
                    "folder_name": model_name,
                    "files": [{"name": file[0], "type": file[1], "path": file[2]} for file in files]
                })
    return results

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            results = search_folders_and_files(query)
            return render_template('results.html', query=query, results=results)
    # If it's not a POST request or if query is empty, render the home page
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
