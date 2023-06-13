#  Script to scrape Australian postalcodes, locality and state from DATA.gov.au
#                          (Australian Government)GNAF-2023
#                 GNAF stands for Geoscape Geocoded National Access File.
#                           by Pabitra Jana
########################################################################################


from flask import Flask, request, jsonify
# Integrated API code to retrieve state and locality based on the postcode
import psycopg2
import json
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print(os.environ.get('DBNAME'))
print(os.getenv('DBNAME'))

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        try:
            # Get the postcode from the user input
            postcode = request.form.get('postcode')

            # Check if the postcode is a number
            if not postcode.isdigit():
                raise ValueError("Invalid postcode. Please enter a numeric value.")

            db_name = os.getenv('DBNAME')
            db_user = os.getenv('USER')
            db_password = os.getenv('PASSWORD')
            db_host = os.getenv('HOST')

            conn = psycopg2.connect(
                dbname = db_name,            
                user = db_user,
                password = db_password,
                host = db_host
            )

            cur = conn.cursor()

            query = """
            SELECT DISTINCT address_detail.postcode, locality.locality_name, state.state_name
            FROM address_detail
            JOIN locality ON address_detail.locality_pid = locality.locality_pid
            JOIN state ON locality.state_pid = state.state_pid
            WHERE address_detail.postcode = %(postcode)s;
            """

            cur.execute(query, {'postcode': postcode})

            table_dict = {}
            rows = cur.fetchall()

            if not rows:
                return jsonify({'message': 'No results found for the entered postcode.'}), 200

            table_list = []  # Empty list to store dictionaries

            for row in rows:
                keys = ['Postcode', 'Locality', 'State']
                values = row
                table_dict = dict(zip(keys, values))
                table_list.append(table_dict)

            cur.close()
            conn.close()

            # Return the JSON response
            return jsonify(table_list)
        
        except (psycopg2.Error, KeyError, TypeError, ValueError) as e:
            # Handle specific exceptions
            error_message = str(e)
            return jsonify({'error': error_message}), 500    

    # If it's a GET request or no data is submitted, display the form
    return '''
    <form method="post">
        <label for="postcode">Enter postcode:</label>
        <input type="text" id="postcode" name="postcode" required>
        <input type="submit" value="Submit">
    </form>
    '''

if __name__ == '__main__':
    app.run()
