# This codebase can search upto 5 postalcodes, and shows error for invalid postcodes as well !!
# Refactored the code using class and format using Black

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create a SQLAlchemy engine
db_name = os.getenv("DBNAME")
db_user = os.getenv("USER")
db_password = os.getenv("PASSWORD")
db_host = os.getenv("HOST")

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")

# Create a session
Session = sessionmaker(bind=engine)


class PostcodeApp:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route("/", methods=["GET"])
        def display_form():
            # If it's a GET request, display the form
            return """
            <form method="post">
                <label for="postcodes">Enter postcodes (comma-separated):</label>
                <input type="text" id="postcodes" name="postcodes" required>
                <input type="submit" value="Submit">
            </form>
            """

        @self.app.route("/", methods=["POST"])
        def scrape():
            try:
                # Get the comma-separated postcodes from the user input
                postcodes_input = request.form.get("postcodes")

                # Split the input on commas to extract individual postcodes
                postcodes = postcodes_input.split(",")

                # Create a session
                session = Session()

                response_data = {}

                for postcode in postcodes:
                    # Strip leading and trailing spaces from the postcode
                    postcode = postcode.strip()

                    # Check if the postcode is a number having 4-digits
                    if not postcode.isdigit() or len(postcode) != 4:
                        error_message = f"Invalid postcode: {postcode}. Please enter a 4-digit numeric value."
                        response_data[postcode] = {"error": error_message}
                    else:
                        # Use SQLAlchemy to execute the query
                        query = text(
                            """
                        SELECT *
                        FROM postcodeDB
                        WHERE postcode = :postcode
                        """
                        )

                        result = session.execute(query, {"postcode": postcode})

                        postcode_data = []

                        for row in result:
                            keys = ["Postcode", "Locality", "State"]
                            values = row
                            table_dict = dict(zip(keys, values))
                            postcode_data.append(table_dict)

                        if not postcode_data:
                            error_message = (
                                f"404, Postcode {postcode} not found in the database"
                            )
                            response_data[postcode] = {"error": error_message}
                        else:
                            response_data[postcode] = postcode_data

                session.close()

                # Return the JSON response
                return jsonify(response_data)

            except (ValueError, KeyError, TypeError) as e:
                # Handle specific exceptions
                error_message = str(e)
                return jsonify({"error": error_message}), 500

    def run(self):
        if __name__ == "__main__":
            self.app.run()


if __name__ == "__main__":
    postcode_app = PostcodeApp()
    postcode_app.run()
