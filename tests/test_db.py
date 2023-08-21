import unittest
from unittest.mock import MagicMock, patch
import xmlrunner
import HtmlTestRunner

import os, sys

dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(f"{dirname}/../src")
import db_utils


class TestPostgreSQLDatabase(unittest.TestCase):
    def setUp(self):
        # Create a mock connection and cursor for testing
        self.connection_mock = MagicMock()
        self.cursor_mock = MagicMock()
        self.connection_mock.cursor.return_value = self.cursor_mock

    @patch("db_utils.psycopg2.connect")
    def test_connect_success(self, mock_connect):
        mock_connect.return_value = self.connection_mock

        db = db_utils.PostgreSQLDatabase("host", 5432, "database", "user", "password")
        db.connect()

        self.assertTrue(db.connected)
        mock_connect.assert_called_once()

    @patch("db_utils.psycopg2.connect", side_effect=Exception("Connection Error"))
    def test_connect_failure(self, mock_connect):
        db = db_utils.PostgreSQLDatabase("host", 5432, "database", "user", "password")
        db.connect()

        self.assertFalse(db.connected)
        mock_connect.assert_called_once()

    @patch("db_utils.psycopg2.connect")
    def test_disconnect(self, mock_connect):
        mock_connect.return_value = self.connection_mock

        db = db_utils.PostgreSQLDatabase("host", 5432, "database", "user", "password")
        db.connect()
        db.disconnect()

        self.assertFalse(db.connected)
        self.cursor_mock.close.assert_called_once()
        self.connection_mock.close.assert_called_once()

    # Write similar test methods for other functions


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