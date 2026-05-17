from playwright.sync_api import Page


BASE_URL = (
    "http://127.0.0.1:8000"
)


def test_high_risk_patient_flow(
    page: Page
):

    """
    Validate that severe symptoms
    produce a visible high-risk
    classification in the UI.
    """

    page.goto(
        f"{BASE_URL}/patient-intake-ui"
    )

    page.fill(
        "#symptoms",
        "Severe chest pain"
    )

    page.click(
        "text=Submit Symptoms"
    )

    page.wait_for_timeout(1000)

    response_text = page.locator(
        "#response"
    ).inner_text()

    assert (
        "high"
        in
        response_text.lower()
    )


def test_invalid_file_upload(
    page: Page
):

    """
    Validate that unsupported
    medical files display
    appropriate UI error messages.
    """

    page.goto(
        f"{BASE_URL}/patient-intake-ui"
    )

    page.set_input_files(
        "#medicalFile",
        {
            "name": "virus.exe",
            "mimeType":
            "application/octet-stream",
            "buffer": b"malicious"
        }
    )

    page.click(
        "text=Upload Medical Chart"
    )

    page.wait_for_timeout(1000)

    response_text = page.locator(
        "#response"
    ).inner_text()

    assert (
        "unsupported file format"
        in
        response_text.lower()
    )


def test_successful_medical_upload(
    page: Page
):

    """
    Validate successful upload
    workflow for supported
    medical chart formats.
    """

    page.goto(
        f"{BASE_URL}/patient-intake-ui"
    )

    page.set_input_files(
        "#medicalFile",
        {
            "name": "chart.pdf",
            "mimeType":
            "application/pdf",
            "buffer": b"valid medical chart"
        }
    )

    page.click(
        "text=Upload Medical Chart"
    )

    page.wait_for_timeout(1000)

    response_text = page.locator(
        "#response"
    ).inner_text()

    assert (
        "upload successful"
        in
        response_text.lower()
    )