from fastapi import FastAPI

app = FastAPI(title="The Dugout API")

@app.get("/")
def home():
    return {"message": "Welcome to The Dugout"}
