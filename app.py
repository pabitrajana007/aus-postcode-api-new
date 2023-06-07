from flask import Flask, request, jsonify
# Integrated API code to retrieve state and locality based on the postcode
import psycopg2
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        # Get the postcode from the user input
        postcode = request.form.get('postcode')

       

        conn = psycopg2.connect(
            dbname="********",
            user="******",
            password="******",
            host="localhost"
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
