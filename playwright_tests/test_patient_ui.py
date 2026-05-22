import os

from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


def test_high_risk_patient_flow(page: Page):
    # Validate high-risk patient symptom workflow in UI.

    page.goto(f"{BASE_URL}/patient-intake-ui")
    page.fill("#symptoms", "Severe chest pain")

    page.click("text=Submit Symptoms")

    expect(page.locator("#response")).to_contain_text("high")


def test_invalid_file_upload(page: Page):
    # Validate unsupported medical file upload handling in UI.

    page.goto(f"{BASE_URL}/patient-intake-ui")

    page.set_input_files(
        "#medicalFile",
        {
            "name": "virus.exe",
            "mimeType": "application/octet-stream",
            "buffer": b"malicious",
        },
    )

    page.click("text=Upload Medical Chart")

    expect(page.locator("#response")).to_contain_text("Unsupported file format")
    expect(page.locator("#response span.error")).to_be_visible()


def test_empty_symptoms_flow(page: Page):
    # Validate empty symptoms input shows a clear error message.

    page.goto(f"{BASE_URL}/patient-intake-ui")
    page.click("text=Submit Symptoms")

    expect(page.locator("#response")).to_contain_text("Symptoms cannot be empty")
    expect(page.locator("#response span.error")).to_be_visible()


def test_no_file_selected(page: Page):
    # Validate UI warns when no chart file is selected.

    page.goto(f"{BASE_URL}/patient-intake-ui")
    page.click("text=Upload Medical Chart")

    expect(page.locator("#response")).to_contain_text(
        "Please select a medical chart file"
    )
    expect(page.locator("#response span.error")).to_be_visible()


def test_large_file_upload(page: Page):
    # Validate oversized medical file upload rejection in UI.

    page.goto(f"{BASE_URL}/patient-intake-ui")
    page.set_input_files(
        "#medicalFile",
        {
            "name": "large.pdf",
            "mimeType": "application/pdf",
            "buffer": b"a" * (6 * 1024 * 1024),
        },
    )

    page.click("text=Upload Medical Chart")

    expect(page.locator("#response")).to_contain_text("File size exceeds allowed limit")
    expect(page.locator("#response span.error")).to_be_visible()


def test_successful_medical_upload(page: Page):
    # Validate successful healthcare chart upload workflow in UI.

    page.goto(f"{BASE_URL}/patient-intake-ui")
    page.set_input_files(
        "#medicalFile",
        {
            "name": "chart.pdf",
            "mimeType": "application/pdf",
            "buffer": b"valid medical chart",
        },
    )

    page.click("text=Upload Medical Chart")

    expect(page.locator("#response")).to_contain_text("Upload Successful")
