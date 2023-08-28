import sys
sys.path.insert(0, 'src/')
import os
import unittest
import psycopg2

import HtmlTestRunner
import db_utils

POSTGRES_DB = "postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"

class TestPostgreSQLDatabase(unittest.TestCase):
    def setUp(self):
        print("Starting Unit Test")
        self.db = db_utils.PostgreSQLDatabase(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        self.db.connect()

    def tearDown(self):
        self.db.disconnect()
        print("Ending Unit Test\n")

    def test_select_data(self):
        self.db.execute_query('SELECT schema_name FROM information_schema.schemata;')
    def test_drop_table(self):
        self.db.drop_table("pepe")

if __name__ == "__main__":
    reports_dir = f"tests/reports/"
    os.makedirs(f"{reports_dir}", exist_ok=True)

    # # Generate XML report
    # xml_report_path = f"{reports_dir}/report.xml"
    # with open(xml_report_path, "wb") as output:
    #     unittest.main(
    #         testRunner=xmlrunner.XMLTestRunner(output=output),
    #         failfast=False,
    #         buffer=False,
    #         catchbreak=False,
    #     )

    # Generate HTML report using HtmlTestRunner
    html_report_path = f"{reports_dir}"

    unittest.main(
            testRunner=HtmlTestRunner.HTMLTestRunner(output=html_report_path,
                                                     report_name="unit_test_report"),
            failfast=False,
            buffer=False,
            catchbreak=False,
    )