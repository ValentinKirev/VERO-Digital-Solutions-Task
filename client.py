import argparse
import json
import pandas as pd
from utils import my_request
from datetime import datetime, date
from dateutil import relativedelta

COLORS = {
    'green': '#007500',
    'orange': '#FFA500',
    'red': '#b30000'
}

SERVER_ENDPOINT = "http://127.0.0.1:5000"
FILE_PATH = "vehicles.csv"


def send_csv_file(url, headers, file_name):
    # Define input parameters
    parser = argparse.ArgumentParser(description='Transmits a CSV to a REST-API,handles the response and generates'
                                                 ' an Excel-File taking the input parameters into account.')
    parser.add_argument("-k", "--keys", nargs="*", help="Keys which to be included as additional columns in a table")
    parser.add_argument("-c", "--colored", action="store_true",
                        help="Boolean flag that determines the row coloring according to age of 'hu' field")
    args = parser.parse_args()

    # Transmit CSV to server
    decoded_response = my_request(method="POST", url=url, headers=headers, file_name=file_name)

    # Convert server response to pandas DataFrame
    df = pd.DataFrame(json.loads(decoded_response))

    # Sort DataFrame values by response field 'gruppe'
    df = df.sort_values('gruppe')

    # Make sure that columns always contain 'rnr' field
    if 'rnr' not in df:
        df.insert(0, 'rnr', '')

    # Adding additional columns according to the passed arguments
    result_columns = ['rnr', 'gruppe']

    for key in args.keys:
        if key not in df:
            df.insert(len(df), key, '')
        result_columns.append(key)

    def colorize_rows(row):
        """Colorize rows if args have colored flag"""

        end_date = date.today()
        start_date = datetime.fromisoformat(row["hu"]).date()
        delta = relativedelta.relativedelta(end_date, start_date)
        result_months = delta.months + (delta.years * 12)

        if result_months <= 3:
            color = COLORS['green']
        elif 3 < result_months <= 12:
            color = COLORS['orange']
        else:
            color = COLORS['red']

        return [f'background-color: {color}'] * len(row)

    def tint_cell_text(row):
        """Tint 'labelIds' cell text if 'labelIds' in args"""

        default = 'color: black'

        if len(row['labelColors']) > 0:
            colored = f"color: {row['labelColors'][0]}"

            return [colored, default]

        return [default, default]

    # temp_columns needed for colorizing the table
    temp_columns = result_columns + ['labelColors']

    if 'hu' not in result_columns:
        temp_columns.append('hu')

    df = df[temp_columns]

    # Colorize table
    styler = df.style

    if args.colored:
        styler.apply(colorize_rows, axis=1)

    if 'labelIds' in args.keys:
        styler.apply(tint_cell_text, axis=1, subset=['labelIds', 'labelColors'])

    # Convert DataFrame to excel file
    result_filename = f'vehicles_{date.today().isoformat()}.xlsx'.replace('-', '_')
    styler.to_excel(result_filename, sheet_name='vehicles', index=False, columns=result_columns)


if __name__ == '__main__':
    send_csv_file(SERVER_ENDPOINT, {}, FILE_PATH)
