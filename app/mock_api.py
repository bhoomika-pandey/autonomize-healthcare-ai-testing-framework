from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health_check():

    return {
        "message": "Healthcare AI Testing API is running"
    }