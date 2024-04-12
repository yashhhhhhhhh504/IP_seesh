from flask import Flask, request, jsonify
import psycopg2
from fuzzywuzzy import fuzz

app = Flask(__name__)

def connect_to_database():
    try:
        return psycopg2.connect(
            dbname="IP",
            user="yash",
            password="yash",
            host="localhost",
            port="5433"
        )
    except psycopg2.Error as e:
        return f"Error connecting to the database: {e}"

def search_folders_and_files(query):
    results = []
    connection = connect_to_database()
    if isinstance(connection, str):
        return {"error": connection}

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

    return {"results": results}

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    search_results = search_folders_and_files(query)
    return jsonify(search_results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
