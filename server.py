import csv
import json
import os
from flask import Flask, request
from utils import my_request

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'csv'}

endpoints = {
    'login_url': "https://api.baubuddy.de/index.php/login",
    'active_vehicles_url': "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active",
    'labels_url': "https://api.baubuddy.de/dev/index.php/v1/labels/"
}

login_data = {
    "username": "365",
    "password": "1"
}

unauthorized_headers = {
    "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json"
}


authorized_headers = {
    "Content-Type": "application/json"
}


@app.route('/', methods=["POST"])
def handle_csv():
    """Download .csv file from POST request, get resources from https://api.baubuddy.de,
    merge .csv file with those resources, applies filtering, and return JSON as response """

    # Authorize requests to https://api.baubuddy.de
    server_response = my_request(method="POST", url=endpoints['login_url'], headers=unauthorized_headers, body=login_data)
    access_token = json.loads(server_response)['oauth']['access_token']
    authorized_headers["Authorization"] = f"Bearer {access_token}"

    # Get info for the file from the request
    file_name = request.files['filefield'].filename
    file_data = request.files['filefield'].stream.read().decode('utf-8')

    # Check if downloaded file is with extension '.csv' otherwise return response 400 BAD REQUEST
    if file_name.split('.')[-1] not in ALLOWED_EXTENSIONS:
        response = json.dumps({
            "status": "400 BAD REQUEST",
            "message": "The provided file is not with extension" +
                       " .csv" + " and cannot be processed. Please provide valid" + ".csv" + " file",
        }, indent=4)
    else:
        # Get active vehicles from https://api.baubuddy.de
        active_vehicles = json.loads(my_request('GET', endpoints["active_vehicles_url"], authorized_headers))

        # Merge downloaded .csv file with active vehicles
        all_vehicles = [vehicle for vehicle in active_vehicles]

        with open('downloaded_file.csv', 'w') as downloaded_file:
            downloaded_file.write(file_data)

        with open('downloaded_file.csv', 'r+') as downloaded_file:
            filtered = (line.replace('\n', '') for line in downloaded_file)
            csv_reader = csv.DictReader(filtered, delimiter=';')

            for row in csv_reader:
                if row not in all_vehicles:
                    all_vehicles.append(row)

        # Filter out all vehicles that not have value for 'hu' field
        filtered_vehicles = [vehicle for vehicle in all_vehicles if 'hu' in vehicle and vehicle['hu'] is not None]

        # Resolve labels colorCode
        for vehicle in filtered_vehicles:
            colors = []
            if vehicle['labelIds'] is not None:
                label_response = json.loads(
                    my_request("GET", endpoints['labels_url'] + f"{vehicle['labelIds']}", request_headers))
                if label_response[0]['colorCode'] is not None:
                    colors.append(label_response[0]['colorCode'])
            vehicle['labelColors'] = colors

        # Return json response
        response = json.dumps(filtered_vehicles, indent=4)
        os.remove('downloaded_file.csv')

    return response


if __name__ == '__main__':
    app.run()
