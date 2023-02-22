from flask import Flask

from utils import get_access_token

app = Flask(__name__)

endpoints = {
    'login_url': "https://api.baubuddy.de/index.php/login",
    'vehicles_url': "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active",
    'labels_url': "https://api.baubuddy.de/dev/index.php/v1/labels/"
}

login_data = {
    "username": "365",
    "password": "1"
}

request_headers = {
    "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json"
}


@app.route('/', methods=["POST"])
def handle_csv():
    pass


if __name__ == '__main__':
    """Authorize requests to https://api.baubuddy.de with starting of the server"""
    access_token = get_access_token('POST', endpoints["login_url"], request_headers, login_data)
    request_headers["Authorization"] = f"Bearer {access_token}"

    app.run()
