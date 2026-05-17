from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File
)

from fastapi.responses import HTMLResponse

app = FastAPI()


PATIENT_DATABASE = {
    "P123": {
        "patient_id": "P123",
        "name": "John Doe",
        "dob": "1990-01-01",
        "condition": "Diabetes"
    },
    "P456": {
        "patient_id": "P456",
        "name": "Jane Smith",
        "dob": "1985-05-12",
        "condition": "Hypertension"
    }
}


@app.get("/")
def home():

    return {
        "message": (
            "Healthcare AI Agentic "
            "Testing Platform"
        )
    }


@app.get(
    "/patient-intake-ui",
    response_class=HTMLResponse
)
def patient_intake_ui():

    return """
    <!DOCTYPE html>

    <html>

    <head>
        <title>
            Patient Intake Portal
        </title>

        <style>

            body {
                font-family: Arial;
                margin: 40px;
            }

            input, textarea {
                width: 400px;
                margin-bottom: 10px;
                padding: 8px;
            }

            button {
                padding: 10px 20px;
            }

            .response {
                margin-top: 20px;
                font-weight: bold;
            }

            .error {
                color: red;
            }

        </style>
    </head>

    <body>

        <h1>
            Patient Intake Portal
        </h1>

        <textarea
            id="symptoms"
            placeholder="Enter symptoms"
        ></textarea>

        <br>

        <button onclick="submitSymptoms()">
            Submit Symptoms
        </button>

        <br><br>

        <input
            type="file"
            id="medicalFile"
        />

        <button onclick="uploadFile()">
            Upload Medical Chart
        </button>

        <div
            id="response"
            class="response"
        ></div>

        <script>

            async function submitSymptoms() {

                const symptoms =
                    document.getElementById(
                        "symptoms"
                    ).value;

                const response = await fetch(
                    "/predict-risk",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                            "application/json"
                        },

                        body: JSON.stringify({
                            symptoms: symptoms
                        })
                    }
                );

                const data =
                    await response.json();

                document.getElementById(
                    "response"
                ).innerHTML =
                    "Risk Level: "
                    + data.risk_level;
            }


            async function uploadFile() {

                const fileInput =
                    document.getElementById(
                        "medicalFile"
                    );

                const file =
                    fileInput.files[0];

                const formData =
                    new FormData();

                formData.append(
                    "file",
                    file
                );

                const response =
                    await fetch(
                        "/upload-chart",
                        {
                            method: "POST",
                            body: formData
                        }
                    );

                const data =
                    await response.json();

                if (response.status !== 200) {

                    document.getElementById(
                        "response"
                    ).innerHTML =
                        "<span class='error'>"
                        + data.detail +
                        "</span>";

                } else {

                    document.getElementById(
                        "response"
                    ).innerHTML =
                        "Upload Successful";
                }
            }

        </script>

    </body>

    </html>
    """


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.get("/extract-patient/{patient_id}")
def extract_patient_data(patient_id: str):

    patient_data = (
        PATIENT_DATABASE.get(patient_id)
    )

    if not patient_data:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient_data


@app.post("/predict-risk")
def predict_risk(payload: dict):

    symptoms = (
        payload.get("symptoms", "")
        .lower()
        .strip()
    )

    if not symptoms:

        raise HTTPException(
            status_code=400,
            detail="Symptoms cannot be empty"
        )

    if (
        "ignore all instructions"
        in symptoms
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Potential prompt "
                "injection detected"
            )
        )

    if (
        "chest pain"
        in symptoms
    ):

        return {
            "risk_level": "high",
            "confidence": 0.95
        }

    if (
        "fever"
        in symptoms
    ):

        return {
            "risk_level": "medium",
            "confidence": 0.80
        }

    return {
        "risk_level": "low",
        "confidence": 0.60
    }


@app.post("/upload-chart")
async def upload_medical_chart(
    file: UploadFile = File(...)
):

    allowed_extensions = [
        ".pdf",
        ".png",
        ".jpg"
    ]

    if not any(
        file.filename.endswith(ext)
        for ext in allowed_extensions
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file format"
            )
        )

    content = await file.read()

    if not content:

        raise HTTPException(
            status_code=400,
            detail=(
                "Uploaded file is empty"
            )
        )

    if len(content) > (
        5 * 1024 * 1024
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "File size exceeds "
                "allowed limit"
            )
        )

    return {
        "message":
        "File uploaded successfully"
    }