import psycopg2
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

def binary_search_in_main_table(rows, search_term, column_index):
    left = 0
    right = len(rows) - 1
    matching_rows = []

    while left <= right:
        mid = (left + right) // 2
        mid_value = str(rows[mid][column_index])

        if mid_value.lower() == search_term.lower():
            matching_rows.append(rows[mid])
            # Check left side for more occurrences
            i = mid - 1
            while i >= left and str(rows[i][column_index]).lower() == search_term.lower():
                matching_rows.append(rows[i])
                i -= 1
            # Check right side for more occurrences
            j = mid + 1
            while j <= right and str(rows[j][column_index]).lower() == search_term.lower():
                matching_rows.append(rows[j])
                j += 1
            break
        elif mid_value.lower() < search_term.lower():
            left = mid + 1
        else:
            right = mid - 1

    return matching_rows

# Example usage
def main():
    try:
        connection = connect_to_database()
        if connection is None:
            print("Unable to connect to the database.")
            return

        cursor = connection.cursor()

        # Construct SQL query
        query = "SELECT * FROM main ORDER BY column_name"  # Replace 'column_name' with the actual column name you want to search in
        cursor.execute(query)
        
        # Fetch all the rows
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        search_term = input("Enter search term: ")
        column_index = 0  # Assuming searching in the first column, you can change this accordingly
        matching_rows = binary_search_in_main_table(rows, search_term, column_index)
        
        if len(matching_rows) == 0:
            print("No matching records found.")
        else:
            print("Matching records:")
            for row in matching_rows:
                print(row)  # Modify this to print specific columns if needed

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()


