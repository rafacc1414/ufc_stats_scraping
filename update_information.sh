#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

FIGTHER_DETAILS="src/scraping/scrape_fighter_details.py"
FIGTHER_TOTT="src/scraping/scrape_fighter_tott.py"

FIGTHER_TABLE="src/manage_db/fighters_table.py"

# Update data
python3 $FIGTHER_DETAILS
python3 $FIGTHER_TOTT

# Update database
python3 $FIGTHER_TABLE