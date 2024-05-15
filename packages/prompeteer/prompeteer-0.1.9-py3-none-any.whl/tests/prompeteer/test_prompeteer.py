import csv
import os
import unittest

import prompeteer


class MyTestCase(unittest.TestCase):

    def setUp(self):
        os.environ["AZURE_OPENAI_RESOURCE_NAME"] = "gong-dev-research-ea-uk-south"

    def test_run_prompt_azure(self):
        # Execute the prompt function, potentially stub or mock this in actual tests
        prompeteer.run_prompt(prompt_config_file_path='azure_openai_test_prompt.yaml',
                              output_csv='./output.csv',
                              include_prompt=True,
                              input_csv='./input.csv',
                              row_numbers_to_process=[0, 1],
                              destination='file')

        # Check that the output file has been created
        self.assertTrue(os.path.exists("./output.csv"))

        # Open and verify the output file
        with open(file="./output.csv", mode='r') as output_file:
            reader = csv.reader(output_file, delimiter=",")
            lines = list(reader)

            # Check the header
            self.assertEqual(lines[0], ['request', 'response'])

            # Check that there are exactly two data entries
            self.assertEqual(len(lines), 3)  # Including the header, total should be 3 lines

        # Clean up by removing the output file after the test
        if os.path.exists("./output.csv"):
            os.remove("./output.csv")

    def test_run_prompt_azure_console(self):
        self.assertFalse(os.path.exists("./output.csv"))
        prompeteer.run_prompt(prompt_config_file_path='azure_openai_test_prompt.yaml',
                              output_csv='./output.csv',
                              include_prompt=True,
                              input_csv='./input.csv',
                              row_numbers_to_process=[0, 1],
                              destination='console')
        self.assertFalse(os.path.exists("./output.csv"))

    def test_run_prompt_azure_prompt_not_included(self):
        prompeteer.run_prompt(prompt_config_file_path='azure_openai_test_prompt.yaml',
                              output_csv='./output.csv',
                              include_prompt=False,
                              input_csv='./input.csv',
                              row_numbers_to_process=[0, 1],
                              destination='file')

        # Check that the output file has been created
        self.assertTrue(os.path.exists("./output.csv"))

        # Open and verify the output file
        with open(file="./output.csv", mode='r') as output_file:
            reader = csv.reader(output_file, delimiter=",")
            lines = list(reader)

            # Check the header
            self.assertEqual(lines[0], ['response'])

            # Check that there are exactly two data entries
            self.assertEqual(len(lines), 3)  # Including the header, total should be 3 lines

        # Clean up by removing the output file after the test
        if os.path.exists("./output.csv"):
            os.remove("./output.csv")


if __name__ == '__main__':
    unittest.main()
