"""
This program creates or update the fighter table in the postgreSQL database with the data retrieved
with web scrapping from ufc_stats (stored in the csv files).
"""

import sys
import os
import yaml
import csv

current_file_path = os.path.abspath(__file__)
dirname = os.path.dirname(current_file_path)

# Scrapping information
scrape_config_file = f"{dirname}/../../config/scrape_config.yaml"
with open(scrape_config_file, "r") as file:
    scrape_config = yaml.safe_load(file)
UFC_FIGHTER_DETAILS_PATH = (
    f"{dirname}/../../{scrape_config['fighter_details_file_name']}"
)
UFC_FIGHTER_TOTT_PATH = (
    f"{dirname}/../../{scrape_config['fighter_tott_file_name']}"
)

# Get the database credentials
database_config_file = f"{dirname}/../../config/database_config.yaml"
with open(database_config_file, "r") as file:
    db_config = yaml.safe_load(file)

# Get database
sys.path.append(f"{dirname}/../")
import db_utils

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

# Read the CSVs and store the information in the database
with open(UFC_FIGHTER_DETAILS_PATH, "r") as first_csv_file, open(
    UFC_FIGHTER_TOTT_PATH, "r"
) as second_csv_file:
    first_csv_reader = csv.DictReader(first_csv_file)
    second_csv_reader = csv.DictReader(second_csv_file)

    merged_rows = []
    for row1, row2 in zip(first_csv_reader, second_csv_reader):
        merged_row = {
            "fighter": row2["FIGHTER"].lower(),
            "nickname": row1["NICKNAME"].lower(),
            "height": row2["HEIGHT"].lower(),
            "weight": row2["WEIGHT"].lower(),
            "reach": row2["REACH"].lower(),
            "stance": row2["STANCE"].lower(),
            "dob": row2["DOB"].lower(),
            "url": row2["URL"].lower(),
        }
        merged_rows.append(merged_row)

    columns = merged_rows[0].keys()

    columns_str = [
        "fighter VARCHAR PRIMARY KEY",
        "nickname VARCHAR",
        "height VARCHAR",
        "weight VARCHAR",
        "reach VARCHAR",
        "stance VARCHAR",
        "dob VARCHAR",
        "url VARCHAR",
    ]

    if not database.table_exists(db_config["FIGHTERS_TABLE"]):
        if not database.create_table(db_config["FIGHTERS_TABLE"], columns_str):
            print(f"Error: Could not created table")
            exit()

    for row in merged_rows:
        values = []
        for col in columns:
            values.append(f"{row[col]}")

        fighter_name = values[0]
        if database.row_exists(db_config["FIGHTERS_TABLE"], "fighter", fighter_name):
            if not database.update_data(
                db_config["FIGHTERS_TABLE"], "fighter", fighter_name, values, columns
            ):
                print(f"Error: Not merged rows")
                exit()
        else:
            if not database.insert_data(db_config["FIGHTERS_TABLE"], values):
                print(f"Error: Not merged rows")
                exit()

        print(
            f'--- Merged CSV data inserted into table "{db_config["FIGHTERS_TABLE"]}" ---'
        )
