import psycopg2
from decouple import config

# Database connection parameters
db_params = {
    "host": config('DB_HOST'),
    "database": config('DB_NAME'),
    "user": config('DB_USER'),
    "password": config('DB_PASSWORD')
}

# SQL command to create the new table
create_table_query = """
CREATE TABLE postcode_db AS 
SELECT DISTINCT address_detail.postcode, locality.locality_name, state.state_name
FROM address_detail 
JOIN locality ON address_detail.locality_pid = locality.locality_pid
JOIN state ON locality.state_pid = state.state_pid;
"""

def main():
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Execute the SQL command to create the new table
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'postcode_db' created successfully!")

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

if __name__ == "__main__":
    main()
