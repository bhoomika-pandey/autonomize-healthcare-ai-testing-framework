import io

import pytest

from utils.api_client import upload_file_request


@pytest.mark.regression
def test_invalid_file_upload():

    # Validate unsupported medical file upload rejection logic.

    file_data = io.BytesIO(b"dummy executable content")
    files = {"file": ("malware.exe", file_data, "application/octet-stream")}
    response = upload_file_request("/upload-chart", files)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Unsupported file format"


@pytest.mark.regression
def test_empty_file_upload():

    # Validate empty medical file upload handling.

    empty_file = io.BytesIO(b"")
    files = {"file": ("empty.pdf", empty_file, "application/pdf")}
    response = upload_file_request("/upload-chart", files)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Uploaded file is empty"


@pytest.mark.regression
def test_large_file_upload():

    # Validate oversized medical file upload restriction logic.

    large_content = b"a" * (6 * 1024 * 1024)
    large_file = io.BytesIO(large_content)
    files = {"file": ("large.pdf", large_file, "application/pdf")}
    response = upload_file_request("/upload-chart", files)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "File size exceeds allowed limit"
