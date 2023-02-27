import argparse
import json
import pandas as pd
from utils import my_request
from datetime import datetime


def send_csv_file(url, headers, file_name):
    # Define input parameters
    parser = argparse.ArgumentParser(description='Transmits a CSV to a REST-API,handles the response and generates'
                                                 ' an Excel-File taking the input parameters into account.')
    parser.add_argument("-k", "--keys", nargs="*", help="Keys which to be included as additional columns in a table")
    parser.add_argument("-c", "--colored", default=True, help="Boolean flag that determines the row coloring according "
                                                              "to age of 'hu' field")
    args = parser.parse_args()

    # Transmit CSV to server
    decoded_response = my_request(method="POST", url=url, headers=headers, file_name=file_name)

    # Convert server response to pandas DataFrame
    data_frame = pd.DataFrame(json.loads(decoded_response))

    # Sort DataFrame values by response field 'gruppe'
    data_frame = data_frame.sort_values('gruppe')

    # Make sure that columns always contain 'rnr' field
    if 'rnr' not in data_frame:
        data_frame.insert(0, 'rnr', '')

    result_excel_file = data_frame.to_excel(f'vehicles.xlsx', sheet_name='vehicles')


send_csv_file("http://127.0.0.1:5000", {}, 'vehicles.csv')
