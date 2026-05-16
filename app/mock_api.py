from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

app = FastAPI(
    title="Autonomize Healthcare AI Testing API",
    description="Mock APIs for AI healthcare testing assignment",
    version="1.0"
)

class RiskRequest(BaseModel):
    symptoms: str


# Mock Patient Database
# ---------------------

mock_patient_db = {
    "P123": {
        "patient_id": "P123",
        "name": "John Doe",
        "dob": "1990-01-01",
        "condition": "Diabetes"
    },
    "P456": {
        "patient_id": "P456",
        "name": "Alice Smith",
        "dob": "1985-05-12",
        "condition": "Hypertension"
    }
}

# Health Check API
# ----------------

@app.get("/")
def root():
    return {"message": "Healthcare AI Testing API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Patient Extraction API
# ----------------------

@app.get("/extract-patient/{patient_id}")
def extract_patient(patient_id: str):
    if patient_id not in mock_patient_db:
        raise HTTPException(
            status_code=404,
            detail="Patient record not found"
        )

    return mock_patient_db[patient_id]

# AI Risk Prediction API
# ----------------------

@app.post("/predict-risk")
def predict_risk(request: RiskRequest):
    symptoms = request.symptoms.strip().lower()

    if not symptoms:
        raise HTTPException(
            status_code=400,
            detail="Symptoms cannot be empty"
        )
    
    if "ignore all instructions" in symptoms:
        raise HTTPException(
            status_code=400,
            detail="Potential prompt injection detected"
        )

    if "chest pain" in symptoms:
        risk = "high"
        confidence = 0.95

    elif "fever" in symptoms:
        risk = "medium"
        confidence = 0.75

    else:
        risk = "low"
        confidence = 0.60

    return {
        "risk_level": risk,
        "confidence": confidence
    }

# Upload Validation API
# ---------------------

@app.post("/upload-chart")
def upload_chart(file: UploadFile = File(...)):
    allowed_extensions = ["pdf", "png", "jpg", "jpeg"]
    extension = file.filename.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )
    
    content = file.file.read()

    if len(content) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds allowed limit"
        )

    return {
        "message": "File uploaded successfully"
    }