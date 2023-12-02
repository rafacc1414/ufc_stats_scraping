import os
import sys
import yaml
from flask import Flask, request, jsonify
current_file_path = os.path.abspath(__file__)
dirname = os.path.dirname(current_file_path)
sys.path.append(f"{dirname}/../")
import db_utils

app = Flask(__name__)

# Get the database credentials
database_config_file = f"{dirname}/../../config/database_config.yaml"
with open(database_config_file, "r") as file:
    db_config = yaml.safe_load(file)
# Create an instance of PostgreSQLDatabase
database = db_utils.PostgreSQLDatabase(
    db_config["POSTGRES_HOST"],
    db_config["POSTGRES_PORT"],
    db_config["POSTGRES_DB"],
    db_config["POSTGRES_USER"],
    db_config["POSTGRES_PASSWORD"],
)
database.connect()
if not database.connected:
    print("ERROR: Database is not connected!")
    exit()

# Endpoint to get all data from a table
@app.route('/get_table_data/<table_name>', methods=['GET'])
def get_table_data(table_name):
    data = database.get_table_data(table_name)
    if data is not None:
        return jsonify(data)
    else:
        return jsonify({'error': 'Error fetching data'}), 500

# Add more endpoints as needed

if __name__ == '__main__':
    app.run(debug=True)
