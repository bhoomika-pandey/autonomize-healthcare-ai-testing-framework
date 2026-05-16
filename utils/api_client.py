import requests

BASE_URL = "http://127.0.0.1:8000"


def get_request(endpoint):

    return requests.get(f"{BASE_URL}{endpoint}")


def post_request(endpoint, payload):

    return requests.post(
        f"{BASE_URL}{endpoint}",
        json=payload
    )