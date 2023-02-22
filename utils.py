import json
import urllib3


def request(method, url, headers, body: dict = {}):
    http = urllib3.PoolManager()

    if body:
        body = json.dumps(body)

    response = http.request(method=method, url=url, body=body, headers=headers)
    decoded_response = response.data.decode('utf-8')

    return decoded_response


def get_access_token(method, url, headers, data):
    response = request(method, url, headers, data)
    token = json.loads(response)['oauth']['access_token']

    return token
