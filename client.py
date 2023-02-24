from utils import my_request


def send_csv_file(url, headers, file_name):
    decoded_response = my_request(method="POST", url=url, headers=headers, file_name=file_name)
    print(decoded_response)


send_csv_file("http://127.0.0.1:5000", {}, 'vehicles.csv')
