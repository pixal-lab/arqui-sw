import psycopg2

def execute_query(query):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host="postgres",
        database="postgres",
        user="postgres",
        password="postgres"
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Execute the query
        cursor.execute(query)

        # Fetch all the rows returned by the query
        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()

            # Convert the rows to text
            result = '\n'.join([', '.join(map(str, row)) for row in rows])    
        else:
            # Para comandos que no devuelven resultados (INSERT, UPDATE, DELETE)
            conn.commit()
            result = "Query executed successfully"

        return result

    except Exception as e:
        # Handle the exception and return "ERROR"
        return "ERROR DB: " + e

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()