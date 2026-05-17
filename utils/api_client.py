import os
import requests

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils.logger import logger

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 5))


session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("http://", adapter)
session.mount("https://", adapter)

def get_request(endpoint):
    url = f"{BASE_URL}{endpoint}"

    logger.info(f"Sending GET request to: {url}")

    response = session.get(
        url,
        timeout=REQUEST_TIMEOUT
    )
    logger.info(f"Response Status: {response.status_code}")

    return response

def post_request(endpoint, payload):
    url = f"{BASE_URL}{endpoint}"

    logger.info(f"Sending POST request to: {url}")
    logger.info(f"Payload: {payload}")

    response = session.post(
        url,
        json=payload,
        timeout=REQUEST_TIMEOUT
    )
    logger.info(f"Response Status: {response.status_code}")

    return response

def upload_file_request(endpoint, files):
    url = f"{BASE_URL}{endpoint}"
    logger.info(f"Uploading file to: {url}")
    response = session.post(
        url,
        files=files,
        timeout=REQUEST_TIMEOUT
    )
    logger.info(f"Response Status: {response.status_code}")

    return response