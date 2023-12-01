# ufc_stats_scraping
Retrieve all the events and figths stadistics from [ufcstats](http://ufcstats.com/)

## Retrieving the information

The programs which retrieves the information are found in: [src/scraping](src/scraping). 

Run:

- [src/scraping/scrape_fighter_details.py](src/scraping/scrape_fighter_details.py)
- [src/scraping/scrape_fighter_tott.py](src/scraping/scrape_fighter_tott.py)

This programs stores all the information retrieved in the directory: [data](data).

Files generated:

- [data/ufc_fighter_details.csv](data/ufc_fighter_details.csv)
- [data/ufc_fighter_tott.csv](data/ufc_fighter_tott.csv)

## Database

All the information retrieved is stored in a postgreSQL database. 

Run the program [src/manage_db](src/manage_db) to create/update the information in the database. 

The way to connect and manage the database is defined in the database API [src/db_utils.py](src/db_utils.py).

## Testing

The directory [tests](tests) contains all the testing of the application:

- [tests/main.py](tests/main.py) is in charge of launching all the test in the directory.
- [tests/test_db.py](tests/test_db.py) unit tests for [src/db_utils.py](src/db_utils.py).

Run all the tests:

```python
python3 tests/main.py
```

## Configuration files

The directory [config](config) keeps all the configuration files for running the programs. The list of configuration files is:

- [config/database_config.yaml](config/database_config.yaml) has all the variables related to the database.
- [config/scrape_config.yaml](config/scrape_config.yaml) has all the variables needed to scrape in [ufcstats](http://ufcstats.com/).



