import os
import sys

dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(f"{dirname}/../../ext_libs")
sys.path.append(f"{dirname}/../../config")

# imports
import pandas as pd
import numpy as np

# import library
import scrape_ufc_stats_library as LIB
import yaml

config_file = f"{dirname}/../../config/scrape_config.yaml"
with open(config_file, "r") as file:
    config = yaml.safe_load(file)

print(config)

# generate list of urls for fighter details
list_of_alphabetical_urls = LIB.generate_alphabetical_urls()
print(list_of_alphabetical_urls)

# create empty dataframe to store all fighter details
all_fighter_details_df = pd.DataFrame()

for url in list_of_alphabetical_urls:
    # get soup
    soup = LIB.get_soup(url)
    # parse fighter details
    fighter_details_df = LIB.parse_fighter_details(
        soup, config["fighter_details_column_names"]
    )
    # concat fighter_details_df to all_fighter_details_df
    all_fighter_details_df = pd.concat([all_fighter_details_df, fighter_details_df])

# write to file
all_fighter_details_df.to_csv(config["fighter_details_file_name"], index=False)


list_of_fighter_urls = list(all_fighter_details_df["URL"])

# create empty df to store fighters' tale of the tape
all_fighter_tott_df = pd.DataFrame(columns=config["fighter_tott_column_names"])

# loop through list_of_fighter_urls
for url in list_of_fighter_urls:
    # get soup
    soup = LIB.get_soup(url)
    # parse fighter tale of the tape
    fighter_tott = LIB.parse_fighter_tott(soup)
    # organise fighter tale of the tape
    fighter_tott_df = LIB.organise_fighter_tott(
        fighter_tott, config["fighter_tott_column_names"], url
    )
    # concat fighter
    all_fighter_tott_df = pd.concat([all_fighter_tott_df, fighter_tott_df])

# write to file
all_fighter_tott_df.to_csv(config["fighter_tott_file_name"], index=False)
