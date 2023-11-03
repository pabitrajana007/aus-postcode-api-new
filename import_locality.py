import psycopg2
from decouple import config

# Database connection parameters
db_params = {
    "host": config('DB_HOST'),
    "database": config('DB_NAME'),
    "user": config('DB_USER'),
    "password": config('DB_PASSWORD')
}

# Define the table name
table_name = 'locality'

# List of PSV files to import
psv_files = [
    r'C:\Users\Acer\Downloads\g-naf_feb23_allstates_gda94_psv_1010 (1)\G-NAF\G-NAF FEBRUARY 2023\Standard\ACT_LOCALITY_psv.psv',
    r'C:\Users\Acer\Downloads\g-naf_feb23_allstates_gda94_psv_1010 (1)\G-NAF\G-NAF FEBRUARY 2023\Standard\NSW_LOCALITY_psv.psv',
    r'C:\Users\Acer\Downloads\g-naf_feb23_allstates_gda94_psv_1010 (1)\G-NAF\G-NAF FEBRUARY 2023\Standard\NT_LOCALITY_psv.psv',
    r'C:\Users\Acer\Downloads\g-naf_feb23_allstates_gda94_psv_1010 (1)\G-NAF\G-NAF FEBRUARY 2023\Standard\OT_LOCALITY_psv.psv',
    r'C:\Users\Acer\Downloads\g-naf_feb23_allstates_gda94_psv_1010 (1)\G-NAF\G-NAF FEBRUARY 2023\Standard\QLD_LOCALITY_psv.psv',
    r'C:\Users\Acer\Downloads\g-naf_feb23_allstates_gda94_psv_1010 (1)\G-NAF\G-NAF FEBRUARY 2023\Standard\SA_LOCALITY_psv.psv',
    r'C:\Users\Acer\Downloads\g-naf_feb23_allstates_gda94_psv_1010 (1)\G-NAF\G-NAF FEBRUARY 2023\Standard\TAS_LOCALITY_psv.psv',
    r'C:\Users\Acer\Downloads\g-naf_feb23_allstates_gda94_psv_1010 (1)\G-NAF\G-NAF FEBRUARY 2023\Standard\VIC_LOCALITY_psv.psv',
    r'C:\Users\Acer\Downloads\g-naf_feb23_allstates_gda94_psv_1010 (1)\G-NAF\G-NAF FEBRUARY 2023\Standard\WA_LOCALITY_psv.psv',
    # Add more file paths as needed
]

# Establish a connection to the database
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Create a cursor with the option to read data from files
# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Iterate through the PSV files and perform the COPY operation for each file
for psv_file in psv_files:
    # Define the COPY command for the current file
    copy_command = f"COPY {table_name} FROM stdin DELIMITER '|' CSV HEADER;"
    
    with open(psv_file, 'r') as f:
        # Execute the COPY command and provide data from the file
        cur.copy_expert(sql=copy_command, file=f)
    
    print(f'Data from {psv_file} has been copied into {table_name}.')

# Commit the changes and close the connection
conn.commit()
conn.close()
