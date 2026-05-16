import requests

BASE_URL = "http://127.0.0.1:8000"


def test_invalid_file_upload():

    files = {
        "file": (
            "malware.exe",
            b"fake-content"
        )
    }

    response = requests.post(
        f"{BASE_URL}/upload-chart",
        files=files
    )

    assert response.status_code == 400

    data = response.json()

    assert (
        data["detail"] == "Unsupported file format. Only PDF files are allowed."
    )