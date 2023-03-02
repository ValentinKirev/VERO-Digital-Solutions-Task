import json
import urllib3


def my_request(method, url, headers, body: dict = {}, file_name: str = ''):
    http = urllib3.PoolManager()

    if body:
        body = json.dumps(body)

    if file_name:
        with open(file_name) as fp:
            file_data = fp.read()
            response = http.request(method=method, url=url, headers=headers,
                                    fields={
                                        'filefield': (file_name, file_data),
                                    })
    else:
        response = http.request(method=method, url=url, body=body, headers=headers)

    decoded_response = response.data.decode('utf-8')

    return decoded_response


def authorize(url, headers, data):
    server_response = my_request(method="POST", url=url, headers=headers, body=data)
    access_token = json.loads(server_response)['oauth']['access_token']
    headers["Authorization"] = f"Bearer {access_token}"
