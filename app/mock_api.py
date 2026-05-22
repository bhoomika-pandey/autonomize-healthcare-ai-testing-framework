from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse

from app import workflow_engine as we

app = FastAPI()

# Patient database is loaded lazily via workflow_engine.load_patient_database()


@app.get("/")
def home():

    return {"message": ("Healthcare AI Agentic " "Testing Platform")}


@app.get("/patient-intake-ui", response_class=HTMLResponse)
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

                if (response.status !== 200) {
                    document.getElementById(
                        "response"
                    ).innerHTML =
                        "<span class='error'>"
                        + data.detail +
                        "</span>";
                    return;
                }

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

                if (!file) {
                    document.getElementById(
                        "response"
                    ).innerHTML =
                        "<span class='error'>"
                        + "Please select a medical chart file"
                        + "</span>";
                    return;
                }

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

    return {"status": "healthy"}


@app.get("/extract-patient/{patient_id}")
def extract_patient_data(patient_id: str):

    patient_db = we.load_patient_database()
    patient_data = patient_db.get(patient_id)

    if not patient_data:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patient_data


@app.post("/predict-risk")
def predict_risk(payload: dict):

    prediction = we.classify_risk(payload.get("symptoms", ""))

    if prediction["risk_level"] == "invalid":
        raise HTTPException(status_code=400, detail=prediction["reason"])

    if prediction["risk_level"] == "blocked":
        raise HTTPException(status_code=400, detail=prediction["reason"])

    return prediction


@app.post("/upload-chart")
async def upload_medical_chart(file: UploadFile = File(...)):

    allowed_extensions = [".pdf", ".png", ".jpg"]

    if not any(file.filename.endswith(ext) for ext in allowed_extensions):

        raise HTTPException(status_code=400, detail=("Unsupported file format"))

    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail=("Uploaded file is empty"))

    if len(content) > (5 * 1024 * 1024):
        raise HTTPException(
            status_code=400, detail=("File size exceeds " "allowed limit")
        )

    return {"message": "File uploaded successfully"}


@app.post("/workflow/patient-intake")
def patient_intake_workflow(payload: dict):

    result = we.run_patient_intake_workflow(
        patient_id=payload.get("patient_id", ""),
        symptoms=payload.get("symptoms", ""),
        chart_file_name=payload.get("chart_file_name", ""),
        chart_file_size_bytes=payload.get("chart_file_size_bytes", 0),
    )

    if result["workflow_status"] == "failed":
        raise HTTPException(status_code=400, detail=result)

    return result
