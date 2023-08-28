import unittest
import HtmlTestRunner
import os

# Discover and run all test modules that match the pattern 'test*.py' in the current directory
if __name__ == "__main__":

    reports_dir = f"/tmp/reports/"
    os.makedirs(f"{reports_dir}", exist_ok=True)

    start_dir = "/code/dev/tests/"  # Current directory
    pattern = "test_*.py"
    test_suite = unittest.defaultTestLoader.discover(start_dir, pattern=pattern)

    testRunner=HtmlTestRunner.HTMLTestRunner(output=reports_dir, report_name="unit_test_report")

    test_result = testRunner.run(test_suite)

    # Check if the tests were successful
    if test_result.wasSuccessful():
        print("\n\n\n")
        print("All tests passed!")
    else:
        print("Some tests failed.")
