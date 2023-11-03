import psycopg2
from decouple import config

# Database connection parameters
db_params = {
    "host": config('DB_HOST'),
    "database": config('DB_NAME'),
    "user": config('DB_USER'),
    "password": config('DB_PASSWORD')
}

# Path to the SQL file with table creation commands
sql_file_path = config('SQL_FILE_PATH')

def execute_sql_from_file(conn, file_path):
    try:
        with open(file_path, 'r') as file:
            sql_commands = file.read()

        cursor = conn.cursor()
        cursor.execute(sql_commands)
        conn.commit()
        print("Table creation commands executed successfully.")
    except (psycopg2.DatabaseError, Exception) as error:
        conn.rollback()
        print(f"Error: {error}")
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(**db_params)
        execute_sql_from_file(conn, sql_file_path)
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Connection or execution error: {error}")
